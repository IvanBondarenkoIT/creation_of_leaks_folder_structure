#!/usr/bin/env python3
"""
Test script for sample/test file detection
"""

from filename_analyzer import FilenameAnalyzer

def test_sample_files():
    """Test sample/test file detection cases"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_category, expected_domain, description)
        ("chanel_sample.txt", "Combo", None, "Should be Combo - sample file, not domain"),
        ("amazon_test.csv", "Combo", None, "Should be Combo - test file, not domain"),
        ("facebook_example.json", "Combo", None, "Should be Combo - example file, not domain"),
        ("shopify_demo.zip", "Combo", None, "Should be Combo - demo file, not domain"),
        ("chanel.sa", "Database", "chanel.sa", "Should be Database - valid domain with .sa"),
        ("tiva.am", "Database", "tiva.am", "Should be Database - valid domain"),
        ("tokosatu.com", "Database", "tokosatu.com", "Should be Database - valid domain"),
        ("VALID_MEGA_COMBO", "Combo", None, "Should be Combo - combo indicators"),
    ]
    
    print("=" * 80)
    print("SAMPLE FILE DETECTION TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for filename, expected_category, expected_domain, description in test_cases:
        result = analyzer.analyze_filename(filename)
        
        # Check category
        category_ok = result.suggested_category == expected_category
        
        # Check domain (if expected)
        domain_ok = True
        if expected_domain:
            domain_ok = result.domain_name == expected_domain
        else:
            domain_ok = result.domain_name is None or result.domain_name == ""
        
        # Overall result
        test_passed = category_ok and domain_ok
        
        if test_passed:
            print(f"[PASS] {filename}")
            print(f"       Expected: {expected_category} / {expected_domain or 'None'}")
            print(f"       Got:      {result.suggested_category} / {result.domain_name or 'None'}")
            print(f"       Reason:   {result.reason}")
            passed += 1
        else:
            print(f"[FAIL] {filename}")
            print(f"       Expected: {expected_category} / {expected_domain or 'None'}")
            print(f"       Got:      {result.suggested_category} / {result.domain_name or 'None'}")
            print(f"       Reason:   {result.reason}")
            print(f"       Issue:    {description}")
            failed += 1
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    if failed == 0:
        print("ALL TESTS PASSED! Sample file detection is working correctly.")
    else:
        print(f"WARNING: {failed} tests failed. Need further adjustments.")
    
    return failed == 0

if __name__ == "__main__":
    test_sample_files()









