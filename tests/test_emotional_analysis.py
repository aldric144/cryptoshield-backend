"""
Emotional Analysis Engine Tests
Tests EA-01, EA-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestEmotionalAnalysis:
    """Test Emotional Analysis AI capabilities"""
    
    def test_ea01_threatening_anger_detection(self):
        """
        TEST CASE EA-01: Threatening Language
        Expected: High Anger, High Threatening
        """
        payload = {
            "call_id": "test-ea01",
            "user_id": "test-user",
            "audio_text": "If you don't listen to me, something bad is going to happen."
        }
        
        response = client.post("/api/emotional-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["stress_level"] >= 40 or data["fear_level"] >= 40, \
            f"Expected high stress/fear (>=40), got stress={data['stress_level']}, fear={data['fear_level']}"
        
        assert data["manipulation_index"] >= 30, \
            f"Expected elevated manipulation_index (>=30), got {data['manipulation_index']}"
        
        print(f"✅ EA-01 PASSED: Threatening tone detected - stress={data['stress_level']}, fear={data['fear_level']}, manipulation={data['manipulation_index']}")
    
    def test_ea02_seduction_love_bombing_detection(self):
        """
        TEST CASE EA-02: Seduction/Love Bombing
        Expected: High Seduction/Love Bombing
        """
        payload = {
            "call_id": "test-ea02",
            "user_id": "test-user",
            "audio_text": "Don't worry, sweetheart. You can trust me. I'll take care of everything for you."
        }
        
        response = client.post("/api/emotional-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        assert data["compliance_probability"] >= 40, \
            f"Expected high compliance_probability (>=40), got {data['compliance_probability']}"
        
        assert data["manipulation_index"] >= 30, \
            f"Expected elevated manipulation_index (>=30), got {data['manipulation_index']}"
        
        assert data["victim_vulnerability"] >= 30, \
            f"Expected elevated victim_vulnerability (>=30), got {data['victim_vulnerability']}"
        
        print(f"✅ EA-02 PASSED: Seduction/love bombing detected - compliance={data['compliance_probability']}, manipulation={data['manipulation_index']}, vulnerability={data['victim_vulnerability']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
