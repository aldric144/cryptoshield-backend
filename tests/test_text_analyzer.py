"""
Text Analyzer Tests
Tests TA-01, TA-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestTextAnalyzer:
    """Test Text Analyzer for message/email/chat analysis"""
    
    def test_ta01_crypto_investment_fraud(self):
        """
        TEST CASE TA-01: Crypto Investment Fraud
        Expected: HIGH danger, Scam Type: Investment Fraud
        """
        payload = {
            "call_id": "test-ta01",
            "user_id": "test-user",
            "audio_text": "I can triple your Bitcoin in 24 hours. Guaranteed."
        }
        
        response = client.post("/api/voice-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["scam_probability"] >= 80, \
            f"Expected HIGH danger (>=80%), got {data['scam_probability']}%"
        
        assert data["threat_detected"] is True, \
            "Expected threat_detected=True for investment fraud"
        
        patterns_str = " ".join(data["manipulation_patterns"]).lower()
        assert any(keyword in patterns_str for keyword in ["money", "financial", "investment", "guarantee"]), \
            f"Expected investment fraud patterns, got: {data['manipulation_patterns']}"
        
        print(f"✅ TA-01 PASSED: Crypto investment fraud detected - probability={data['scam_probability']}%, patterns={data['manipulation_patterns']}")
    
    def test_ta02_phishing_account_verification(self):
        """
        TEST CASE TA-02: Account Verification Phishing
        Expected: HIGH danger, Scam Type: Phishing
        """
        payload = {
            "call_id": "test-ta02",
            "user_id": "test-user",
            "audio_text": "Your PayPal account is restricted. Click this link to restore access."
        }
        
        response = client.post("/api/voice-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["scam_probability"] >= 80, \
            f"Expected HIGH danger (>=80%), got {data['scam_probability']}%"
        
        assert data["threat_detected"] is True, \
            "Expected threat_detected=True for phishing"
        
        assert data["urgency_score"] >= 20, \
            f"Expected elevated urgency score (>=20), got {data['urgency_score']}"
        
        patterns_str = " ".join(data["manipulation_patterns"]).lower()
        assert any(keyword in patterns_str for keyword in ["urgency", "threat", "authority"]), \
            f"Expected phishing patterns, got: {data['manipulation_patterns']}"
        
        print(f"✅ TA-02 PASSED: Phishing detected - probability={data['scam_probability']}%, urgency={data['urgency_score']}, patterns={data['manipulation_patterns']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
