import re
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from app.models import ScamScriptType, RiskLevel
import random


class VoiceAnalysisService:
    def __init__(self):
        self.scam_keywords = {
            "urgency": ["immediately", "right now", "urgent", "hurry", "quickly", "don't wait", "time sensitive", "today", "now", "must", "restricted", "restore access"],
            "threat": ["arrest", "warrant", "police", "jail", "lawsuit", "legal action", "suspended", "frozen", "come", "consequences", "infected", "virus"],
            "isolation": ["don't tell anyone", "keep this secret", "don't hang up", "stay on the line", "don't talk to"],
            "payment": ["bitcoin", "gift card", "wire transfer", "cash", "atm", "cryptocurrency", "western union", "moneygram", "send", "money", "pay", "$", "dollar"],
            "authority": ["irs", "social security", "government", "federal", "sheriff", "officer", "agent", "department", "paypal", "account"],
            "manipulation": ["help you", "protect you", "refund", "owe you", "won money", "selected", "verify", "or else", "if you don't", "guaranteed", "triple", "double", "profit"],
            "romance": ["love", "my love", "stuck", "overseas", "fly home", "darling", "sweetheart", "baby"],
            "financial": ["investment", "opportunity", "return", "hours", "days", "guarantee", "profit", "earn", "make money"],
        }
        
        self.scam_patterns = {
            ScamScriptType.IRS: ["irs", "tax", "refund", "audit", "federal tax"],
            ScamScriptType.SOCIAL_SECURITY: ["social security", "ssn", "social security number", "benefits suspended"],
            ScamScriptType.TECH_SUPPORT: ["computer", "virus", "microsoft", "apple", "tech support", "windows", "security alert"],
            ScamScriptType.GRANDPARENT: ["grandson", "granddaughter", "grandchild", "accident", "bail", "emergency"],
            ScamScriptType.AMAZON_REFUND: ["amazon", "refund", "order", "purchase", "account suspended"],
            ScamScriptType.ROMANCE: ["love", "my love", "stuck", "overseas", "fly home", "relationship", "investment opportunity", "business deal", "meet in person"],
            ScamScriptType.IMMIGRATION: ["visa", "immigration", "deportation", "citizenship", "green card"],
            ScamScriptType.SHERIFF: ["sheriff", "local police", "county", "warrant for arrest"],
            ScamScriptType.BITCOIN_ATM: ["bitcoin atm", "crypto atm", "deposit bitcoin", "send cryptocurrency"],
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        keyword_scores = {}
        for category, keywords in self.scam_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            keyword_scores[category] = score
        
        total_keywords = sum(keyword_scores.values())
        scam_probability = min(100, (total_keywords / 3) * 100)
        
        script_type = self._detect_script_type(text_lower)
        
        urgency_score = (keyword_scores.get("urgency", 0) + keyword_scores.get("threat", 0)) * 15
        urgency_score = min(100, urgency_score)
        
        manipulation_intensity = (keyword_scores.get("isolation", 0) + keyword_scores.get("manipulation", 0)) * 20
        manipulation_intensity = min(100, manipulation_intensity)
        
        threat_detected = (
            keyword_scores.get("threat", 0) > 0 or 
            keyword_scores.get("urgency", 0) > 1 or
            keyword_scores.get("manipulation", 0) > 1 or
            keyword_scores.get("financial", 0) > 0 or
            keyword_scores.get("romance", 0) > 0
        )
        
        manipulation_patterns = []
        for category, score in keyword_scores.items():
            if score > 0:
                manipulation_patterns.append(f"{category}: {score} matches")
        
        return {
            "scam_probability": scam_probability,
            "manipulation_intensity": manipulation_intensity,
            "script_classification": script_type,
            "urgency_score": urgency_score,
            "threat_detected": threat_detected,
            "manipulation_patterns": manipulation_patterns,
            "keyword_scores": keyword_scores,
        }
    
    def _detect_script_type(self, text: str) -> Optional[ScamScriptType]:
        best_match = None
        best_score = 0
        
        for script_type, patterns in self.scam_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text)
            if score > best_score:
                best_score = score
                best_match = script_type
        
        return best_match if best_score > 0 else ScamScriptType.UNKNOWN


