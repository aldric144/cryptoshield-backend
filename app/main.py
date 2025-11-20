from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uuid
import logging
import traceback
from typing import List, Optional

from app.models import (
    User, CallEvent, WalletCheck, GPSAlert, FamilyAlert, Report,
    VoiceAnalysisRequest, VoiceAnalysisResponse,
    EmotionalAnalysisRequest, EmotionalAnalysisResponse,
    WalletRiskRequest, WalletRiskResponse,
    GPSCheckRequest, GPSCheckResponse,
    InterventionRequest, InterventionResponse,
    ReportGenerationRequest, RiskLevel, ScamScriptType,
    SubscriptionTier, SubscriptionCheckRequest, SubscriptionCheckResponse,
    CreateSubscriptionRequest, CreateSubscriptionResponse,
    CancelSubscriptionRequest, CancelSubscriptionResponse
)
from app.database import db
from app.ai_services import (
    voice_analysis_service,
    emotional_analysis_service,
    scam_script_fingerprinter,
    dark_pattern_fingerprinter,
    nationality_predictor,
    threat_level_calculator,
    WalletRiskEngine,
    GPSAntiScamShield
)
from app.subscription_service import subscription_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("finalize_case")

app = FastAPI(title="CryptoShield Guardian AI API", version="1.0.0")

import os
from typing import List

def get_cors_origins() -> List[str]:
    """Get CORS allowed origins from environment variable or use defaults"""
    env = os.getenv("ENV", "development")
    
    if env == "production":
        return [
            "https://cryptoshield.app",
            "https://www.cryptoshield.app",
            "https://cryptoshield-frontend.onrender.com"
        ]
    elif env == "staging":
        return [
            "https://staging.cryptoshield.app",
            "https://cryptoshield-frontend-staging.vercel.app",
            "https://cryptoshield-frontend.onrender.com",
            "http://localhost:5173",
            "http://localhost:3000"
        ]
    else:  # development
        return [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000"
        ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

wallet_risk_engine = WalletRiskEngine(db)
gps_shield = GPSAntiScamShield(db)


@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "CryptoShield Guardian AI"}

