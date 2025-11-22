from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ScamScriptType(str, Enum):
    IRS = "irs_scam"
    SOCIAL_SECURITY = "social_security_scam"
    TECH_SUPPORT = "tech_support_scam"
    GRANDPARENT = "grandparent_emergency_scam"
    AMAZON_REFUND = "amazon_refund_scam"
    ROMANCE = "romance_pig_butchering"
    IMMIGRATION = "immigration_scam"
    SHERIFF = "sheriff_impersonation"
    BITCOIN_ATM = "bitcoin_atm_deposit_scam"
    UNKNOWN = "unknown"


class LocationType(str, Enum):
    BITCOIN_ATM = "bitcoin_atm"
    MONEYGRAM = "moneygram"
    WESTERN_UNION = "western_union"
    GIFT_CARD = "gift_card_aisle"
    COINSTAR = "coinstar"
    HIGH_RISK_STORE = "high_risk_store"


class SubscriptionTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium_shield"
    ULTRA = "guardian_ultra"
    ENTERPRISE = "enterprise"


class User(BaseModel):
    user_id: str
    name: str
    phone_number: str
    device_id: str
    trusted_contacts: List[Dict[str, str]] = []
    settings: Dict[str, Any] = {}
    created_at: datetime = datetime.now()
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    subscription_expiration: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    family_members: List[Dict[str, Any]] = []
    agency_id: Optional[str] = None
    agency_portal_access: bool = False
    agency_license_count: int = 0


class CallEvent(BaseModel):
    call_id: str
    user_id: str
    timestamp_start: datetime
    timestamp_end: Optional[datetime] = None
    audio_text: str = ""
    scam_probability: float = 0.0
    emotional_score: float = 0.0
    scam_script_type: Optional[ScamScriptType] = None
    intervention_triggered: bool = False
    location_trace: List[Dict[str, Any]] = []
    manipulation_index: float = 0.0
    urgency_score: float = 0.0


class WalletCheck(BaseModel):
    check_id: str
    user_id: str
    wallet_address: str
    risk_score: float
    lineage_map: Dict[str, Any] = {}
    risk_category: RiskLevel
    known_scams: List[Dict[str, Any]] = []
    checked_at: datetime = datetime.now()


class GPSAlert(BaseModel):
    gps_id: str
    user_id: str
    latitude: float
    longitude: float
    matched_location_type: Optional[LocationType] = None
    risk_level: RiskLevel
    action_taken: str = ""
    created_at: datetime = datetime.now()


class FamilyAlert(BaseModel):
    alert_id: str
    user_id: str
    contact_id: str
    event_type: str
    action_taken: str = ""
    created_at: datetime = datetime.now()


class Report(BaseModel):
    report_id: str
    user_id: str
    call_id: Optional[str] = None
    wallet_id: Optional[str] = None
    emotional_graph: Dict[str, Any] = {}
    scam_script_detected: Optional[ScamScriptType] = None
    pdf_url: str = ""
    created_at: datetime = datetime.now()


class VoiceAnalysisRequest(BaseModel):
    call_id: str
    user_id: str
    audio_text: str


class VoiceAnalysisResponse(BaseModel):
    scam_probability: float
    manipulation_intensity: float
    script_classification: Optional[ScamScriptType]
    urgency_score: float
    threat_detected: bool
    manipulation_patterns: List[str]


class EmotionalAnalysisRequest(BaseModel):
    call_id: str
    user_id: str
    audio_text: str
    tone_features: Optional[Dict[str, Any]] = None


class EmotionalAnalysisResponse(BaseModel):
    stress_level: float
    confusion_level: float
    fear_level: float
    compliance_probability: float
    tone_instability: float
    victim_vulnerability: float
    manipulation_index: float


class WalletRiskRequest(BaseModel):
    wallet_address: str
    user_id: str


class WalletRiskResponse(BaseModel):
    risk_score: float
    risk_category: RiskLevel
    risk_lineage_map: Dict[str, Any]
    known_scam_flags: List[str]
    mixer_detected: bool
    darknet_crossing: bool


class GPSCheckRequest(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    call_id: Optional[str] = None


class GPSCheckResponse(BaseModel):
    risk_detected: bool
    location_type: Optional[LocationType]
    risk_level: RiskLevel
    alert_message: str
    distance_to_risk: float


class InterventionRequest(BaseModel):
    call_id: str
    user_id: str
    scam_probability: float
    manipulation_index: float


class InterventionResponse(BaseModel):
    intervention_triggered: bool
    actions: List[str]
    alert_level: RiskLevel
    family_notified: bool


class ReportGenerationRequest(BaseModel):
    user_id: str
    call_id: Optional[str] = None
    wallet_id: Optional[str] = None
    include_transcript: bool = True
    include_gps: bool = True
    include_emotional: bool = True


class SubscriptionCheckRequest(BaseModel):
    user_id: str
    feature: str


class SubscriptionCheckResponse(BaseModel):
    has_access: bool
    current_tier: SubscriptionTier
    required_tier: Optional[SubscriptionTier] = None
    upgrade_message: Optional[str] = None


class CreateSubscriptionRequest(BaseModel):
    user_id: str
    tier: SubscriptionTier
    stripe_token: Optional[str] = None


class CreateSubscriptionResponse(BaseModel):
    success: bool
    subscription_id: Optional[str] = None
    customer_id: Optional[str] = None
    message: str


class CancelSubscriptionRequest(BaseModel):
    user_id: str


class CancelSubscriptionResponse(BaseModel):
    success: bool
    message: str

class AnalyzeTextRequest(BaseModel):
    call_id: Optional[str] = None
    user_id: Optional[str] = None
    text: Optional[str] = None
    audio_text: Optional[str] = None

class AnalyzeTextResponse(BaseModel):
    scam_probability: float
    emotional_tone: dict
    manipulation_timeline: list
    dark_patterns: list
    predicted_region: str
    threat_level: str
    scammer_profile: dict
    suggested_action: str
    raw: dict
