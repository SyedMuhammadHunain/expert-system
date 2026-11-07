"""Knowledge base data structures and rule definitions for Agriculture Expert System."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RuleType(str, Enum):
    """Three rule modalities taught by instructor."""
    HARDCODED = "hardcoded"          # Deterministic 1.0 Certainty Factor
    MAY_OR_MAY_NOT = "may_or_may_not"# Probabilistic / partial certainty (0.4 - 0.85)
    EXTENDED = "extended"            # Rule refined or extended based on secondary facts


class Category(str, Enum):
    """The three functional modules of the system."""
    DISEASE = "disease"
    PEST = "pest"
    NUTRIENT = "nutrient"


@dataclass
class Fact:
    """Working memory fact assertion."""
    name: str
    value: Any
    confidence: float = 1.0


@dataclass
class Rule:
    """Individual rule definition in knowledge base."""
    rule_id: str
    category: Category
    crop: str
    conditions: Dict[str, Any]
    conclusion: Dict[str, Any]
    rule_type: RuleType = RuleType.HARDCODED
    certainty_factor: float = 1.0
    explanation: str = ""
    extended_from: Optional[str] = None  # Reference to base rule if extended


@dataclass
class ExplanationTrace:
    """Trace details generated for transparent reasoning."""
    rule_id: str
    rule_type: RuleType
    fired_conditions: Dict[str, Any]
    certainty_factor: float
    reasoning: str
    limitations: Optional[str] = None


@dataclass
class InferenceResult:
    """Structured result returned by inference engine."""
    success: bool
    category: Category
    crop: str
    diagnosis: str
    confidence: float
    details: Dict[str, Any] = field(default_factory=dict)
    remedies: List[str] = field(default_factory=list)
    chemical_blocked: bool = False
    traces: List[ExplanationTrace] = field(default_factory=list)
    limitation_notice: Optional[str] = None


# Initial empty list to be populated in Task 2
RULES: List[Rule] = []
