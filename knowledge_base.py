"""Knowledge base data structures and rule definitions for Pakistan Agriculture Expert System.
Covers 5 major Pakistani crops: Wheat, Cotton, Rice, Sugarcane, Maize.
Contains 55+ validated agricultural rules categorized as:
- Hardcoded (1.0 Certainty Factor)
- May or May Not (0.50 - 0.85 Certainty Factor)
- Extended (Rule extensions that refine or escalate based on additional factors)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RuleType(str, Enum):
    """Three rule modalities taught by instructor."""
    HARDCODED = "hardcoded"          # Deterministic 1.0 Certainty Factor
    MAY_OR_MAY_NOT = "may_or_may_not"# Probabilistic / partial certainty (0.50 - 0.85)
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


RULES: List[Rule] = [
    # Wheat
    Rule(
        rule_id="W-DIS-001",
        category=Category.DISEASE,
        crop="wheat",
        conditions={"symptoms": ["yellow_pustules_stripes"], "weather": "cool_humid"},
        conclusion={"name": "Yellow Rust (Stripe Rust / Peeli Kungi)", "severity": "High", "remedies": ["Apply Tebuconazole (Folicur) @ 200ml/acre", "Ensure field aeration"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Linear bright yellow pustules along leaf veins in cool, humid spring weather are definitive for Puccinia striiformis."
    ),
    Rule(
        rule_id="W-DIS-002",
        category=Category.DISEASE,
        crop="wheat",
        conditions={"symptoms": ["brown_oval_pustules"]},
        conclusion={"name": "Brown Rust (Leaf Rust / Bhoori Kungi)", "severity": "Moderate", "remedies": ["Foliar spray of Propiconazole (Tilt 250 EC) @ 200ml/acre"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Scattered brown pustules without distinct striping indicate leaf rust, highly likely in warm temperatures."
    ),
    Rule(
        rule_id="W-DIS-003",
        category=Category.DISEASE,
        crop="wheat",
        conditions={"symptoms": ["black_powdery_heads"]},
        conclusion={"name": "Loose Smut (Kani)", "severity": "Severe", "remedies": ["Rogue out infected heads immediately", "Use certified Vitavax seed dressing next season"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Ear heads completely transformed into black sooty spore mass is a classic diagnostic marker for Ustilago tritici."
    ),
    Rule(
        rule_id="W-DIS-004",
        category=Category.DISEASE,
        crop="wheat",
        conditions={"symptoms": ["fishy_smell_grains", "blackened_kernels"], "weather": "high_humidity"},
        conclusion={"name": "Karnal Bunt", "severity": "Moderate", "remedies": ["Spray Azoxystrobin + Difenoconazole at boot stage", "Avoid night sprinkler irrigation"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.90,
        explanation="Extended rule: High humidity at ear emergence converts marginal bunt symptoms into severe Karnal Bunt with trimethylamine odour.",
        extended_from="W-DIS-002"
    ),
    # Wheat Pests
    Rule(
        rule_id="W-PST-001",
        category=Category.PEST,
        crop="wheat",
        conditions={"plant_zone": "leaves", "damage": "sticky_honeydew", "sightings": "tiny_green_insects"},
        conclusion={"pest_name": "Wheat Aphid (Sust Sula)", "severity_tier": "Moderate", "bio_controls": ["Conserve Chrysoperla carnea predators", "Neem oil spray (2%)"], "chemical_controls": ["Imidacloprid 200 SL @ 60ml/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Clusters of tiny soft green insects producing sticky secretions on wheat flag leaves confirm aphid colonies."
    ),
    Rule(
        rule_id="W-PST-002",
        category=Category.PEST,
        crop="wheat",
        conditions={"plant_zone": "leaves", "damage": "chewed_leaf_margins", "sightings": "caterpillars"},
        conclusion={"pest_name": "Armyworm (Lashkari Soondi)", "severity_tier": "Severe", "bio_controls": ["Bacillus thuringiensis (Bt) formulation", "Pheromone traps"], "chemical_controls": ["Emamectin Benzoate 1.9 EC @ 200ml/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Chewed leaf margins accompanied by nocturnal caterpillar sightings represent active armyworm marching."
    ),
    Rule(
        rule_id="W-PST-003",
        category=Category.PEST,
        crop="wheat",
        conditions={"plant_zone": "roots", "damage": "dry_wilted_plants"},
        conclusion={"pest_name": "Termite Infestation (Seemuk)", "severity_tier": "Moderate", "bio_controls": ["Beauveria bassiana drenching", "Crop rotation"], "chemical_controls": ["Chlorpyrifos 40 EC @ 1-2 Litres/acre with irrigation"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.70,
        explanation="Root-zone wilting and easily uprooted wheat tillers indicate underground termite root feeding."
    ),
    Rule(
        rule_id="W-PST-004",
        category=Category.PEST,
        crop="wheat",
        conditions={"plant_zone": "leaves", "damage": "chewed_leaf_margins", "sightings": "caterpillars", "near_harvest": True},
        conclusion={"pest_name": "Late Armyworm Outbreak", "severity_tier": "Severe", "bio_controls": ["Hand collection and Bt biological spray", "Trichogramma releases"], "chemical_controls": ["BLOCKED: Pre-harvest interval (PHI) prevents chemical spray"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: When armyworm strikes within 14 days of harvest, toxic synthetics are locked out to protect grain safety.",
        extended_from="W-PST-002"
    ),
    # Wheat Nutrients
    Rule(
        rule_id="W-NUT-001",
        category=Category.NUTRIENT,
        crop="wheat",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "vegetative", "ph_min": 7.5, "ph_max": 8.5},
        conclusion={"nutrient": "Nitrogen (N)", "prescription": "Urea (46% N) @ 50 kg/acre split top-dress before first irrigation", "recovery_timeline": "7-10 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="General chlorosis starting on older lower wheat leaves in alkaline Indus plain soil signals nitrogen depletion."
    ),
    Rule(
        rule_id="W-NUT-002",
        category=Category.NUTRIENT,
        crop="wheat",
        conditions={"discoloration": "purple_leaf_undersides", "stage": "vegetative"},
        conclusion={"nutrient": "Phosphorus (P)", "prescription": "Diammonium Phosphate (DAP 18-46-0) @ 50 kg/acre or Single Super Phosphate", "recovery_timeline": "10-14 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Purplish pigmentation on underside of leaves and stunted root branching is textbook phosphorus deficiency."
    ),
    Rule(
        rule_id="W-NUT-003",
        category=Category.NUTRIENT,
        crop="wheat",
        conditions={"discoloration": "interveinal_chlorosis", "stage": "vegetative", "ph_min": 7.8, "ph_max": 8.5},
        conclusion={"nutrient": "Zinc (Zn)", "prescription": "Zinc Sulphate (33% Zn) @ 6 kg/acre or foliar 0.5% chelated Zn spray", "recovery_timeline": "5-7 days"},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.80,
        explanation="Interveinal pale bleaching of middle leaves in high pH soils points strongly to zinc unavailability."
    ),

    # Cotton
    Rule(
        rule_id="C-DIS-001",
        category=Category.DISEASE,
        crop="cotton",
        conditions={"symptoms": ["leaf_curling_upward", "thickened_veins"]},
        conclusion={"name": "Cotton Leaf Curl Virus (CLCuV)", "severity": "Severe", "remedies": ["Eradicate whitefly vectors immediately", "Spray foliar micronutrient cocktail (Zn+B)", "Cultivate CLCuV-tolerant BT hybrids next season"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Upward curling of leaves, vein swelling, and enation under leaves are signature symptoms of whitefly-vectored CLCuV."
    ),
    Rule(
        rule_id="C-DIS-002",
        category=Category.DISEASE,
        crop="cotton",
        conditions={"symptoms": ["angular_water_soaked_spots", "black_veins"]},
        conclusion={"name": "Bacterial Blight / Angular Leaf Spot (Kala Tilla)", "severity": "High", "remedies": ["Copper Oxychloride (50 WP) @ 500g/acre + Streptomycin @ 20g/acre", "Avoid excessive flood irrigation"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Angular leaf lesions bounded by veinlets caused by Xanthomonas citri pv. malvacearum."
    ),
    Rule(
        rule_id="C-DIS-003",
        category=Category.DISEASE,
        crop="cotton",
        conditions={"symptoms": ["sudden_plant_wilting", "rotted_taproot"]},
        conclusion={"name": "Cotton Root Rot (Jarrh Galan)", "severity": "Severe", "remedies": ["Soil drenching with Thiophanate Methyl @ 400g/acre", "Rotate with sorghum or moth bean"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Entire patches of plants wilting within 24 hours accompanied by shredded bark on taproots indicates Rhizoctonia root rot."
    ),
    Rule(
        rule_id="C-DIS-004",
        category=Category.DISEASE,
        crop="cotton",
        conditions={"symptoms": ["leaf_curling_upward", "thickened_veins"], "weather": "hot_dry"},
        conclusion={"name": "Virulent CLCuV Epidemic", "severity": "Critical", "remedies": ["Intensive vector eradication with Pyriproxyfen + Dinotefuran", "Foliar potash spray 2% to support plant resilience"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Hot dry spell accelerates whitefly lifecycle, turning localized CLCuV into rapid epidemic.",
        extended_from="C-DIS-001"
    ),
    # Cotton Pests
    Rule(
        rule_id="C-PST-001",
        category=Category.PEST,
        crop="cotton",
        conditions={"plant_zone": "fruit", "damage": "bore_holes", "sightings": "caterpillars"},
        conclusion={"pest_name": "Pink Bollworm (Gulabi Soondi)", "severity_tier": "Severe", "bio_controls": ["Install PB Rope L / Gossyplure pheromone traps (6/acre)", "Trichogramma card releases"], "chemical_controls": ["Spinetoram 120 SC @ 80ml/acre or Gamma-Cyhalothrin"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Rosetted flowers and bore holes plugged with larval frass into developing bolls confirm Pectinophora gossypiella."
    ),
    Rule(
        rule_id="C-PST-002",
        category=Category.PEST,
        crop="cotton",
        conditions={"plant_zone": "leaves", "damage": "sticky_honeydew", "sightings": "white_flying_flies"},
        conclusion={"pest_name": "Cotton Whitefly (Safaid Makhi)", "severity_tier": "Severe", "bio_controls": ["Yellow sticky traps (20/acre)", "Neem seed extract 3%"], "chemical_controls": ["Pyriproxyfen 10.8 EC @ 500ml/acre or Spirotetramat"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Clouds of minute white flies flushing on foliage disturbance with lower leaf sooty mold confirm Bemisia tabaci."
    ),
    Rule(
        rule_id="C-PST-003",
        category=Category.PEST,
        crop="cotton",
        conditions={"plant_zone": "leaves", "damage": "chewed_leaf_margins", "sightings": "tiny_green_insects"},
        conclusion={"pest_name": "Cotton Jassid (Subz Tela)", "severity_tier": "Moderate", "bio_controls": ["Encourage predator spiders and ladybird beetles", "Castor oil trap cropping"], "chemical_controls": ["Flonicamid 50 WG @ 60g/acre"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.80,
        explanation="Hopper burn on leaf margins with wedge-shaped green insects moving sideways signifies Amrasca devastans."
    ),
    Rule(
        rule_id="C-PST-004",
        category=Category.PEST,
        crop="cotton",
        conditions={"plant_zone": "stems", "damage": "sticky_honeydew", "sightings": "white_waxy_clusters"},
        conclusion={"pest_name": "Cotton Mealybug (Guddi Keera)", "severity_tier": "Severe", "bio_controls": ["Aenasius bambawalei parasitic wasps", "Neem soap spray"], "chemical_controls": ["Profenofos 50 EC @ 800ml/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="White waxy cotton-like coatings on stems and terminal shoots indicate invasive Phenacoccus solenopsis."
    ),
    Rule(
        rule_id="C-PST-005",
        category=Category.PEST,
        crop="cotton",
        conditions={"plant_zone": "fruit", "damage": "bore_holes", "sightings": "caterpillars", "near_harvest": True},
        conclusion={"pest_name": "Terminal Bollworm Infestation", "severity_tier": "Severe", "bio_controls": ["Manual infected boll removal and Bt dusting", "Light traps"], "chemical_controls": ["BLOCKED: Pre-harvest interval (PHI) prevents synthetic insecticide"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Late-season bollworm attack near harvest halts synthetic chemicals to avoid lint residue contamination.",
        extended_from="C-PST-001"
    ),
    # Cotton Nutrients
    Rule(
        rule_id="C-NUT-001",
        category=Category.NUTRIENT,
        crop="cotton",
        conditions={"discoloration": "leaf_edges_scorched_brown", "stage": "flowering"},
        conclusion={"nutrient": "Potassium (K)", "prescription": "Muriate/Sulphate of Potash (SOP 0-0-50) @ 25 kg/acre or 2% KNO3 foliar sprays", "recovery_timeline": "8-12 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Cotton is heavy K feeder during boll fill; marginal chlorosis and bronzing scorching on upper leaves signals K deficit."
    ),
    Rule(
        rule_id="C-NUT-002",
        category=Category.NUTRIENT,
        crop="cotton",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "vegetative"},
        conclusion={"nutrient": "Nitrogen (N)", "prescription": "Urea @ 35 kg/acre split application with canal water", "recovery_timeline": "6-8 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Uniform pale green to yellow lower canopy leaves during early vegetative squaring signals nitrogen hunger."
    ),
    Rule(
        rule_id="C-NUT-003",
        category=Category.NUTRIENT,
        crop="cotton",
        conditions={"discoloration": "interveinal_chlorosis", "stage": "flowering", "ph_min": 7.8, "ph_max": 8.5},
        conclusion={"nutrient": "Magnesium (Mg)", "prescription": "Magnesium Sulphate (Epsom salt) @ 10 kg/acre or 1% foliar spray", "recovery_timeline": "7-10 days"},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Reddish-purple pigmentation between veins on mature leaves during flowering points to magnesium deficiency."
    ),

    # Rice
    Rule(
        rule_id="R-DIS-001",
        category=Category.DISEASE,
        crop="rice",
        conditions={"symptoms": ["spindle_eye_shaped_lesions", "brown_margin_grey_center"]},
        conclusion={"name": "Rice Blast (Dhan Ka Jhulka)", "severity": "Severe", "remedies": ["Tricyclazole 75 WP @ 120g/acre or Kasugamycin @ 250ml/acre", "Avoid excessive nitrogen top dressing"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Elliptical spindle-shaped lesions with ash-grey center on leaves and panicle neck rot diagnose Magnaporthe oryzae."
    ),
    Rule(
        rule_id="R-DIS-002",
        category=Category.DISEASE,
        crop="rice",
        conditions={"symptoms": ["water_soaked_leaf_margins", "milky_bacterial_ooze"]},
        conclusion={"name": "Bacterial Leaf Blight (BLB / Bakayan)", "severity": "High", "remedies": ["Bismerthiazol (Klorin 20 WP) @ 250g/acre", "Drain flood water and suspend nitrogen"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Wavy yellowish-white marginal leaf lesions exuding microscopic bacterial drops confirms Xanthomonas oryzae."
    ),
    Rule(
        rule_id="R-DIS-003",
        category=Category.DISEASE,
        crop="rice",
        conditions={"symptoms": ["circular_brown_spots_leaf"]},
        conclusion={"name": "Brown Spot (Bhoora Dag)", "severity": "Moderate", "remedies": ["Mancozeb 75 WP @ 500g/acre or Carbendazim", "Supply balanced potassium and zinc"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.70,
        explanation="Oval sesame-seed shaped brown spots with yellow halos across leaf surface indicate Bipolaris oryzae."
    ),
    Rule(
        rule_id="R-DIS-004",
        category=Category.DISEASE,
        crop="rice",
        conditions={"symptoms": ["spindle_eye_shaped_lesions", "brown_margin_grey_center"], "weather": "cool_nights_rain"},
        conclusion={"name": "Neck Blast Epidemic Outbreak", "severity": "Critical", "remedies": ["Emergency aerial/knapsack spray of Isoprothiolane (Fuji-One) @ 400ml/acre", "Immediate flood water renewal"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Rainy weather combined with dew and cool night temperatures turns leaf blast into devastating neck blast.",
        extended_from="R-DIS-001"
    ),
    # Rice Pests
    Rule(
        rule_id="R-PST-001",
        category=Category.PEST,
        crop="rice",
        conditions={"plant_zone": "stems", "damage": "bore_holes", "sightings": "caterpillars"},
        conclusion={"pest_name": "Rice Stem Borer (Dhan Ka Tilla / White Earhead)", "severity_tier": "Severe", "bio_controls": ["Pheromone lures for Scirpophaga incertulas", "Egg parasitoid Trichogramma releases"], "chemical_controls": ["Cartap Hydrochloride 4G @ 9 kg/acre or Fipronil granules"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Dead hearts in tillering stage or bleached empty 'white heads' at flowering are caused by stem borer larvae."
    ),
    Rule(
        rule_id="R-PST-002",
        category=Category.PEST,
        crop="rice",
        conditions={"plant_zone": "stems", "damage": "sticky_honeydew", "sightings": "tiny_brown_hoppers"},
        conclusion={"pest_name": "Brown Planthopper (BPH / Bhoora Tela)", "severity_tier": "Severe", "bio_controls": ["Drain standing water for 3-4 days to break reproduction cycle", "Preserve mirid bug predators"], "chemical_controls": ["Pymetrozine 50 WG @ 120g/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Circular patches of dried scorched plants ('hopper burn') near water line caused by Nilaparvata lugens."
    ),
    Rule(
        rule_id="R-PST-003",
        category=Category.PEST,
        crop="rice",
        conditions={"plant_zone": "leaves", "damage": "fine_silky_webbing", "sightings": "caterpillars"},
        conclusion={"pest_name": "Rice Leaf Folder (Patta Lapet)", "severity_tier": "Moderate", "bio_controls": ["Pass long coir rope over canopy to dislodge larvae", "Neem formulation spray"], "chemical_controls": ["Chlorantraniliprole 20 SC @ 50ml/acre"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.80,
        explanation="Leaves longitudinally folded into tubular shelters with inner surface scraped white indicates Cnaphalocrocis medinalis."
    ),
    Rule(
        rule_id="R-PST-004",
        category=Category.PEST,
        crop="rice",
        conditions={"plant_zone": "stems", "damage": "bore_holes", "sightings": "caterpillars", "near_harvest": True},
        conclusion={"pest_name": "Late Rice Stem Borer Incursion", "severity_tier": "Moderate", "bio_controls": ["Light traps and hand weeding", "Biological BT application"], "chemical_controls": ["BLOCKED: Prohibited systemic granules within 21 days of harvesting"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.90,
        explanation="Extended rule: Late borer sightings near ripening block systemic granulate poisons like Cartap to ensure Basmati export safety.",
        extended_from="R-PST-001"
    ),
    # Rice Nutrients
    Rule(
        rule_id="R-NUT-001",
        category=Category.NUTRIENT,
        crop="rice",
        conditions={"discoloration": "interveinal_chlorosis", "stage": "vegetative", "ph_min": 7.8, "ph_max": 8.5},
        conclusion={"nutrient": "Zinc (Zn - Khaira Rog)", "prescription": "Zinc Sulphate 33% @ 10 kg/acre or 21% @ 15 kg/acre broadcasted in standing water", "recovery_timeline": "5-7 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Brownish rusty patches appearing on middle leaves 2-3 weeks after transplanting in calcareous Kallar belt soil is Khaira disease (Zn deficiency)."
    ),
    Rule(
        rule_id="R-NUT-002",
        category=Category.NUTRIENT,
        crop="rice",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "vegetative"},
        conclusion={"nutrient": "Nitrogen (N)", "prescription": "Urea @ 40 kg/acre top dressed into 2 inches of stagnant water", "recovery_timeline": "6-8 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Stunted tillering and pale yellow discoloration of entire seedling canopy denotes early nitrogen starvation."
    ),
    Rule(
        rule_id="R-NUT-003",
        category=Category.NUTRIENT,
        crop="rice",
        conditions={"discoloration": "leaf_edges_scorched_brown", "stage": "flowering"},
        conclusion={"nutrient": "Potassium (K)", "prescription": "Potassium Sulphate (SOP) @ 25 kg/acre top dress before panicle initiation", "recovery_timeline": "8-10 days"},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Dark green plants with scorched leaf tips and poorly filled panicle bases denote inadequate potassium."
    ),

    # Sugarcane
    Rule(
        rule_id="S-DIS-001",
        category=Category.DISEASE,
        crop="sugarcane",
        conditions={"symptoms": ["reddened_internal_pith", "alcohol_sour_smell"]},
        conclusion={"name": "Red Rot (Rattarok / Surkh Sarhan)", "severity": "Severe", "remedies": ["Uproot and burn diseased stools", "Treat seed setts with Carbendazim (Bavistin) @ 2g/litre", "Avoid ratoon crop in infected fields"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Internal cane stalk tissues showing red discoloration with distinct white cross-bands and alcoholic fermentation smell diagnose Colletotrichum falcatum."
    ),
    Rule(
        rule_id="S-DIS-002",
        category=Category.DISEASE,
        crop="sugarcane",
        conditions={"symptoms": ["black_whip_structure_shoot"]},
        conclusion={"name": "Sugarcane Whip Smut (Kani)", "severity": "Severe", "remedies": ["Carefully bag and sever the black whip", "Dip seed setts in hot water (52°C for 30 mins) before planting"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Terminal shoot transformed into a long, whip-like unbranched black dusty structure confirms Sporisorium scitamineum."
    ),
    Rule(
        rule_id="S-DIS-003",
        category=Category.DISEASE,
        crop="sugarcane",
        conditions={"symptoms": ["yellow_white_stripes_leaf"]},
        conclusion={"name": "Sugarcane Mosaic Virus", "severity": "Moderate", "remedies": ["Control aphid vectors", "Select virus-free tissue culture seed canes"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.70,
        explanation="Contrasting pale yellow or chlorotic discontinuous stripes against dark green leaf background diagnose mosaic potyvirus."
    ),
    Rule(
        rule_id="S-DIS-004",
        category=Category.DISEASE,
        crop="sugarcane",
        conditions={"symptoms": ["reddened_internal_pith", "alcohol_sour_smell"], "weather": "waterlogged_humid"},
        conclusion={"name": "Catastrophic Red Rot Epidemic", "severity": "Critical", "remedies": ["Total field quarantine and immediate disposal", "Replace variety with resistant CPF-248 or CPF-249 canes"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Waterlogged fields and prolonged humidity rapidly disseminate red rot spores through irrigation channels.",
        extended_from="S-DIS-001"
    ),
    # Sugarcane Pests
    Rule(
        rule_id="S-PST-001",
        category=Category.PEST,
        crop="sugarcane",
        conditions={"plant_zone": "stems", "damage": "bore_holes", "sightings": "caterpillars"},
        conclusion={"pest_name": "Sugarcane Stem Borer (Kamad Ka Kida)", "severity_tier": "Severe", "bio_controls": ["Trichogramma chilonis cards (10/acre)", "Earthing up soil around base"], "chemical_controls": ["Carbofuran 3G @ 12 kg/acre or Chlorantraniliprole granules"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Bore holes on cane internodes with reddish frass and damaged internal tissues indicate Chilo sacchariphagus."
    ),
    Rule(
        rule_id="S-PST-002",
        category=Category.PEST,
        crop="sugarcane",
        conditions={"plant_zone": "leaves", "damage": "sticky_honeydew", "sightings": "white_flying_flies"},
        conclusion={"pest_name": "Sugarcane Whitefly (Safaid Makhi)", "severity_tier": "Moderate", "bio_controls": ["Conserve Chrysoperla carnea", "Foliar water jet wash"], "chemical_controls": ["Diafenthiuron 500 SC @ 200ml/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Nymphs encrusting lower surface of leaves producing abundant honeydew and sooty mold denote Aleurolobus barodensis."
    ),
    Rule(
        rule_id="S-PST-003",
        category=Category.PEST,
        crop="sugarcane",
        conditions={"plant_zone": "leaves", "damage": "chewed_leaf_margins", "sightings": "jumping_leafhoppers"},
        conclusion={"pest_name": "Sugarcane Pyrilla (Patte Ka Teeda)", "severity_tier": "Moderate", "bio_controls": ["Epiricania melanoleuca cocoon releases", "Light trapping"], "chemical_controls": ["Chlorpyrifos 40 EC @ 1 Litre/acre"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Straw-colored active bugs with snout-like heads hopping vigorously on foliage indicate Pyrilla perpusilla."
    ),
    Rule(
        rule_id="S-PST-004",
        category=Category.PEST,
        crop="sugarcane",
        conditions={"plant_zone": "stems", "damage": "bore_holes", "sightings": "caterpillars", "near_harvest": True},
        conclusion={"pest_name": "Pre-Crush Cane Borer Presence", "severity_tier": "Moderate", "bio_controls": ["Biological predator inundation", "Prioritize early milling harvest"], "chemical_controls": ["BLOCKED: Toxic granules banned within 30 days of mill crushing"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.90,
        explanation="Extended rule: Chemical controls blocked to protect sugar juice and molasses processing purity near harvest.",
        extended_from="S-PST-001"
    ),
    # Sugarcane Nutrients
    Rule(
        rule_id="S-NUT-001",
        category=Category.NUTRIENT,
        crop="sugarcane",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "vegetative"},
        conclusion={"nutrient": "Nitrogen (N)", "prescription": "Urea @ 100-150 kg/acre split into 3 doses during tillering phase", "recovery_timeline": "10-14 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Short thin stalks and premature dying of basal leaves signify acute nitrogen deficiency in heavy cane biomass production."
    ),
    Rule(
        rule_id="S-NUT-002",
        category=Category.NUTRIENT,
        crop="sugarcane",
        conditions={"discoloration": "leaf_edges_scorched_brown", "stage": "vegetative"},
        conclusion={"nutrient": "Potassium (K)", "prescription": "Sulphate of Potash (SOP 0-0-50) @ 50 kg/acre to bolster cane sugar recovery", "recovery_timeline": "14-20 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Orange-yellow spotting coalescing into marginal leaf firing on older leaves signals potassium scarcity."
    ),
    Rule(
        rule_id="S-NUT-003",
        category=Category.NUTRIENT,
        crop="sugarcane",
        conditions={"discoloration": "interveinal_chlorosis", "stage": "vegetative", "ph_min": 8.0, "ph_max": 8.5},
        conclusion={"nutrient": "Iron (Fe)", "prescription": "Ferrous Sulphate (FeSO4) @ 10 kg/acre soil application or 1% foliar spray", "recovery_timeline": "7-10 days"},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Complete bleached whitening of newly emerged top spindle leaves in high alkaline calcareous soils denotes iron chlorosis."
    ),

    # Maize
    Rule(
        rule_id="M-DIS-001",
        category=Category.DISEASE,
        crop="maize",
        conditions={"symptoms": ["long_elliptical_grey_green_lesions"]},
        conclusion={"name": "Northern Corn Leaf Blight (NCLB / Turcicum Blight)", "severity": "High", "remedies": ["Azoxystrobin + Difenoconazole (Amistar Top) @ 200ml/acre", "Destroy infected crop residue"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Large cigar-shaped greyish-green to tan lesions (2.5-15 cm) running parallel to leaf margins identify Exserohilum turcicum."
    ),
    Rule(
        rule_id="M-DIS-002",
        category=Category.DISEASE,
        crop="maize",
        conditions={"symptoms": ["golden_brown_pustules_scattered"]},
        conclusion={"name": "Common Rust (Puccinia sorghi)", "severity": "Moderate", "remedies": ["Mancozeb 75 WP @ 600g/acre", "Plant rust-resistant hybrid seeds"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Circular to elongate golden-brown powdery pustules distributed across both upper and lower leaf surfaces."
    ),
    Rule(
        rule_id="M-DIS-003",
        category=Category.DISEASE,
        crop="maize",
        conditions={"symptoms": ["small_rectangular_lesions"]},
        conclusion={"name": "Maydis Leaf Blight (Southern Leaf Blight)", "severity": "Moderate", "remedies": ["Propiconazole (Tilt) @ 200ml/acre", "Ensure good plant spacing"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.70,
        explanation="Small rectangular lesions confined strictly between leaf veins are typical of Bipolaris maydis."
    ),
    Rule(
        rule_id="M-DIS-004",
        category=Category.DISEASE,
        crop="maize",
        conditions={"symptoms": ["long_elliptical_grey_green_lesions"], "weather": "cool_damp_overcast"},
        conclusion={"name": "Epidemic NCLB Blight Defoliation", "severity": "Critical", "remedies": ["Immediate foliar systemic pyraclostrobin fungicide", "Provide adequate potash fertilizer to enhance leaf tissue toughness"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Prolonged wet overcast days trigger rapid conidia germination, escalating leaf blight into total premature drying.",
        extended_from="M-DIS-001"
    ),
    # Maize Pests
    Rule(
        rule_id="M-PST-001",
        category=Category.PEST,
        crop="maize",
        conditions={"plant_zone": "leaves", "damage": "chewed_leaf_margins", "sightings": "caterpillars"},
        conclusion={"pest_name": "Fall Armyworm (FAW / Makai Ka Fauji Keera)", "severity_tier": "Severe", "bio_controls": ["Apply neem seed kernel paste inside leaf whorls", "Trichogramma releases"], "chemical_controls": ["Chlorantraniliprole 18.5 SC @ 80ml/acre or Emamectin Benzoate"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Ragged 'shot-hole' whorl damage filled with moist sawdust-like frass and caterpillars with inverted 'Y' on head identify Spodoptera frugiperda."
    ),
    Rule(
        rule_id="M-PST-002",
        category=Category.PEST,
        crop="maize",
        conditions={"plant_zone": "stems", "damage": "bore_holes", "sightings": "caterpillars"},
        conclusion={"pest_name": "Maize Stem Borer (Chilo partellus)", "severity_tier": "Severe", "bio_controls": ["Intercropping with cowpea", "Release Cotesia flavipes parasitoids"], "chemical_controls": ["Carbofuran 3G whorl application @ 5 kg/acre"]},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Pinholes on young unfurled leaves progressing to terminal dead-hearts and stalk tunneling diagnose Chilo borer."
    ),
    Rule(
        rule_id="M-PST-003",
        category=Category.PEST,
        crop="maize",
        conditions={"plant_zone": "leaves", "damage": "fine_silky_webbing", "sightings": "tiny_red_mites"},
        conclusion={"pest_name": "Red Spider Mite (Surkh Makrhi)", "severity_tier": "Moderate", "bio_controls": ["Predatory phytoseiid mite releases", "Wettable sulfur spray"], "chemical_controls": ["Fenpyroximate 5 SC @ 300ml/acre"]},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.75,
        explanation="Silky webs spun on undersides of leaves accompanied by dusty yellow stippling denote Tetranychus mite feeding."
    ),
    Rule(
        rule_id="M-PST-004",
        category=Category.PEST,
        crop="maize",
        conditions={"plant_zone": "fruit", "damage": "bore_holes", "sightings": "caterpillars", "near_harvest": True},
        conclusion={"pest_name": "Corn Earworm (Helicoverpa)", "severity_tier": "Severe", "bio_controls": ["Manual sorting and Bt microbial spray", "Mineral oil drop on cob silks"], "chemical_controls": ["BLOCKED: Pre-harvest green cob safety threshold forbids insecticide"]},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.95,
        explanation="Extended rule: Caterpillars feeding on ear tips near cob harvest block chemical application to protect roasting/fodder safety.",
        extended_from="M-PST-001"
    ),
    # Maize Nutrients
    Rule(
        rule_id="M-NUT-001",
        category=Category.NUTRIENT,
        crop="maize",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "vegetative"},
        conclusion={"nutrient": "Nitrogen (N)", "prescription": "Urea (46%) @ 50 kg/acre applied at knee-high stage before hilling-up", "recovery_timeline": "5-7 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Characteristic inverted V-shaped yellowing advancing down the midrib from leaf tip on older basal leaves."
    ),
    Rule(
        rule_id="M-NUT-002",
        category=Category.NUTRIENT,
        crop="maize",
        conditions={"discoloration": "purple_leaf_undersides", "stage": "vegetative"},
        conclusion={"nutrient": "Phosphorus (P)", "prescription": "Diammonium Phosphate (DAP) @ 50 kg/acre band placed at root depth", "recovery_timeline": "10-14 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Intense reddish-purple coloration along margins of young maize seedling leaves reflects accumulation of anthocyanin due to low P."
    ),
    Rule(
        rule_id="M-NUT-003",
        category=Category.NUTRIENT,
        crop="maize",
        conditions={"discoloration": "interveinal_chlorosis", "stage": "vegetative", "ph_min": 7.5, "ph_max": 8.5},
        conclusion={"nutrient": "Zinc (Zn - White Bud)", "prescription": "Chelated Zinc EDTA (12%) @ 1 kg/acre foliar or ZnSO4 33% @ 6 kg/acre soil", "recovery_timeline": "5-8 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Broad bleached bands of white or pale yellow on both sides of the leaf midrib with emergence of stunted white new leaves ('white bud')."
    ),

    # Universal soil remediation
    Rule(
        rule_id="ALL-NUT-001",
        category=Category.NUTRIENT,
        crop="all",
        conditions={"ph_min": 4.5, "ph_max": 5.5},
        conclusion={"nutrient": "Soil Acidity Fix", "prescription": "Apply Agricultural Limestone (CaCO3) @ 1.5 - 2.0 tons/acre to raise pH to 6.5 neutral range", "recovery_timeline": "20-30 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Strongly acidic soil (pH < 5.5) fixes phosphorus and induces aluminum toxicity; agricultural lime neutralizes acidity."
    ),
    Rule(
        rule_id="ALL-NUT-002",
        category=Category.NUTRIENT,
        crop="all",
        conditions={"ph_min": 8.2, "ph_max": 8.5},
        conclusion={"nutrient": "Soil Alkalinity & Salinity Fix", "prescription": "Apply Agricultural Gypsum (Calcium Sulphate) @ 1 ton/acre followed by leaching irrigation", "recovery_timeline": "20-30 days"},
        rule_type=RuleType.HARDCODED,
        certainty_factor=1.0,
        explanation="Alkaline/sodic soil (pH > 8.2) locks micronutrients (Zn, Fe, Mn); gypsum replaces exchangeable sodium with calcium."
    ),
    Rule(
        rule_id="ALL-NUT-003",
        category=Category.NUTRIENT,
        crop="all",
        conditions={"discoloration": "leaf_edges_scorched_brown", "stage": "fruiting"},
        conclusion={"nutrient": "Potassium (K)", "prescription": "Potassium Nitrate or SOP foliar application @ 2 kg/100 L water", "recovery_timeline": "7-10 days"},
        rule_type=RuleType.MAY_OR_MAY_NOT,
        certainty_factor=0.80,
        explanation="Marginal necrosis and leaf edge curling during fruiting/grain-fill universally signals potassium depletion across heavy feeder crops."
    ),
    Rule(
        rule_id="ALL-NUT-004",
        category=Category.NUTRIENT,
        crop="all",
        conditions={"discoloration": "lower_leaves_yellowing", "stage": "fruiting", "ph_min": 8.0, "ph_max": 8.5},
        conclusion={"nutrient": "Severe Nitrogen + Micronutrient Starvation", "prescription": "Combined Urea @ 25 kg/acre + Micronutrient Zn/Fe cocktail spray", "recovery_timeline": "6-9 days"},
        rule_type=RuleType.EXTENDED,
        certainty_factor=0.90,
        explanation="Extended rule: Late-stage nitrogen yellowing aggravated by high alkaline pH locks out micro-elements, demanding combined remediation.",
        extended_from="ALL-NUT-002"
    ),
]
