"""
Nationality Prediction Engine Tests
Tests NP-01, NP-02 from CryptoShield AI Test Suite
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestNationalityPrediction:
    """Test Nationality Prediction AI capabilities"""
    
    def test_np01_south_asia_detection(self):
        """
        TEST CASE NP-01: South Asian Language Patterns
        Expected: Region: South Asia (India/Pakistan), Confidence: Medium
        """
        payload = {
            "text": "Kindly send me the OTP so I can verify your account, sir.",
            "user_id": "test-user"
        }
        
        response = client.post("/api/nationality-prediction", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        predicted_region = data.get("predicted_region", "").lower()
        assert any(keyword in predicted_region for keyword in ["south asia", "india", "pakistan", "indian", "south asian"]), \
            f"Expected South Asia region, got: {data.get('predicted_region')}"
        
        confidence = data.get("confidence", 0)
        assert confidence >= 40, \
            f"Expected medium confidence (>=40%), got {confidence}%"
        
        markers = data.get("linguistic_markers", [])
        markers_str = " ".join(markers).lower()
        assert any(keyword in markers_str for keyword in ["kindly", "sir", "formal", "polite"]), \
            f"Expected South Asian linguistic markers, got: {markers}"
        
        print(f"✅ NP-01 PASSED: South Asian origin detected - region={data.get('predicted_region')}, confidence={confidence}%, markers={markers}")
    
    def test_np02_west_africa_detection(self):
        """
        TEST CASE NP-02: West African Language Patterns
        Expected: Region: West Africa, Confidence: Medium/High
        """
        payload = {
            "text": "My dear, I promise I will return to you after this offshore contract.",
            "user_id": "test-user"
        }
        
        response = client.post("/api/nationality-prediction", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        predicted_region = data.get("predicted_region", "").lower()
        assert any(keyword in predicted_region for keyword in ["west africa", "africa", "nigerian", "ghana"]), \
            f"Expected West Africa region, got: {data.get('predicted_region')}"
        
        confidence = data.get("confidence", 0)
        assert confidence >= 40, \
            f"Expected medium/high confidence (>=40%), got {confidence}%"
        
        markers = data.get("linguistic_markers", [])
        markers_str = " ".join(markers).lower()
        assert any(keyword in markers_str for keyword in ["my dear", "promise", "offshore", "contract"]), \
            f"Expected West African linguistic markers, got: {markers}"
        
        print(f"✅ NP-02 PASSED: West African origin detected - region={data.get('predicted_region')}, confidence={confidence}%, markers={markers}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
