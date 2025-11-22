"""
Pytest configuration and fixtures for CryptoShield AI Test Suite
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def test_user_id():
    """Provide a consistent test user ID across all tests"""
    return "test-user-ai-suite"


@pytest.fixture(scope="session")
def test_call_id_prefix():
    """Provide a consistent call ID prefix for test isolation"""
    return "test-ai-"


@pytest.fixture(autouse=True)
def reset_test_state():
    """Reset any test state before each test"""
    yield
    pass


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "voice_shield: Tests for Voice Shield AI engine"
    )
    config.addinivalue_line(
        "markers", "emotional: Tests for Emotional Analysis engine"
    )
    config.addinivalue_line(
        "markers", "dark_patterns: Tests for Dark Pattern detection"
    )
    config.addinivalue_line(
        "markers", "nationality: Tests for Nationality Prediction"
    )
    config.addinivalue_line(
        "markers", "threat_level: Tests for Threat Level calculation"
    )
    config.addinivalue_line(
        "markers", "intervention: Tests for Intervention Engine"
    )
    config.addinivalue_line(
        "markers", "text_analyzer: Tests for Text Analyzer"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their module"""
    for item in items:
        if "voice_shield" in item.nodeid:
            item.add_marker(pytest.mark.voice_shield)
        elif "emotional" in item.nodeid:
            item.add_marker(pytest.mark.emotional)
        elif "dark_pattern" in item.nodeid:
            item.add_marker(pytest.mark.dark_patterns)
        elif "nationality" in item.nodeid:
            item.add_marker(pytest.mark.nationality)
        elif "threat_level" in item.nodeid:
            item.add_marker(pytest.mark.threat_level)
        elif "intervention" in item.nodeid:
            item.add_marker(pytest.mark.intervention)
        elif "text_analyzer" in item.nodeid:
            item.add_marker(pytest.mark.text_analyzer)
