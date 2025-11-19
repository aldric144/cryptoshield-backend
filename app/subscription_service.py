from typing import Dict, Optional
from datetime import datetime, timedelta
from app.models import SubscriptionTier, User


class SubscriptionService:
    """Service for managing subscription tiers and feature access control"""
    
    FEATURE_ACCESS = {
        "basic_scam_detection": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "wallet_risk_single": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "gps_fraud_warnings": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "address_lookup": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "manual_freeze_mode": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "case_report_limited": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "community_alerts": [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        
        "realtime_voice_protection": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "emotional_manipulation_ai": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "auto_freeze_mode": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "unlimited_wallet_scanning": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "mixer_detection": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "wallet_lineage": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "unlimited_pdf_exports": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "case_timeline": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "scammer_profile_builder": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "family_safety_center": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "travel_mode": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "crisis_response_bot": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "threat_meter": [SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        
        "scammer_network_intelligence": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "voice_lineup_identification": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "dark_web_monitoring": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "ultra_travel_mode": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "international_hotzone_map": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        "priority_law_enforcement": [SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE],
        
        "multi_case_linking": [SubscriptionTier.ENTERPRISE],
        "agency_dashboards": [SubscriptionTier.ENTERPRISE],
        "unlimited_devices": [SubscriptionTier.ENTERPRISE],
        "agency_portal": [SubscriptionTier.ENTERPRISE],
        "forensic_export_bundles": [SubscriptionTier.ENTERPRISE],
        "realtime_analytics_feed": [SubscriptionTier.ENTERPRISE],
        "police_case_integration": [SubscriptionTier.ENTERPRISE],
    }
    
    FAMILY_LIMITS = {
        SubscriptionTier.FREE: 1,
        SubscriptionTier.PREMIUM: 3,
        SubscriptionTier.ULTRA: 10,
        SubscriptionTier.ENTERPRISE: 999,
    }
    
    PDF_LIMITS = {
        SubscriptionTier.FREE: 1,
        SubscriptionTier.PREMIUM: 999,
        SubscriptionTier.ULTRA: 999,
        SubscriptionTier.ENTERPRISE: 999,
    }
    
    @staticmethod
    def check_feature_access(user: User, feature: str) -> bool:
        """Check if user has access to a specific feature"""
        if user.subscription_expiration and user.subscription_expiration < datetime.now():
            grace_period_end = user.subscription_expiration + timedelta(days=3)
            if datetime.now() > grace_period_end:
                user.subscription_tier = SubscriptionTier.FREE
        
        allowed_tiers = SubscriptionService.FEATURE_ACCESS.get(feature, [])
        return user.subscription_tier in allowed_tiers
    
    @staticmethod
    def get_required_tier(feature: str) -> Optional[SubscriptionTier]:
        """Get the minimum required tier for a feature"""
        allowed_tiers = SubscriptionService.FEATURE_ACCESS.get(feature, [])
        if not allowed_tiers:
            return None
        
        tier_order = [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE]
        for tier in tier_order:
            if tier in allowed_tiers:
                return tier
        return None
    
    @staticmethod
    def get_upgrade_message(feature: str, current_tier: SubscriptionTier) -> str:
        """Get upgrade message for a feature"""
        required_tier = SubscriptionService.get_required_tier(feature)
        
        if required_tier == SubscriptionTier.PREMIUM:
            return "This feature requires Premium Shield ($9.99/month). Upgrade now to unlock real-time scam protection!"
        elif required_tier == SubscriptionTier.ULTRA:
            return "This feature requires Guardian Ultra ($19.99/month). Upgrade now for maximum family protection!"
        elif required_tier == SubscriptionTier.ENTERPRISE:
            return "This feature requires Enterprise subscription. Contact us for custom pricing."
        else:
            return "This feature is not available in your current plan."
    
    @staticmethod
    def check_family_limit(user: User) -> bool:
        """Check if user can add more family members"""
        limit = SubscriptionService.FAMILY_LIMITS.get(user.subscription_tier, 1)
        return len(user.family_members) < limit
    
    @staticmethod
    def get_family_limit(tier: SubscriptionTier) -> int:
        """Get family member limit for a tier"""
        return SubscriptionService.FAMILY_LIMITS.get(tier, 1)
    
    @staticmethod
    def check_pdf_export_limit(user: User, exports_this_month: int) -> bool:
        """Check if user can export more PDFs this month"""
        limit = SubscriptionService.PDF_LIMITS.get(user.subscription_tier, 1)
        return exports_this_month < limit
    
    @staticmethod
    def get_tier_features(tier: SubscriptionTier) -> Dict[str, bool]:
        """Get all features available for a tier"""
        features = {}
        for feature, allowed_tiers in SubscriptionService.FEATURE_ACCESS.items():
            features[feature] = tier in allowed_tiers
        return features
    
    @staticmethod
    def get_tier_price(tier: SubscriptionTier) -> Optional[float]:
        """Get monthly price for a tier"""
        prices = {
            SubscriptionTier.FREE: 0.0,
            SubscriptionTier.PREMIUM: 9.99,
            SubscriptionTier.ULTRA: 19.99,
            SubscriptionTier.ENTERPRISE: None,  # Custom pricing
        }
        return prices.get(tier)
    
    @staticmethod
    def get_tier_name(tier: SubscriptionTier) -> str:
        """Get display name for a tier"""
        names = {
            SubscriptionTier.FREE: "Free",
            SubscriptionTier.PREMIUM: "Premium Shield",
            SubscriptionTier.ULTRA: "Guardian Ultra",
            SubscriptionTier.ENTERPRISE: "Enterprise",
        }
        return names.get(tier, "Unknown")


subscription_service = SubscriptionService()
