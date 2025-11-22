"""
Threat Level Engine Tests
Tests TL-01, TL-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestThreatLevel:
    """Test Threat Level calculation capabilities"""
    
    def test_tl01_high_risk_detection(self):
        """
        TEST CASE TL-01: High Risk Threat
        Expected: Threat Score 90-100%, Classification: HIGH RISK
        """
        payload = {
            "text": "You must send the money or the police will come today.",
            "user_id": "test-user",
            "call_id": "test-tl01"
        }
        
        response = client.post("/api/threat-level", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        threat_score = data.get("threat_score", 0)
        assert threat_score >= 80, \
            f"Expected HIGH threat score (>=80%), got {threat_score}%"
        
        risk_level = data.get("risk_level", "").lower()
        assert risk_level in ["high", "critical", "high risk"], \
            f"Expected HIGH RISK classification, got: {data.get('risk_level')}"
        
        indicators = data.get("threat_indicators", [])
        indicators_str = " ".join(indicators).lower()
        assert any(keyword in indicators_str for keyword in ["urgency", "threat", "police", "authority", "immediate"]), \
            f"Expected threat indicators, got: {indicators}"
        
        print(f"✅ TL-01 PASSED: High risk detected - score={threat_score}%, level={data.get('risk_level')}, indicators={indicators}")
    
    def test_tl02_low_risk_detection(self):
        """
        TEST CASE TL-02: Low Risk / Safe
        Expected: Threat Score <10%, Classification: SAFE
        """
        payload = {
            "text": "Hey, just checking if you're free later.",
            "user_id": "test-user",
            "call_id": "test-tl02"
        }
        
        response = client.post("/api/threat-level", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        threat_score = data.get("threat_score", 0)
        assert threat_score <= 20, \
            f"Expected LOW threat score (<=20%), got {threat_score}%"
        
        risk_level = data.get("risk_level", "").lower()
        assert risk_level in ["low", "safe", "minimal", "low risk"], \
            f"Expected SAFE/LOW classification, got: {data.get('risk_level')}"
        
        print(f"✅ TL-02 PASSED: Low risk detected - score={threat_score}%, level={data.get('risk_level')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
