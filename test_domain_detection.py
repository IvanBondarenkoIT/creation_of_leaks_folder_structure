#!/usr/bin/env python3
"""
Test script for domain detection issues
"""

from filename_analyzer import FilenameAnalyzer

def test_domain_detection():
    """Test domain detection for specific cases"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_category, expected_domain, description)
        ("tiva.am", "Database", "tiva.am", "Should be Database - domain with .am"),
        ("tokosatu.com", "Database", "tokosatu.com", "Should be Database - domain with .com"),
        ("tronwallet.id", "Database", "tronwallet.id", "Should be Database - domain with .id"),
        ("order_bnaia.com", "Database", "bnaia.com", "Should be Database - domain with underscore"),
        ("bestbuy.ca", "Database", "bestbuy.ca", "Should be Database - domain with .ca"),
        ("VALID_MEGA_COMBO", "Combo", None, "Should be Combo - combo indicators"),
        ("Germany_hotmail", "Combo", None, "Should be Combo - combo indicators"),
    ]
    
    print("=" * 80)
    print("DOMAIN DETECTION TEST")
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
            domain_ok = result.domain_name is None
        
        # Overall result
        test_passed = category_ok and domain_ok
        
        if test_passed:
            print(f"[PASS] {filename}")
            print(f"       Expected: {expected_category} / {expected_domain}")
            print(f"       Got:      {result.suggested_category} / {result.domain_name}")
            print(f"       Reason:   {result.reason}")
            passed += 1
        else:
            print(f"[FAIL] {filename}")
            print(f"       Expected: {expected_category} / {expected_domain}")
            print(f"       Got:      {result.suggested_category} / {result.domain_name}")
            print(f"       Reason:   {result.reason}")
            print(f"       Issue:    {description}")
            failed += 1
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    if failed == 0:
        print("ALL TESTS PASSED! Domain detection is working correctly.")
    else:
        print(f"WARNING: {failed} tests failed. Need further adjustments.")
    
    return failed == 0

if __name__ == "__main__":
    test_domain_detection()
