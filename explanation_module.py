"""Explanation and limitations facility for Agriculture Expert System.
Translates inference results and working memory history into transparent,
human-readable reasoning steps and explicit boundary warnings.
"""

from typing import Any, Dict, List, Optional
from knowledge_base import InferenceResult, RuleType
from working_memory import WorkingMemory


class ExplanationModule:
    """Explains decision chains, certainty logic, and system limits."""

    def explain(self, result: InferenceResult, memory: Optional[WorkingMemory] = None) -> Dict[str, Any]:
        """Generate a complete structured explanation report for UI and viva audit."""
        steps: List[Dict[str, str]] = []

        # 1. Input observations step
        facts_summary = []
        if memory:
            for k, f in memory.all_facts().items():
                if k not in ("crop", "near_harvest") and f.value:
                    facts_summary.append(f"{k}: {f.value}")
        input_desc = ", ".join(facts_summary) if facts_summary else "User provided crop parameters"
        steps.append({
            "step": "1. Input Observations",
            "detail": f"Observed facts for {result.crop.title()}: {input_desc}."
        })

        # 2. Rule evaluation and modality
        if not result.success:
            steps.append({
                "step": "2. Knowledge Base Search",
                "detail": "Engine scanned 60 rules across Pakistan crop profiles. Zero rules fully satisfied."
            })
            steps.append({
                "step": "3. Boundary & Limitations Defense",
                "detail": (
                    "System knows its limitations: It refuses to fabricate diagnoses on unmapped signs. "
                    "Safety protocol delegates to field extension agronomists."
                )
            })
            return {
                "success": False,
                "summary": "No conclusive pattern matched in knowledge base.",
                "steps": steps,
                "limitations": result.limitation_notice or "Symptom pattern outside calibrated rules.",
                "safety_lock": False,
                "rule_type": "None"
            }

        # Success path
        primary_trace = result.traces[0] if result.traces else None
        rule_type_val = result.details.get("rule_type", "hardcoded")

        if rule_type_val == RuleType.HARDCODED.value:
            modality_text = "Hardcoded Rule (100% Deterministic match — exact textbook agronomy pattern)."
        elif rule_type_val == RuleType.MAY_OR_MAY_NOT.value:
            modality_text = f"Probabilistic Rule (Certainty Factor = {result.confidence}% — partial symptom footprint)."
        elif rule_type_val == RuleType.EXTENDED.value:
            modality_text = "Extended Rule (Base rule modified or escalated by secondary factor)."
        else:
            modality_text = f"Rule Modality: {rule_type_val}"

        steps.append({
            "step": "2. Rule Firing & Modality",
            "detail": f"Fired Rule [{result.details.get('rule_id', 'UNKNOWN')}]: {modality_text}"
        })

        # 3. Reasoning Chain
        reasoning = primary_trace.reasoning if primary_trace else "Conditions satisfied."
        steps.append({
            "step": "3. Agronomic Decision Chain",
            "detail": reasoning
        })

        # 4. Safety & Remedy rationale
        if result.chemical_blocked:
            steps.append({
                "step": "4. Safety Guard Override",
                "detail": (
                    "Pre-Harvest Interval (PHI) Guard active: Synthetic chemical poisons are strictly locked "
                    "out to prevent food chain toxicity. Bio-controls and cultural practices mandated."
                )
            })
        else:
            steps.append({
                "step": "4. Treatment Rationale",
                "detail": f"Prescribed {len(result.remedies)} recommended management practices."
            })

        limitations_text = (
            "System boundary: Diagnosis applies specifically to irrigated Indus Basin cropping conditions. "
            "Severe anomalies or secondary infections require soil test lab confirmation."
        )

        return {
            "success": True,
            "summary": f"Identified {result.diagnosis} with {result.confidence}% certainty.",
            "steps": steps,
            "limitations": limitations_text,
            "safety_lock": result.chemical_blocked,
            "rule_type": rule_type_val
        }
