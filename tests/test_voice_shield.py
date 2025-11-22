"""
Voice Shield AI Engine Tests
Tests VS-01, VS-02, VS-03 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestVoiceShield:
    """Test Voice Shield scam detection capabilities"""
    
    def test_vs01_irs_threat_detection(self):
        """
        TEST CASE VS-01: IRS Threat
        Expected: HIGH danger, Threatening + Urgency manipulation, Freeze Mode YES
        """
        payload = {
            "call_id": "test-vs01",
            "user_id": "test-user",
            "audio_text": "This is Agent Robert Sanders from the IRS. A warrant is active. If you don't pay now, officers are coming to your house today."
        }
        
        response = client.post("/api/voice-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["scam_probability"] >= 80, f"Expected HIGH danger (>=80%), got {data['scam_probability']}%"
        
        assert data["threat_detected"] is True, "Expected threat_detected=True for IRS scam"
        
        patterns_str = " ".join(data["manipulation_patterns"]).lower()
        assert any(keyword in patterns_str for keyword in ["threat", "urgency", "authority"]), \
            f"Expected threatening/urgency/authority patterns, got: {data['manipulation_patterns']}"
        
        assert data["script_classification"] == "irs_scam", \
            f"Expected 'irs_scam' classification, got: {data['script_classification']}"
        
        print(f"✅ VS-01 PASSED: IRS threat detected with {data['scam_probability']}% probability")
    
    def test_vs02_love_scam_detection(self):
        """
        TEST CASE VS-02: Love Scam
        Expected: MEDIUM/HIGH danger, Seduction + Financial Request, Profile: Romance Scammer
        """
        payload = {
            "call_id": "test-vs02",
            "user_id": "test-user",
            "audio_text": "My love, I'm stuck overseas. Please send me $400 so I can fly home to you."
        }
        
        response = client.post("/api/voice-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["scam_probability"] >= 50, \
            f"Expected MEDIUM/HIGH danger (>=50%), got {data['scam_probability']}%"
        
        patterns_str = " ".join(data["manipulation_patterns"]).lower()
        assert any(keyword in patterns_str for keyword in ["love", "romance", "money", "financial"]), \
            f"Expected love/romance/financial patterns, got: {data['manipulation_patterns']}"
        
        assert data["script_classification"] in ["romance_scam", "love_scam", None], \
            f"Expected romance/love scam classification, got: {data['script_classification']}"
        
        print(f"✅ VS-02 PASSED: Love scam detected with {data['scam_probability']}% probability")
    
    def test_vs03_tech_support_scam_detection(self):
        """
        TEST CASE VS-03: Tech Support Scam
        Expected: HIGH danger, Urgency + False Authority
        """
        payload = {
            "call_id": "test-vs03",
            "user_id": "test-user",
            "audio_text": "Your computer is infected. Buy a $500 Target gift card right now."
        }
        
        response = client.post("/api/voice-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["scam_probability"] >= 80, \
            f"Expected HIGH danger (>=80%), got {data['scam_probability']}%"
        
        assert data["urgency_score"] >= 20, \
            f"Expected high urgency score (>=20), got {data['urgency_score']}"
        
        patterns_str = " ".join(data["manipulation_patterns"]).lower()
        assert any(keyword in patterns_str for keyword in ["urgency", "authority", "threat"]), \
            f"Expected urgency/authority patterns, got: {data['manipulation_patterns']}"
        
        print(f"✅ VS-03 PASSED: Tech support scam detected with {data['scam_probability']}% probability")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
