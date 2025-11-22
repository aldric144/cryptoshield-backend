"""
Intervention Engine Tests
Tests IE-01, IE-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestInterventionEngine:
    """Test Intervention Engine response capabilities"""
    
    def test_ie01_police_payment_scam_intervention(self):
        """
        TEST CASE IE-01: Police Payment Scam
        Expected: Intervention message about law enforcement never demanding payment
        """
        payload = {
            "user_id": "test-user",
            "call_id": "test-ie01",
            "scam_type": "authority_scam",
            "threat_level": "high",
            "victim_statement": "He said if I don't pay he's sending police."
        }
        
        response = client.post("/api/intervention", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        message = data.get("intervention_message", "").lower()
        assert len(message) > 0, "Expected intervention message to be provided"
        
        assert any(keyword in message for keyword in ["law enforcement", "police", "payment", "scam", "tactic", "never"]), \
            f"Expected intervention about law enforcement payment scam, got: {data.get('intervention_message')}"
        
        actions = data.get("recommended_actions", [])
        assert len(actions) > 0, "Expected recommended actions to be provided"
        
        print(f"✅ IE-01 PASSED: Police payment scam intervention - message='{data.get('intervention_message')[:100]}...', actions={len(actions)}")
    
    def test_ie02_love_bombing_intervention(self):
        """
        TEST CASE IE-02: Love Bombing
        Expected: Intervention message about classic love bombing tactics
        """
        payload = {
            "user_id": "test-user",
            "call_id": "test-ie02",
            "scam_type": "romance_scam",
            "threat_level": "medium",
            "victim_statement": "He keeps telling me I'm the only one he loves."
        }
        
        response = client.post("/api/intervention", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        message = data.get("intervention_message", "").lower()
        assert len(message) > 0, "Expected intervention message to be provided"
        
        assert any(keyword in message for keyword in ["love bombing", "romance", "caution", "careful", "warning", "manipulation"]), \
            f"Expected intervention about love bombing, got: {data.get('intervention_message')}"
        
        actions = data.get("recommended_actions", [])
        assert len(actions) > 0, "Expected recommended actions to be provided"
        
        print(f"✅ IE-02 PASSED: Love bombing intervention - message='{data.get('intervention_message')[:100]}...', actions={len(actions)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
