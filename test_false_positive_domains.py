#!/usr/bin/env python3
"""
Test script for false positive domain detection
"""

from filename_analyzer import FilenameAnalyzer

def test_false_positive_domains():
    """Test false positive domain detection cases"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_category, expected_domain, description)
        ("BANGKA_BELITUNG_KAB_BANGKA_SELATAN_1903_3e6b6657_c2bf_4529_a845.7z", "Combo", None, "Should be Combo - geographic name, not domain"),
        ("INDONESIA_JAKARTA_CENTRAL_2023.7z", "Combo", None, "Should be Combo - geographic name, not domain"),
        ("GERMANY_BERLIN_MITTE_2024.zip", "Combo", None, "Should be Combo - geographic name, not domain"),
        ("tiva.am", "Database", "tiva.am", "Should be Database - valid domain"),
        ("tokosatu.com", "Database", "tokosatu.com", "Should be Database - valid domain"),
        ("tronwallet.id", "Database", "tronwallet.id", "Should be Database - valid domain"),
        ("VALID_MEGA_COMBO", "Combo", None, "Should be Combo - combo indicators"),
    ]
    
    print("=" * 80)
    print("FALSE POSITIVE DOMAIN DETECTION TEST")
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
        print("ALL TESTS PASSED! False positive detection is working correctly.")
    else:
        print(f"WARNING: {failed} tests failed. Need further adjustments.")
    
    return failed == 0

if __name__ == "__main__":
    test_false_positive_domains()