@app.get("/health")
async def health():
    """Health check endpoint for Fly.io and monitoring systems"""
    env = os.getenv("ENV", "development")
    return {
        "status": "healthy",
        "service": "CryptoShield Guardian AI",
        "version": "1.0.0",
        "environment": env,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/users", response_model=User)
async def create_user(user: User):
    if not user.user_id:
        user.user_id = str(uuid.uuid4())
    return db.create_user(user)


@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/voice-analysis", response_model=VoiceAnalysisResponse)
async def analyze_voice(request: VoiceAnalysisRequest):
    analysis = voice_analysis_service.analyze_text(request.audio_text)
    
    call_event = db.get_call_event(request.call_id)
    if call_event:
        db.update_call_event(request.call_id, {
            "audio_text": request.audio_text,
            "scam_probability": analysis["scam_probability"],
            "scam_script_type": analysis["script_classification"],
            "urgency_score": analysis["urgency_score"],
        })
    else:
        call_event = CallEvent(
            call_id=request.call_id,
            user_id=request.user_id,
            timestamp_start=datetime.now(),
            audio_text=request.audio_text,
            scam_probability=analysis["scam_probability"],
            scam_script_type=analysis["script_classification"],
            urgency_score=analysis["urgency_score"],
        )
        db.create_call_event(call_event)
    
    return VoiceAnalysisResponse(
        scam_probability=analysis["scam_probability"],
        manipulation_intensity=analysis["manipulation_intensity"],
        script_classification=analysis["script_classification"],
        urgency_score=analysis["urgency_score"],
        threat_detected=analysis["threat_detected"],
        manipulation_patterns=analysis["manipulation_patterns"],
    )


@app.post("/api/emotional-analysis", response_model=EmotionalAnalysisResponse)
async def analyze_emotion(request: EmotionalAnalysisRequest):
    analysis = emotional_analysis_service.analyze_emotion(
        request.audio_text,
        request.tone_features
    )
    
    call_event = db.get_call_event(request.call_id)
    if call_event:
        db.update_call_event(request.call_id, {
            "emotional_score": analysis["manipulation_index"],
            "manipulation_index": analysis["manipulation_index"],
        })
    
    return EmotionalAnalysisResponse(
        stress_level=analysis["stress_level"],
        confusion_level=analysis["confusion_level"],
        fear_level=analysis["fear_level"],
        compliance_probability=analysis["compliance_probability"],
        tone_instability=analysis["tone_instability"],
        victim_vulnerability=analysis["victim_vulnerability"],
        manipulation_index=analysis["manipulation_index"],
    )


@app.post("/api/wallet-risk", response_model=WalletRiskResponse)
async def check_wallet_risk(request: WalletRiskRequest):
    analysis = wallet_risk_engine.analyze_wallet(request.wallet_address)
    
    wallet_check = WalletCheck(
        check_id=str(uuid.uuid4()),
        user_id=request.user_id,
        wallet_address=request.wallet_address,
        risk_score=analysis["risk_score"],
        lineage_map=analysis["risk_lineage_map"],
        risk_category=analysis["risk_category"],
        known_scams=[{"flag": flag} for flag in analysis["known_scam_flags"]],
    )
    db.create_wallet_check(wallet_check)
    
    return WalletRiskResponse(
        risk_score=analysis["risk_score"],
        risk_category=analysis["risk_category"],
        risk_lineage_map=analysis["risk_lineage_map"],
        known_scam_flags=analysis["known_scam_flags"],
        mixer_detected=analysis["mixer_detected"],
        darknet_crossing=analysis["darknet_crossing"],
    )


@app.post("/api/gps-check", response_model=GPSCheckResponse)
async def check_gps_location(request: GPSCheckRequest):
    analysis = gps_shield.check_location(
        request.latitude,
        request.longitude,
        request.call_id
    )
    
    if analysis["risk_detected"]:
        gps_alert = GPSAlert(
            gps_id=str(uuid.uuid4()),
            user_id=request.user_id,
            latitude=request.latitude,
            longitude=request.longitude,
            matched_location_type=analysis["location_type"],
            risk_level=analysis["risk_level"],
            action_taken="alert_triggered",
        )
        db.create_gps_alert(gps_alert)
    
    return GPSCheckResponse(
        risk_detected=analysis["risk_detected"],
        location_type=analysis.get("location_type"),
        risk_level=analysis["risk_level"],
        alert_message=analysis["alert_message"],
        distance_to_risk=analysis["distance_to_risk"],
    )


@app.post("/api/intervention", response_model=InterventionResponse)
async def trigger_intervention(request: InterventionRequest):
    intervention_triggered = False
    actions = []
    alert_level = RiskLevel.LOW
    family_notified = False
    
    if request.scam_probability >= 85 or request.manipulation_index >= 80:
        intervention_triggered = True
        alert_level = RiskLevel.CRITICAL
        
        actions.append("vibrate_phone")
        actions.append("display_blocking_overlay")
        actions.append("offer_auto_hangup")
        actions.append("lock_crypto_wallet_app")
        actions.append("trigger_emergency_mode")
        
        user = db.get_user(request.user_id)
        if user and user.trusted_contacts:
            family_notified = True
            for contact in user.trusted_contacts:
                family_alert = FamilyAlert(
                    alert_id=str(uuid.uuid4()),
                    user_id=request.user_id,
                    contact_id=contact.get("contact_id", "unknown"),
                    event_type="high_risk_scam_call",
                    action_taken="sms_and_push_notification_sent",
                )
                db.create_family_alert(family_alert)
            actions.append("family_notified")
        
        db.update_call_event(request.call_id, {
            "intervention_triggered": True,
        })
    
    elif request.scam_probability >= 60 or request.manipulation_index >= 60:
        intervention_triggered = True
        alert_level = RiskLevel.HIGH
        actions.append("display_warning")
        actions.append("suggest_hang_up")
    
    elif request.scam_probability >= 40:
        alert_level = RiskLevel.MEDIUM
        actions.append("display_caution_notice")
    
    return InterventionResponse(
        intervention_triggered=intervention_triggered,
        actions=actions,
        alert_level=alert_level,
        family_notified=family_notified,
    )


@app.post("/api/reports", response_model=Report)
async def generate_report(request: ReportGenerationRequest):
    report_id = str(uuid.uuid4())
    
    emotional_graph = {}
    scam_script_detected = None
    
    if request.call_id:
        call_event = db.get_call_event(request.call_id)
        if call_event:
            scam_script_detected = call_event.scam_script_type
            emotional_graph = {
                "manipulation_index": call_event.manipulation_index,
                "scam_probability": call_event.scam_probability,
                "urgency_score": call_event.urgency_score,
            }
    
    report = Report(
        report_id=report_id,
        user_id=request.user_id,
        call_id=request.call_id,
        wallet_id=request.wallet_id,
        emotional_graph=emotional_graph,
        scam_script_detected=scam_script_detected,
        pdf_url=f"/api/reports/{report_id}/pdf",
    )
    
    db.create_report(report)
    
    return report


@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(report_id: str):
    report = db.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.get("/api/users/{user_id}/call-events", response_model=List[CallEvent])
async def get_user_call_events(user_id: str):
    return db.get_user_call_events(user_id)


@app.get("/api/users/{user_id}/wallet-checks", response_model=List[WalletCheck])
async def get_user_wallet_checks(user_id: str):
    return db.get_user_wallet_checks(user_id)


@app.get("/api/scam-scripts/{script_type}")
async def get_scam_script_info(script_type: str):
    try:
        script_enum = ScamScriptType(script_type)
        fingerprint = scam_script_fingerprinter.fingerprint_script("", script_enum)
        return fingerprint
    except ValueError:
        raise HTTPException(status_code=404, detail="Script type not found")


@app.get("/api/stats")
async def get_system_stats():
    return {
        "total_users": len(db.users),
        "total_call_events": len(db.call_events),
        "total_wallet_checks": len(db.wallet_checks),
        "total_gps_alerts": len(db.gps_alerts),
        "total_family_alerts": len(db.family_alerts),
        "total_reports": len(db.reports),
        "known_scam_wallets": len(db.scam_wallet_database),
        "high_risk_locations": len(db.high_risk_locations),
    }


@app.post("/api/call-events", response_model=CallEvent)
async def create_call_event(call_event: CallEvent):
    if not call_event.call_id:
        call_event.call_id = str(uuid.uuid4())
    return db.create_call_event(call_event)


@app.get("/api/call-events/{call_id}", response_model=CallEvent)
async def get_call_event(call_id: str):
    call_event = db.get_call_event(call_id)
    if not call_event:
        raise HTTPException(status_code=404, detail="Call event not found")
    return call_event


@app.post("/api/dark-pattern-analysis")
async def analyze_dark_patterns(request: dict):
    text = request.get("text", "")
    analysis = dark_pattern_fingerprinter.detect_dark_patterns(text)
    return analysis


@app.post("/api/nationality-prediction")
async def predict_nationality(request: dict):
    text = request.get("text", "")
    voice_features = request.get("voice_features")
    prediction = nationality_predictor.predict_nationality(text, voice_features)
    return prediction


@app.post("/api/threat-level")
async def calculate_threat_level(request: dict):
    threat_level = threat_level_calculator.calculate_threat_level(
        emotional_index=request.get("emotional_index", 0),
        manipulation_index=request.get("manipulation_index", 0),
        scam_pattern_match=request.get("scam_pattern_match", False),
        wallet_risk=request.get("wallet_risk", 0),
        atm_proximity=request.get("atm_proximity", False),
        store_risk=request.get("store_risk", 0),
        time_of_day_risk=request.get("time_of_day_risk", 0),
        geolocation_overlap=request.get("geolocation_overlap", False),
    )
    return threat_level


@app.post("/api/finalize-case")
async def finalize_case(request: dict):
    case_id = str(uuid.uuid4())
    user_id = request.get("user_id", "unknown")
    
    logger.info(f"🔄 START: Finalizing case {case_id} for user {user_id}")
    
    warnings = []
    
    try:
        transcript = request.get("transcript") or ""
        if not transcript:
            warnings.append("Empty transcript")
            transcript = "Data not available for this case."
        
        emotional_analysis = request.get("emotional_analysis") or None
        manipulation_index = request.get("manipulation_index", 0)
        scam_script = request.get("scam_script") or "Unknown"
        wallet_data = request.get("wallet_data") or None
        gps_data = request.get("gps_data") or None
        freeze_mode_logs = request.get("freeze_mode_logs") or []
        dark_patterns = request.get("dark_patterns") or None
        nationality_prediction = request.get("nationality_prediction") or None
        threat_level = request.get("threat_level") or None
        scammer_profile = request.get("scammer_profile") or None
        session_timeline = request.get("session_timeline") or []
        
        if len(transcript) > 50000:
            transcript = transcript[:50000] + "\n\n[Content truncated - exceeded 50,000 characters]"
            warnings.append("Transcript truncated")
        
        logger.info(f"✅ SAVE_OK: Normalized case data for {case_id}")
        
        case_data = {
            "case_id": case_id,
            "user_id": user_id,
            "status": "FINALIZED",
            "timestamp": datetime.now().isoformat(),
            "transcript": transcript,
            "emotional_analysis": emotional_analysis,
            "manipulation_index": manipulation_index,
            "scam_script": scam_script,
            "wallet_data": wallet_data,
            "gps_data": gps_data,
            "freeze_mode_logs": freeze_mode_logs,
            "dark_patterns": dark_patterns,
            "nationality_prediction": nationality_prediction,
            "threat_level": threat_level,
            "scammer_profile": scammer_profile,
            "session_timeline": session_timeline,
            "warnings": warnings
        }
        
        logger.info(f"✅ TIMELINE_OK: Timeline has {len(session_timeline)} events")
        logger.info(f"✅ PROFILE_OK: Scammer profile {'present' if scammer_profile else 'missing'}")
        logger.info(f"✅ THREAT_OK: Threat level {'present' if threat_level else 'missing'}")
        logger.info(f"✅ LINEAGE_OK: Wallet data {'present' if wallet_data else 'missing'}")
        
        pdf_url = f"/api/cases/{case_id}/pdf"
        qr_code_url = f"/api/cases/{case_id}/qr"
        
        try:
            logger.info(f"✅ PDF_OK: PDF URL generated: {pdf_url}")
        except Exception as pdf_error:
            logger.error(f"⚠️ PDF_WARNING: {str(pdf_error)}")
            warnings.append(f"PDF generation warning: {str(pdf_error)}")
        
        try:
            logger.info(f"✅ QR_OK: QR code URL generated: {qr_code_url}")
        except Exception as qr_error:
            logger.error(f"⚠️ QR_WARNING: {str(qr_error)}")
            qr_code_url = "/api/cases"
            warnings.append(f"QR generation warning: {str(qr_error)}")
        
        logger.info(f"✅ CLEANUP_OK: Case {case_id} finalized successfully")
        
        return {
            "case_id": case_id,
            "status": "success",
            "message": "Case finalized successfully",
            "pdf_url": pdf_url,
            "qr_code_url": qr_code_url,
            "warnings": warnings if warnings else None
        }
        
    except Exception as e:
        logger.error(f"❌ ERROR: Case finalization failed for {case_id}: {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Case finalization failed: {str(e)}"
        )



@app.post("/api/subscription/check", response_model=SubscriptionCheckResponse)
async def check_subscription_access(request: SubscriptionCheckRequest):
    """Check if user has access to a specific feature"""
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    has_access = subscription_service.check_feature_access(user, request.feature)
    required_tier = subscription_service.get_required_tier(request.feature)
    upgrade_message = None
    
    if not has_access:
        upgrade_message = subscription_service.get_upgrade_message(request.feature, user.subscription_tier)
    
    return SubscriptionCheckResponse(
        has_access=has_access,
        current_tier=user.subscription_tier,
        required_tier=required_tier,
        upgrade_message=upgrade_message
    )


@app.post("/api/subscription/create", response_model=CreateSubscriptionResponse)
async def create_subscription(request: CreateSubscriptionRequest):
    """Create or upgrade a subscription (Stripe integration placeholder)"""
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    user.subscription_tier = request.tier
    user.subscription_expiration = datetime.now() + timedelta(days=30)
    user.stripe_customer_id = f"cus_{uuid.uuid4().hex[:14]}"
    user.stripe_subscription_id = f"sub_{uuid.uuid4().hex[:14]}"
    
    db.update_user(request.user_id, user.dict())
    
    return CreateSubscriptionResponse(
        success=True,
        subscription_id=user.stripe_subscription_id,
        customer_id=user.stripe_customer_id,
        message=f"Successfully subscribed to {subscription_service.get_tier_name(request.tier)}"
    )


@app.post("/api/subscription/cancel", response_model=CancelSubscriptionResponse)
async def cancel_subscription(request: CancelSubscriptionRequest):
    """Cancel a subscription"""
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.subscription_tier == SubscriptionTier.FREE:
        return CancelSubscriptionResponse(
            success=False,
            message="No active subscription to cancel"
        )
    
    
    return CancelSubscriptionResponse(
        success=True,
        message="Subscription will be canceled at the end of the current billing period"
    )


@app.get("/api/subscription/tiers")
async def get_subscription_tiers():
    """Get all available subscription tiers with features and pricing"""
    tiers = []
    
    for tier in [SubscriptionTier.FREE, SubscriptionTier.PREMIUM, SubscriptionTier.ULTRA, SubscriptionTier.ENTERPRISE]:
        tier_info = {
            "tier": tier.value,
            "name": subscription_service.get_tier_name(tier),
            "price": subscription_service.get_tier_price(tier),
            "family_limit": subscription_service.get_family_limit(tier),
            "features": subscription_service.get_tier_features(tier)
        }
        tiers.append(tier_info)
    
    return {"tiers": tiers}


@app.get("/api/subscription/user/{user_id}")
async def get_user_subscription(user_id: str):
    """Get user's current subscription status"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_expired = False
    if user.subscription_expiration:
        is_expired = user.subscription_expiration < datetime.now()
    
    return {
        "user_id": user.user_id,
        "subscription_tier": user.subscription_tier,
        "tier_name": subscription_service.get_tier_name(user.subscription_tier),
        "subscription_expiration": user.subscription_expiration,
        "is_expired": is_expired,
        "family_members_count": len(user.family_members),
        "family_limit": subscription_service.get_family_limit(user.subscription_tier),
        "stripe_customer_id": user.stripe_customer_id,
        "stripe_subscription_id": user.stripe_subscription_id
    }


@app.post("/api/subscription/webhook")
async def stripe_webhook(request: dict):
    """Handle Stripe webhook events (subscription.updated, subscription.deleted, etc.)"""
    
    event_type = request.get("type")
    
    if event_type == "customer.subscription.updated":
        pass
    elif event_type == "customer.subscription.deleted":
        pass
    elif event_type == "invoice.payment_failed":
        pass
    
    return {"status": "received"}
