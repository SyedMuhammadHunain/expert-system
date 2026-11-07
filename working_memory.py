"""Working memory management for Agriculture Expert System.
Maintains session state, asserted facts, hypothesis evaluation, and firing history.
"""

from typing import Any, Dict, List, Optional
from knowledge_base import Fact


class WorkingMemory:
    """In-memory state tracker for expert system inference cycles."""

    def __init__(self) -> None:
        self._facts: Dict[str, Fact] = {}
        self._fired_rules: List[Dict[str, Any]] = []

    def assert_fact(self, name: str, value: Any, confidence: float = 1.0) -> Fact:
        """Assert a new fact or update existing fact in working memory."""
        fact = Fact(name=name, value=value, confidence=confidence)
        self._facts[name] = fact
        return fact

    def retract_fact(self, name: str) -> bool:
        """Retract a fact from working memory if present."""
        if name in self._facts:
            del self._facts[name]
            return True
        return False

    def get_fact(self, name: str) -> Optional[Fact]:
        """Retrieve a Fact object by name."""
        return self._facts.get(name)

    def get_fact_value(self, name: str, default: Any = None) -> Any:
        """Retrieve the value of a fact, or default if not asserted."""
        fact = self._facts.get(name)
        return fact.value if fact is not None else default

    def has_fact(self, name: str) -> bool:
        """Check whether a fact has been asserted."""
        return name in self._facts

    def all_facts(self) -> Dict[str, Fact]:
        """Return shallow copy of all current facts."""
        return dict(self._facts)

    def log_rule_firing(self, rule_id: str, rule_type: str, details: Dict[str, Any]) -> None:
        """Record a rule execution event in the working memory trail."""
        self._fired_rules.append({
            "rule_id": rule_id,
            "rule_type": rule_type,
            "details": details
        })

    def get_fired_rules(self) -> List[Dict[str, Any]]:
        """Return the complete execution trail of fired rules."""
        return list(self._fired_rules)

    def clear(self) -> None:
        """Reset working memory to fresh state."""
        self._facts.clear()
        self._fired_rules.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Export serializable snapshot of working memory."""
        return {
            "facts": {k: {"value": v.value, "confidence": v.confidence} for k, v in self._facts.items()},
            "fired_rules": list(self._fired_rules)
        }
