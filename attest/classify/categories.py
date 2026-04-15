"""EU AI Act Annex III high-risk categories and keyword signals.

Each category contains:
- id: machine-readable identifier
- name: official Annex III area name
- article: EU AI Act article reference
- description: what qualifies
- signals: keywords/patterns that suggest an AI system falls into this category
- obligations: key compliance obligations for this category
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RiskCategory:
    id: str
    name: str
    area_number: int
    description: str
    signals: list[str] = field(default_factory=list)
    obligations: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)


ANNEX_III_CATEGORIES: list[RiskCategory] = [
    RiskCategory(
        id="biometrics",
        name="Biometrics",
        area_number=1,
        description=(
            "AI systems intended for remote biometric identification, "
            "biometric categorisation by sensitive attributes, or emotion recognition"
        ),
        signals=[
            "biometric", "face recognition", "facial recognition", "face detection",
            "face id", "fingerprint", "iris scan", "voice recognition", "speaker id",
            "emotion recognition", "emotion detection", "sentiment from face",
            "gait recognition", "person re-identification", "liveness detection",
        ],
        obligations=[
            "Fundamental rights impact assessment",
            "Registration in EU database",
            "Real-time human oversight",
            "Data governance for biometric data",
        ],
        examples=["Facial recognition access control", "Emotion detection in interviews"],
    ),
    RiskCategory(
        id="critical_infrastructure",
        name="Critical Infrastructure",
        area_number=2,
        description=(
            "AI systems intended as safety components in the management and operation of "
            "critical infrastructure: road traffic, water, gas, heating, electricity, "
            "digital infrastructure"
        ),
        signals=[
            "safety component", "safety system", "safety inspection", "safety monitoring",
            "critical infrastructure", "road traffic", "traffic management",
            "water supply", "gas supply", "heating", "electricity grid", "power grid",
            "digital infrastructure", "construction safety", "site safety",
            "construction site", "structural integrity", "structural inspection",
            "bridge inspection", "hazard detection", "hazard", "ppe detection",
            "ppe violation", "ppe", "hard hat", "hard hat detection",
            "guardrail detection", "guardrail", "safety vest",
            "fall protection", "osha", "safety violation", "safety compliance",
            "crane safety", "scaffold", "excavation safety", "fire safety",
            "building inspection", "defect detection", "crack detection",
            "quality inspection", "quality control", "safety hazard",
        ],
        obligations=[
            "Risk management system (Article 9)",
            "Data governance (Article 10)",
            "Technical documentation (Article 11, Annex IV)",
            "Logging and record-keeping (Article 12)",
            "Transparency and information to deployers (Article 13)",
            "Human oversight mechanisms (Article 14)",
            "Accuracy, robustness, cybersecurity (Article 15)",
        ],
        examples=[
            "AI-powered construction safety inspection",
            "Structural defect detection in bridges",
            "PPE compliance monitoring on construction sites",
            "Quality control in manufacturing",
        ],
    ),
    RiskCategory(
        id="education",
        name="Education and Vocational Training",
        area_number=3,
        description=(
            "AI systems determining access to education, evaluating learning outcomes, "
            "assessing appropriate education level, or monitoring prohibited exam behaviour"
        ),
        signals=[
            "education", "admission", "grading", "exam", "assessment", "learning outcome",
            "student evaluation", "academic", "proctoring", "cheating detection",
            "plagiarism", "aptitude test", "vocational training",
        ],
        obligations=[
            "Non-discrimination testing across demographic groups",
            "Transparency to students and educators",
            "Human oversight for consequential decisions",
        ],
        examples=["Automated essay grading", "Exam proctoring", "Admission screening"],
    ),
    RiskCategory(
        id="employment",
        name="Employment and Worker Management",
        area_number=4,
        description=(
            "AI systems for recruitment, CV screening, candidate evaluation, "
            "promotion/termination decisions, task allocation, and performance monitoring"
        ),
        signals=[
            "recruitment", "hiring", "cv screening", "resume screening", "candidate",
            "job application", "performance review", "employee monitoring",
            "worker surveillance", "task allocation", "promotion", "termination",
            "workforce management", "productivity monitoring", "attendance",
        ],
        obligations=[
            "Bias and fairness auditing",
            "Worker notification requirements",
            "Works council / union consultation",
            "Human override for all consequential decisions",
        ],
        examples=["Resume screening AI", "Employee productivity monitoring"],
    ),
    RiskCategory(
        id="essential_services",
        name="Access to Essential Services",
        area_number=5,
        description=(
            "AI for credit scoring, insurance risk assessment, "
            "emergency service dispatch, public assistance eligibility"
        ),
        signals=[
            "credit score", "credit scoring", "creditworthiness", "loan", "mortgage",
            "insurance risk", "insurance pricing", "underwriting", "claims",
            "emergency dispatch", "911", "triage", "public assistance", "benefits",
            "welfare", "social services", "eligibility",
        ],
        obligations=[
            "Explainability of decisions to affected persons",
            "Right to human review",
            "Regular bias audits on protected characteristics",
        ],
        examples=["Credit scoring model", "Insurance risk pricing", "Emergency triage"],
    ),
    RiskCategory(
        id="law_enforcement",
        name="Law Enforcement",
        area_number=6,
        description=(
            "AI for evidence reliability assessment, crime analytics, "
            "profiling in criminal investigations, polygraph-type assessments"
        ),
        signals=[
            "law enforcement", "police", "crime prediction", "predictive policing",
            "evidence analysis", "forensic", "criminal profiling", "polygraph",
            "lie detection", "deception detection", "recidivism", "parole",
        ],
        obligations=[
            "Fundamental rights impact assessment",
            "Strict human oversight",
            "Prohibition on sole automated decision-making",
        ],
        examples=["Crime risk prediction", "Evidence analysis tool"],
    ),
    RiskCategory(
        id="migration",
        name="Migration, Asylum and Border Control",
        area_number=7,
        description=(
            "AI for interview assessment, migration risk assessment, "
            "identity document authentication in border control"
        ),
        signals=[
            "migration", "asylum", "border control", "immigration", "visa",
            "refugee", "document authentication", "passport verification",
            "identity verification", "border security",
        ],
        obligations=[
            "Non-discrimination safeguards",
            "Human review of all decisions",
            "Registration in EU database",
        ],
        examples=["Automated visa screening", "Document authentication at borders"],
    ),
    RiskCategory(
        id="justice",
        name="Administration of Justice and Democratic Processes",
        area_number=8,
        description=(
            "AI assisting judicial research, law interpretation, "
            "or intended to influence election outcomes"
        ),
        signals=[
            "judicial", "court", "legal research", "law interpretation", "sentencing",
            "election", "voting", "democratic process", "campaign",
            "political advertising",
        ],
        obligations=[
            "Full transparency of AI involvement",
            "Human judge retains final authority",
            "Public disclosure of AI use in elections",
        ],
        examples=["Legal research assistant for judges", "Sentencing recommendation tool"],
    ),
]

SAFETY_COMPONENT_SIGNALS = [
    "safety component", "safety-critical", "safety critical", "life safety",
    "structural", "load bearing", "fire protection", "fall protection",
    "pressure vessel", "machinery safety", "medical device",
    "automotive safety", "aviation safety", "railway safety",
]

CATEGORY_BY_ID = {cat.id: cat for cat in ANNEX_III_CATEGORIES}
