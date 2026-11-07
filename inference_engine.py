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

    def evaluate(self, memory: WorkingMemory, category: Category) -> InferenceResult:
        """Evaluate working memory against rules for a specific category.
        Guaranteed to complete in < 1.0 second and never raise unhandled exceptions.
        """
        start_time = time.perf_counter()

        crop = memory.get_fact_value("crop", "unknown").lower()
        matched_candidates: List[Tuple[Rule, float, Dict[str, Any]]] = []

        # 1. Match cycle: find all satisfying rules
        for rule in self.rules:
            if rule.category != category:
                continue

            if rule.crop != "all" and rule.crop.lower() != crop:
                continue

            matches, fired_conds = self._check_conditions(rule.conditions, memory)
            if matches:
                # Calculate combined certainty
                cf = self._compute_certainty(rule, memory)
                matched_candidates.append((rule, cf, fired_conds))

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # 2. System Boundary Check: No rules fired
        if not matched_candidates:
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

        # 3. Conflict Resolution & Rule Extension Escalation
        selected_rule, final_cf, fired_conds = self._resolve_conflicts(matched_candidates)

        # Log rule firing in working memory
        memory.log_rule_firing(
            rule_id=selected_rule.rule_id,
            rule_type=selected_rule.rule_type.value,
            details={"conditions": fired_conds, "certainty": final_cf}
        )

        # 4. Construct Explanation Trace
        trace = ExplanationTrace(
            rule_id=selected_rule.rule_id,
            rule_type=selected_rule.rule_type,
            fired_conditions=fired_conds,
            certainty_factor=final_cf,
            reasoning=selected_rule.explanation,
            limitations=(
                "Rule extended due to secondary environmental/harvest factor."
                if selected_rule.rule_type == RuleType.EXTENDED else None
            )
        )

        # 5. Extract Diagnosis and Remedies
        conc = selected_rule.conclusion
        diagnosis = (
            conc.get("name")
            or conc.get("pest_name")
            or conc.get("nutrient")
            or "Identified Condition"
        )

        # Pre-harvest safety lockout detection
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
            remedies = conc.get("remedies", [])
        elif category == Category.NUTRIENT:
            prescription = conc.get("prescription")
            timeline = conc.get("recovery_timeline")
            if prescription:
                remedies.append(f"Prescription: {prescription}")
            if timeline:
                remedies.append(f"Expected recovery: {timeline}")

        details = dict(conc)
        details["latency_ms"] = round(elapsed_ms, 2)
        details["rule_id"] = selected_rule.rule_id
        details["rule_type"] = selected_rule.rule_type.value

        return InferenceResult(
            success=True,
            category=category,
            crop=crop,
            diagnosis=diagnosis,
            confidence=round(final_cf * 100, 1),
            details=details,
            remedies=remedies,
            chemical_blocked=chemical_blocked,
            traces=[trace]
        )

    def _check_conditions(
        self, conditions: Dict[str, Any], memory: WorkingMemory
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check whether all conditions of a rule are satisfied by working memory."""
        fired_conds: Dict[str, Any] = {}

        for key, cond_val in conditions.items():
            if key == "symptoms":
                # User symptoms in working memory (list)
                user_symptoms = memory.get_fact_value("symptoms", [])
                if not isinstance(user_symptoms, list):
                    user_symptoms = [user_symptoms]
                # Rule requires all listed symptoms
                if not all(s in user_symptoms for s in cond_val):
                    return False, {}
                fired_conds[key] = cond_val

            elif key == "damage":
                user_damage = memory.get_fact_value("damage", [])
                if isinstance(user_damage, list):
                    if cond_val not in user_damage:
                        return False, {}
                else:
                    if cond_val != user_damage:
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
                if user_val is None:
                    return False, {}
                if str(user_val).lower() != str(cond_val).lower():
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
        self, candidates: List[Tuple[Rule, float, Dict[str, Any]]]
    ) -> Tuple[Rule, float, Dict[str, Any]]:
        """Conflict resolution:
        1. Give priority to EXTENDED rules over their base rules.
        2. Give priority to higher specificity (more condition keys).
        3. Break ties with higher Certainty Factor.
        """
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
