"""
Comprehensive AI Test Suite Runner
Runs all 21 test cases across 7 AI engines

Test Coverage:
- Voice Shield: VS-01, VS-02, VS-03 (3 tests)
- Emotional Analysis: EA-01, EA-02 (2 tests)
- Dark Patterns: DP-01, DP-02 (2 tests)
- Nationality Prediction: NP-01, NP-02 (2 tests)
- Threat Level: TL-01, TL-02 (2 tests)
- Intervention Engine: IE-01, IE-02 (2 tests)
- Text Analyzer: TA-01, TA-02 (2 tests)

Total: 15 test cases implemented (Note: User document listed 21 but provided 15)
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def run_all_tests():
    """Run all AI engine tests with verbose output"""
    test_files = [
        "tests/test_voice_shield.py",
        "tests/test_emotional_analysis.py",
        "tests/test_dark_patterns.py",
        "tests/test_nationality_prediction.py",
        "tests/test_threat_level.py",
        "tests/test_intervention.py",
        "tests/test_text_analyzer.py",
    ]
    
    print("=" * 80)
    print("CRYPTOSHIELD AI COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Running {len(test_files)} test modules covering 7 AI engines...")
    print("=" * 80)
    print()
    
    exit_code = pytest.main([
        "-v",
        "--tb=short",
        "--color=yes",
        "-ra",  # Show summary of all test results
        *test_files
    ])
    
    print()
    print("=" * 80)
    if exit_code == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED - Review output above")
    print("=" * 80)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(run_all_tests())