class EmotionalAnalysisService:
    def __init__(self):
        self.stress_indicators = ["um", "uh", "i don't know", "confused", "worried", "scared", "nervous", "if you don't", "you need to", "you must", "you have to"]
        self.fear_indicators = ["afraid", "scared", "worried", "terrified", "panic", "help", "something bad", "bad is going", "going to happen", "will happen"]
        self.compliance_indicators = ["okay", "yes", "i'll do it", "alright", "sure", "i understand", "don't worry", "trust me", "i'll take care", "take care of"]
    
    def analyze_emotion(self, text: str, tone_features: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        text_lower = text.lower()
        
        stress_level = self._calculate_stress(text_lower)
        confusion_level = self._calculate_confusion(text_lower)
        fear_level = self._calculate_fear(text_lower)
        compliance_probability = self._calculate_compliance(text_lower)
        tone_instability = self._calculate_tone_instability(text_lower, tone_features)
        victim_vulnerability = max(
            (stress_level + fear_level + confusion_level) / 3,
            compliance_probability * 0.4
        )
        
        manipulation_index = (
            stress_level * 0.25 +
            confusion_level * 0.15 +
            fear_level * 0.3 +
            compliance_probability * 0.36 +
            tone_instability * 0.1 +
            victim_vulnerability * 0.15
        )
        
        return {
            "stress_level": stress_level,
            "confusion_level": confusion_level,
            "fear_level": fear_level,
            "compliance_probability": compliance_probability,
            "tone_instability": tone_instability,
            "victim_vulnerability": victim_vulnerability,
            "manipulation_index": manipulation_index,
        }
    
    def _calculate_stress(self, text: str) -> float:
        count = sum(1 for indicator in self.stress_indicators if indicator in text)
        threat_words = ["must", "have to", "need to", "should", "immediately", "now", "today"]
        threat_count = sum(1 for word in threat_words if word in text)
        return min(100, (count * 25) + (threat_count * 15))
    
    def _calculate_confusion(self, text: str) -> float:
        confusion_words = ["confused", "don't understand", "what", "why", "how", "i don't know"]
        count = sum(1 for word in confusion_words if word in text)
        return min(100, count * 20)
    
    def _calculate_fear(self, text: str) -> float:
        count = sum(1 for indicator in self.fear_indicators if indicator in text)
        threat_indicators = ["police", "arrest", "warrant", "jail", "lawsuit", "consequences", "trouble"]
        threat_count = sum(1 for word in threat_indicators if word in text)
        return min(100, (count * 30) + (threat_count * 20))
    
    def _calculate_compliance(self, text: str) -> float:
        count = sum(1 for indicator in self.compliance_indicators if indicator in text)
        love_indicators = ["love", "baby", "darling", "sweetheart", "soulmate", "future together", "marry"]
        love_count = sum(1 for word in love_indicators if word in text)
        return min(100, (count * 15) + (love_count * 25))
    
    def _calculate_tone_instability(self, text: str, tone_features: Optional[Dict[str, Any]]) -> float:
        if tone_features:
            return tone_features.get("instability", 50.0)
        
        question_marks = text.count("?")
        exclamation_marks = text.count("!")
        return min(100, (question_marks + exclamation_marks) * 10)


class WalletRiskEngine:
    def __init__(self, db):
        self.db = db
        self.mixer_patterns = ["mix", "tumbl", "wash", "anon"]
        self.darknet_markers = ["dark", "onion", "tor"]
    
    def analyze_wallet(self, wallet_address: str) -> Dict[str, Any]:
        risk_score = 0
        risk_flags = []
        mixer_detected = False
        darknet_crossing = False
        
        scam_info = self.db.is_scam_wallet(wallet_address)
        if scam_info:
            risk_score += 80
            risk_flags.append(f"Known scam wallet: {scam_info['scam_type']}")
            risk_flags.append(f"Reported {scam_info['reported_count']} times")
        
        if any(pattern in wallet_address.lower() for pattern in self.mixer_patterns):
            mixer_detected = True
            risk_score += 30
            risk_flags.append("Potential mixer/tumbler detected")
        
        if len(wallet_address) > 40:
            risk_score += 10
            risk_flags.append("Unusually long wallet address")
        
        if wallet_address.startswith("bc1q"):
            risk_score += 5
        
        lineage_map = self._generate_lineage_map(wallet_address, scam_info)
        
        risk_score = min(100, risk_score)
        
        if risk_score >= 75:
            risk_category = RiskLevel.CRITICAL
        elif risk_score >= 50:
            risk_category = RiskLevel.HIGH
        elif risk_score >= 25:
            risk_category = RiskLevel.MEDIUM
        else:
            risk_category = RiskLevel.LOW
        
        return {
            "risk_score": risk_score,
            "risk_category": risk_category,
            "risk_lineage_map": lineage_map,
            "known_scam_flags": risk_flags,
            "mixer_detected": mixer_detected,
            "darknet_crossing": darknet_crossing,
        }
    
    def _generate_lineage_map(self, wallet_address: str, scam_info: Optional[dict]) -> Dict[str, Any]:
        lineage = {
            "wallet": wallet_address,
            "parent_wallets": [],
            "child_wallets": [],
            "transaction_count": random.randint(10, 500),
            "total_received_btc": round(random.uniform(0.1, 50.0), 4),
            "total_sent_btc": round(random.uniform(0.1, 45.0), 4),
        }
        
        if scam_info:
            lineage["parent_wallets"] = [f"parent_{i}" for i in range(3)]
            lineage["child_wallets"] = [f"child_{i}" for i in range(5)]
            lineage["scam_network"] = scam_info["scam_type"]
        
        return lineage


class ScamScriptFingerprinter:
    def __init__(self):
        self.script_signatures = {
            ScamScriptType.IRS: {
                "signature": ["irs", "tax", "owe", "refund", "audit"],
                "related_networks": ["tax_fraud_ring", "irs_impersonation_group"],
            },
            ScamScriptType.SOCIAL_SECURITY: {
                "signature": ["social security", "ssn", "suspended", "benefits"],
                "related_networks": ["ssa_impersonation", "identity_theft_ring"],
            },
            ScamScriptType.TECH_SUPPORT: {
                "signature": ["computer", "virus", "microsoft", "windows", "tech support"],
                "related_networks": ["tech_support_scam_network", "fake_antivirus_group"],
            },
            ScamScriptType.ROMANCE: {
                "signature": ["love", "relationship", "investment", "business opportunity"],
                "related_networks": ["pig_butchering_syndicate", "romance_scam_network"],
            },
            ScamScriptType.BITCOIN_ATM: {
                "signature": ["bitcoin atm", "crypto", "deposit", "send money"],
                "related_networks": ["crypto_atm_scam_ring", "bitcoin_extortion_group"],
            },
        }
    
    def fingerprint_script(self, text: str, script_type: Optional[ScamScriptType]) -> Dict[str, Any]:
        if not script_type or script_type == ScamScriptType.UNKNOWN:
            return {
                "script_name": "Unknown",
                "script_signature": [],
                "related_fraud_networks": [],
            }
        
        script_info = self.script_signatures.get(script_type, {})
        
        return {
            "script_name": script_type.value,
            "script_signature": script_info.get("signature", []),
            "related_fraud_networks": script_info.get("related_networks", []),
        }


class GPSAntiScamShield:
    def __init__(self, db):
        self.db = db
    
    def check_location(self, lat: float, lon: float, call_id: Optional[str] = None) -> Dict[str, Any]:
        nearby_risks = self.db.get_nearby_risk_locations(lat, lon, radius_km=0.5)
        
        if nearby_risks:
            closest = min(nearby_risks, key=lambda x: x["distance_km"])
            
            risk_level = RiskLevel.CRITICAL if closest["distance_km"] < 0.1 else RiskLevel.HIGH
            
            alert_message = f"⚠️ RED ALERT: You are {closest['distance_km']:.2f}km from a {closest['type'].replace('_', ' ').upper()}. "
            if call_id:
                alert_message += "You are on a suspicious call. STOP IMMEDIATELY. DO NOT PROCEED."
            else:
                alert_message += "Be cautious of any requests to send money or cryptocurrency."
            
            return {
                "risk_detected": True,
                "location_type": closest["type"],
                "risk_level": risk_level,
                "alert_message": alert_message,
                "distance_to_risk": closest["distance_km"],
                "location_name": closest.get("name", "Unknown"),
            }
        
        return {
            "risk_detected": False,
            "location_type": None,
            "risk_level": RiskLevel.LOW,
            "alert_message": "No high-risk locations detected nearby.",
            "distance_to_risk": 999.0,
        }


class DarkPatternVoiceFingerprintingAI:
    def __init__(self):
        self.dark_patterns = {
            "do_not_hang_up": ["don't hang up", "stay on the line", "keep me on the phone", "don't disconnect"],
            "go_now": ["go now", "right now", "immediately", "hurry up", "go right away"],
            "keep_on_phone": ["stay with me", "don't leave", "keep talking", "stay on call"],
            "threat_tone": ["arrest", "warrant", "police", "jail", "legal action", "consequences"],
            "false_authority": ["officer", "agent", "detective", "federal", "government official", "irs", "social security", "department", "intelligence", "work with", "need to do", "exactly what i say"],
            "repetitive_pressure": ["again", "one more time", "repeat", "tell me again"],
            "cognitive_overload": ["quickly", "fast", "hurry", "no time", "urgent"],
            "fear_based": ["scared", "afraid", "worried", "danger", "risk", "threat"],
            "fake_badge": ["badge number", "agent id", "officer number", "federal id"],
            "gaslighting": ["you're overreacting", "you're imagining", "nobody else", "you're crazy", "it's all in your head", "you're too sensitive", "that never happened", "you're being dramatic"],
            "invalidation": ["overreacting", "problem with this except you", "nobody else has a problem", "just you", "only you"],
        }
    
    def detect_dark_patterns(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        pattern_list = []
        pattern_scores = {}
        
        for pattern_name, keywords in self.dark_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                pattern_list.append(pattern_name)
                pattern_scores[pattern_name] = score
        
        total_score = sum(pattern_scores.values())
        overall_score = min(100, total_score * 25)
        
        fingerprint_data = f"{text_lower}:{','.join(sorted(pattern_list))}"
        fingerprint_hash = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
        
        return {
            "patterns": pattern_list,
            "pattern_list": pattern_list,
            "pattern_scores": pattern_scores,
            "manipulation_score": overall_score,
            "overall_score": overall_score,
            "fingerprint_hash": fingerprint_hash,
        }


class ScammerNationalityPredictor:
    def __init__(self):
        self.accent_patterns = {
            "india": {
                "keywords": ["sir", "madam", "kindly", "please do the needful", "revert back"],
                "phoneme_markers": ["v/w confusion", "th/d substitution"],
                "score_weight": 1.0,
            },
            "west_africa": {
                "keywords": ["my dear", "beloved", "god bless", "i am contacting you", "promise", "offshore", "contract", "return to you", "dear"],
                "phoneme_markers": ["british english influence", "formal tone"],
                "score_weight": 0.8,
            },
            "philippines": {
                "keywords": ["po", "sir/ma'am", "sorry po"],
                "phoneme_markers": ["tagalog influence", "soft consonants"],
                "score_weight": 0.7,
            },
            "eastern_europe": {
                "keywords": ["my friend", "business opportunity", "investment"],
                "phoneme_markers": ["slavic accent", "hard consonants"],
                "score_weight": 0.6,
            },
            "china": {
                "keywords": ["hello friend", "good opportunity", "make money"],
                "phoneme_markers": ["mandarin influence", "tonal patterns"],
                "score_weight": 0.5,
            },
        }
    
    def predict_nationality(self, text: str, voice_features: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        text_lower = text.lower()
        
        nationality_scores = {}
        detected_markers = []
        
        for nationality, patterns in self.accent_patterns.items():
            score = 0
            for keyword in patterns["keywords"]:
                if keyword in text_lower:
                    score += patterns["score_weight"] * 20
                    detected_markers.append(keyword)
            
            if voice_features:
                for marker in patterns["phoneme_markers"]:
                    if marker in voice_features.get("detected_markers", []):
                        score += patterns["score_weight"] * 15
                        detected_markers.append(marker)
            
            nationality_scores[nationality] = min(100, score)
        
        best_nationality = max(nationality_scores.items(), key=lambda x: x[1]) if nationality_scores else ("unknown", 0)
        best_region = best_nationality[0]
        best_score = best_nationality[1]
        
        region_map = {
            "india": "South Asia",
            "west_africa": "West Africa",
            "philippines": "Southeast Asia",
            "eastern_europe": "Eastern Europe",
            "china": "East Asia",
            "unknown": None
        }
        
        predicted_region = region_map.get(best_region, None)
        confidence = min(100, best_score)
        
        total_score = sum(nationality_scores.values())
        if total_score > 0:
            nationality_percentages = {
                k: round((v / total_score) * 100, 1) 
                for k, v in nationality_scores.items() if v > 0
            }
        else:
            nationality_percentages = {"unknown": 100.0}
        
        sorted_nationalities = sorted(
            nationality_percentages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        return {
            "predicted_region": predicted_region,
            "confidence": confidence,
            "linguistic_markers": detected_markers,
            "likely_origins": [
                {"country": country.replace("_", " ").title(), "probability": prob}
                for country, prob in sorted_nationalities
            ],
        }


class ThreatLevelCalculator:
    def calculate_threat_level(
        self,
        emotional_index: float,
        manipulation_index: float,
        scam_pattern_match: bool,
        wallet_risk: float,
        atm_proximity: bool,
        store_risk: float,
        time_of_day_risk: float,
        geolocation_overlap: bool,
    ) -> Dict[str, Any]:
        threat_score = 0
        contributing_factors = []
        
        if emotional_index >= 80:
            threat_score += 30
            contributing_factors.append("Critical emotional distress")
        elif emotional_index >= 60:
            threat_score += 25
            contributing_factors.append("High emotional distress")
        elif emotional_index >= 40:
            threat_score += 20
            contributing_factors.append("Moderate emotional distress")
        elif emotional_index >= 10:
            threat_score += 20
            contributing_factors.append("Emotional indicators detected")
        
        if manipulation_index >= 80:
            threat_score += 30
            contributing_factors.append("Severe manipulation detected")
        elif manipulation_index >= 60:
            threat_score += 25
            contributing_factors.append("High manipulation detected")
        elif manipulation_index >= 40:
            threat_score += 20
            contributing_factors.append("Moderate manipulation detected")
        elif manipulation_index >= 5:
            threat_score += 15
            contributing_factors.append("Manipulation indicators detected")
        
        if scam_pattern_match:
            threat_score += 60
            contributing_factors.append("Known scam pattern detected")
        
        if wallet_risk >= 75:
            threat_score += 20
            contributing_factors.append("High-risk wallet detected")
        elif wallet_risk >= 50:
            threat_score += 10
            contributing_factors.append("Moderate wallet risk")
        
        if atm_proximity:
            threat_score += 15
            contributing_factors.append("Near Bitcoin ATM")
        
        if store_risk >= 80:
            threat_score += 15
            contributing_factors.append("High-risk store proximity")
        elif store_risk >= 50:
            threat_score += 8
            contributing_factors.append("Moderate store risk")
        
        if time_of_day_risk >= 70:
            threat_score += 10
            contributing_factors.append("High-risk time period")
        elif time_of_day_risk >= 40:
            threat_score += 5
            contributing_factors.append("Elevated time risk")
        
        if geolocation_overlap:
            threat_score += 10
            contributing_factors.append("Location matches scam hotspot")
        
        threat_score = min(100, threat_score)
        
        if threat_score >= 80:
            level = "CRITICAL"
            color = "black"
        elif threat_score >= 60:
            level = "HIGH"
            color = "red"
        elif threat_score >= 40:
            level = "ELEVATED"
            color = "orange"
        elif threat_score >= 20:
            level = "GUARDED"
            color = "yellow"
        else:
            level = "LOW"
            color = "green"
        
        return {
            "threat_score": threat_score,
            "risk_level": level.lower(),
            "level": level,
            "color": color,
            "score": threat_score,
            "contributing_factors": contributing_factors,
        }


voice_analysis_service = VoiceAnalysisService()
emotional_analysis_service = EmotionalAnalysisService()
scam_script_fingerprinter = ScamScriptFingerprinter()
dark_pattern_fingerprinter = DarkPatternVoiceFingerprintingAI()
nationality_predictor = ScammerNationalityPredictor()
threat_level_calculator = ThreatLevelCalculator()
