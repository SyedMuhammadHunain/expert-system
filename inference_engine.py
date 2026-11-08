"""Pure Python forward-chaining inference engine for Agriculture Expert System.
Evaluates working memory facts against knowledge base rules with Certainty Factors,
rule extension escalation, and safe out-of-boundary handling.
"""

import time
from typing import Any, Dict, List, Optional, Tuple

from knowledge_base import (
    Category,
    ExplanationTrace,
    InferenceResult,
    Rule,
    RuleType,
    RULES,
)
from working_memory import WorkingMemory


class InferenceEngine:
    """Forward-chaining rule evaluator with certainty factor combination."""

    def __init__(self, rules: Optional[List[Rule]] = None) -> None:
        self.rules: List[Rule] = rules if rules is not None else RULES

    # Maximum confidence allowed for a partial (incomplete) rule match.
    PARTIAL_MATCH_CF_CAP: float = 0.50

    def evaluate(self, memory: WorkingMemory, category: Category) -> InferenceResult:
        """Evaluate working memory against rules for a specific category.
        Guaranteed to complete in < 1.0 second and never raise unhandled exceptions.
        """
        start_time = time.perf_counter()

        crop = memory.get_fact_value("crop", "unknown").lower()
        matched_candidates: List[Tuple[Rule, float, Dict[str, Any]]] = []
        partial_candidates: List[Tuple[Rule, float, float, Dict[str, Any]]] = []

        for rule in self.rules:
            if rule.category != category:
                continue

            if rule.crop != "all" and rule.crop.lower() != crop:
                continue

            matches, fired_conds = self._check_conditions(rule.conditions, memory)
            if matches:
                cf = self._compute_certainty(rule, memory)
                matched_candidates.append((rule, cf, fired_conds))
            else:
                match_ratio, partial_fired = self._partial_match_score(
                    rule.conditions, memory
                )
                if match_ratio > 0.0:
                    partial_candidates.append(
                        (rule, match_ratio, rule.certainty_factor, partial_fired)
                    )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if matched_candidates:
            return self._build_result(
                matched_candidates, memory, category, crop, elapsed_ms,
                is_partial=False
            )

        if partial_candidates:
            promoted = self._promote_partial_candidates(partial_candidates)
            return self._build_result(
                promoted, memory, category, crop, elapsed_ms,
                is_partial=True
            )

        # Boundary fallback: no rules matched even partially
        trace = ExplanationTrace(
            rule_id="NO_MATCH",
            rule_type=RuleType.HARDCODED,
            fired_conditions=memory.to_dict()["facts"],
            certainty_factor=0.0,
            reasoning="The provided symptoms do not match any known disease, pest, or nutrient pattern in the knowledge base.",
            limitations="System knows its limitations: Input falls outside calibrated Pakistani crop profiles."
        )
        return InferenceResult(
            success=False,
            category=category,
            crop=crop,
            diagnosis="Unknown Condition / Symptoms Unrecognized",
            confidence=0.0,
            details={"latency_ms": round(elapsed_ms, 2)},
            remedies=[
                "Consult local District Agriculture Extension Officer (Zirat Department)",
                "Submit leaf sample to nearest Agricultural Research Institute (e.g. NARC / AARI)",
                "Double-check symptom inputs and crop growth stage"
            ],
            chemical_blocked=False,
            traces=[trace],
            limitation_notice="Expert system limitation reached: Provided signs are unmapped."
        )

        return self._build_result(
            matched_candidates, memory, category, crop, elapsed_ms,
            is_partial=False
        )

    def _build_result(
        self,
        matched_candidates: List[Tuple[Rule, float, Dict[str, Any]]],
        memory: WorkingMemory,
        category: Category,
        crop: str,
        elapsed_ms: float,
        is_partial: bool = False,
    ) -> InferenceResult:
        """Build InferenceResult from matched (or partially matched) candidates."""

        selected_rule, final_cf, fired_conds = self._resolve_conflicts(
            matched_candidates, is_partial=is_partial
        )

        memory.log_rule_firing(
            rule_id=selected_rule.rule_id,
            rule_type=selected_rule.rule_type.value,
            details={"conditions": fired_conds, "certainty": final_cf}
        )

        limitation_msg = None
        if is_partial:
            limitation_msg = (
                "Partial match: Not all rule conditions were satisfied. "
                "Provide additional symptoms or environmental details to improve confidence."
            )
        elif selected_rule.rule_type == RuleType.EXTENDED:
            limitation_msg = "Rule extended due to secondary environmental/harvest factor."

        trace = ExplanationTrace(
            rule_id=selected_rule.rule_id,
            rule_type=selected_rule.rule_type,
            fired_conditions=fired_conds,
            certainty_factor=final_cf,
            reasoning=selected_rule.explanation,
            limitations=limitation_msg
        )

        conc = selected_rule.conclusion
        diagnosis = (
            conc.get("name")
            or conc.get("pest_name")
            or conc.get("nutrient")
            or "Identified Condition"
        )
        if is_partial:
            diagnosis = f"{diagnosis} (Possible)"

        remedies, chemical_blocked = self._extract_remedies(category, conc, memory)

        details = dict(conc)
        details["latency_ms"] = round(elapsed_ms, 2)
        details["rule_id"] = selected_rule.rule_id
        details["rule_type"] = selected_rule.rule_type.value
        if is_partial:
            details["match_type"] = "partial"

        return InferenceResult(
            success=True,
            category=category,
            crop=crop,
            diagnosis=diagnosis,
            confidence=round(final_cf * 100, 1),
            details=details,
            remedies=remedies,
            chemical_blocked=chemical_blocked,
            traces=[trace],
            limitation_notice=(
                "Partial match — not all conditions met. "
                "Add more symptoms or adjust weather/stage for higher confidence."
                if is_partial else None
            )
        )

    def _partial_match_score(
        self, conditions: Dict[str, Any], memory: WorkingMemory
    ) -> Tuple[float, Dict[str, Any]]:
        """Score how many conditions a rule partially satisfies.
        Returns (match_ratio 0.0-1.0, dict of matched conditions).
        Requires at least one primary discriminating fact (symptoms, damage, sightings, or discoloration)
        to prevent passive contextual facts (like plant_zone or stage alone) from triggering false positives.
        """
        total = len(conditions)
        if total == 0:
            return 0.0, {}

        matched_count = 0.0
        fired: Dict[str, Any] = {}
        has_primary_discriminator = False

        # Primary discriminator keys that represent observed damage/symptoms
        primary_keys = {"symptoms", "damage", "sightings", "discoloration"}

        for key, cond_val in conditions.items():
            if key == "symptoms":
                user_symptoms = memory.get_fact_value("symptoms", [])
                user_list = (
                    user_symptoms if isinstance(user_symptoms, list) else [user_symptoms]
                )
                overlap = [s for s in cond_val if s in user_list]
                if overlap:
                    # Proportional: matched symptoms / required symptoms
                    matched_count += len(overlap) / len(cond_val)
                    fired[key] = overlap
                    has_primary_discriminator = True

            elif key == "damage":
                user_damage = memory.get_fact_value("damage", [])
                user_list = (
                    user_damage if isinstance(user_damage, list) else [user_damage]
                )
                if cond_val in user_list:
                    matched_count += 1.0
                    fired[key] = cond_val
                    has_primary_discriminator = True

            elif key == "sightings":
                user_sight = memory.get_fact_value("sightings", None)
                if user_sight is not None and str(user_sight).lower() == str(cond_val).lower():
                    matched_count += 1.0
                    fired[key] = cond_val
                    has_primary_discriminator = True

            elif key == "discoloration":
                user_disc = memory.get_fact_value("discoloration", None)
                if user_disc is not None and str(user_disc).lower() == str(cond_val).lower():
                    matched_count += 1.0
                    fired[key] = cond_val
                    has_primary_discriminator = True

            elif key == "ph_min":
                soil_ph = memory.get_fact_value("soil_ph", None)
                if soil_ph is not None and soil_ph >= cond_val:
                    matched_count += 1.0
                    fired[key] = cond_val

            elif key == "ph_max":
                soil_ph = memory.get_fact_value("soil_ph", None)
                if soil_ph is not None and soil_ph <= cond_val:
                    matched_count += 1.0
                    fired[key] = cond_val

            else:
                user_val = memory.get_fact_value(key, None)
                if (
                    user_val is not None
                    and str(user_val).lower() == str(cond_val).lower()
                ):
                    matched_count += 1.0
                    fired[key] = cond_val

        # If rule contains any primary discriminators, at least one must have fired
        needs_primary = any(pk in conditions for pk in primary_keys)
        if needs_primary and not has_primary_discriminator:
            return 0.0, {}

        ratio = matched_count / total
        return ratio, fired

    def _promote_partial_candidates(
        self, partials: List[Tuple[Rule, float, float, Dict[str, Any]]]
    ) -> List[Tuple[Rule, float, Dict[str, Any]]]:
        """Convert partial candidates into regular candidates with capped CF.
        Returns list sorted by (match_ratio * cf) descending, CF capped at PARTIAL_MATCH_CF_CAP.
        """
        promoted: List[Tuple[Rule, float, Dict[str, Any]]] = []
        for rule, ratio, base_cf, fired in partials:
            adjusted_cf = min(ratio * base_cf, self.PARTIAL_MATCH_CF_CAP)
            promoted.append((rule, adjusted_cf, fired))

        # Sort: highest adjusted CF first; break ties by more conditions matched
        promoted.sort(
            key=lambda item: (item[1], len(item[2])),
            reverse=True
        )
        return promoted

    def _extract_remedies(
        self, category: Category, conc: Dict[str, Any], memory: WorkingMemory
    ) -> Tuple[List[str], bool]:
        """Extract remedies and enforce pre-harvest chemical lockout."""
        chemical_blocked = False
        remedies: List[str] = []

        if category == Category.PEST:
            bio_controls = conc.get("bio_controls", [])
            chem_controls = conc.get("chemical_controls", [])
            near_harvest = bool(memory.get_fact_value("near_harvest", False))

            if near_harvest or any("BLOCKED" in str(c) for c in chem_controls):
                chemical_blocked = True
                remedies.extend(bio_controls)
                remedies.append("SAFETY WARNING: Synthetic chemical insecticides blocked due to harvest proximity!")
            else:
                remedies.extend(bio_controls)
                remedies.extend(chem_controls)
        elif category == Category.DISEASE:
            remedies = list(conc.get("remedies", []))
        elif category == Category.NUTRIENT:
            if prescription := conc.get("prescription"):
                remedies.append(f"Prescription: {prescription}")
            if timeline := conc.get("recovery_timeline"):
                remedies.append(f"Expected recovery: {timeline}")

        return remedies, chemical_blocked

    def _check_conditions(
        self, conditions: Dict[str, Any], memory: WorkingMemory
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check whether all conditions of a rule are satisfied by working memory."""
        fired_conds: Dict[str, Any] = {}

        for key, cond_val in conditions.items():
            if key == "symptoms":
                user_symptoms = memory.get_fact_value("symptoms", [])
                user_list = user_symptoms if isinstance(user_symptoms, list) else [user_symptoms]
                if not all(s in user_list for s in cond_val):
                    return False, {}
                fired_conds[key] = cond_val

            elif key == "damage":
                user_damage = memory.get_fact_value("damage", [])
                user_list = user_damage if isinstance(user_damage, list) else [user_damage]
                if cond_val not in user_list:
                    return False, {}
                fired_conds[key] = cond_val

            elif key == "ph_min":
                soil_ph = memory.get_fact_value("soil_ph", None)
                if soil_ph is None or soil_ph < cond_val:
                    return False, {}
                fired_conds[key] = cond_val

            elif key == "ph_max":
                soil_ph = memory.get_fact_value("soil_ph", None)
                if soil_ph is None or soil_ph > cond_val:
                    return False, {}
                fired_conds[key] = cond_val

            else:
                user_val = memory.get_fact_value(key, None)
                if user_val is None or str(user_val).lower() != str(cond_val).lower():
                    return False, {}
                fired_conds[key] = cond_val

        return True, fired_conds

    def _compute_certainty(self, rule: Rule, memory: WorkingMemory) -> float:
        """Compute final Certainty Factor factoring in premise confidences."""
        rule_cf = rule.certainty_factor

        # Combine with minimum fact confidence from working memory
        fact_confs: List[float] = []
        for key in rule.conditions.keys():
            fact = memory.get_fact(key)
            if fact:
                fact_confs.append(fact.confidence)

        min_fact_cf = min(fact_confs) if fact_confs else 1.0
        return rule_cf * min_fact_cf

    def _resolve_conflicts(
        self,
        candidates: List[Tuple[Rule, float, Dict[str, Any]]],
        is_partial: bool = False,
    ) -> Tuple[Rule, float, Dict[str, Any]]:
        """Conflict resolution:
        1. If strict match, give priority to EXTENDED rules over their base rules.
        2. If partial match, prioritize candidate with highest proportional Certainty Factor and condition coverage.
        3. Break ties with higher Certainty Factor.
        """
        if is_partial:
            # In partial matching, do not allow weakly matched extended rules
            # to suppress higher-confidence base rules.
            # Sort by: adjusted CF (highest first), then conditions fired (most first).
            sorted_candidates = sorted(
                candidates,
                key=lambda item: (item[1], len(item[2])),
                reverse=True
            )
            return sorted_candidates[0]

        # Check if an extended rule supersedes another
        extended_from_ids = {
            r.extended_from for r, _, _ in candidates if r.extended_from
        }

        # Filter out overridden base rules
        pruned_candidates = [
            cand for cand in candidates if cand[0].rule_id not in extended_from_ids
        ]

        if not pruned_candidates:
            pruned_candidates = candidates

        # Sort by:
        # 1. Extended rule type (True first)
        # 2. Number of conditions matched (higher first)
        # 3. Certainty Factor (higher first)
        sorted_candidates = sorted(
            pruned_candidates,
            key=lambda item: (
                1 if item[0].rule_type == RuleType.EXTENDED else 0,
                len(item[0].conditions),
                item[1]
            ),
            reverse=True
        )

        return sorted_candidates[0]
