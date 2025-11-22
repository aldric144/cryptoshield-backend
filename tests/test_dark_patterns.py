"""
Dark Pattern Manipulation Detector Tests
Tests DP-01, DP-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestDarkPatterns:
    """Test Dark Pattern manipulation detection"""
    
    def test_dp01_gaslighting_detection(self):
        """
        TEST CASE DP-01: Gaslighting
        Expected: HIGH Gaslighting
        """
        payload = {
            "text": "You're overreacting. Nobody else has a problem with this except you.",
            "user_id": "test-user"
        }
        
        response = client.post("/api/dark-pattern-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        patterns = data.get("patterns", [])
        patterns_str = " ".join(patterns).lower()
        
        assert any(keyword in patterns_str for keyword in ["gaslighting", "gaslight", "manipulation", "invalidation"]), \
            f"Expected gaslighting pattern detected, got: {patterns}"
        
        manipulation_score = data.get("manipulation_score", 0)
        assert manipulation_score >= 60, \
            f"Expected high manipulation score (>=60), got {manipulation_score}"
        
        print(f"✅ DP-01 PASSED: Gaslighting detected - patterns={patterns}, score={manipulation_score}")
    
    def test_dp02_false_authority_detection(self):
        """
        TEST CASE DP-02: Authority Fraud
        Expected: HIGH False Authority
        """
        payload = {
            "text": "I work with federal intelligence. You need to do exactly what I say.",
            "user_id": "test-user"
        }
        
        response = client.post("/api/dark-pattern-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        patterns = data.get("patterns", [])
        patterns_str = " ".join(patterns).lower()
        
        assert any(keyword in patterns_str for keyword in ["authority", "false authority", "impersonation", "official"]), \
            f"Expected false authority pattern detected, got: {patterns}"
        
        manipulation_score = data.get("manipulation_score", 0)
        assert manipulation_score >= 70, \
            f"Expected high manipulation score (>=70), got {manipulation_score}"
        
        print(f"✅ DP-02 PASSED: False authority detected - patterns={patterns}, score={manipulation_score}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
