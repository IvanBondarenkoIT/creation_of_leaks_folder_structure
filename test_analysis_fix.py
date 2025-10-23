#!/usr/bin/env python3
"""
Test script for filename analysis fixes
"""

from filename_analyzer import FilenameAnalyzer

def test_analysis_fixes():
    """Test the specific cases mentioned by user"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_category, expected_domain, description)
        ("booktoday.org", "Database", "booktoday.org", "Should be Database - has domain with dot"),
        ("2_Store", "Combo", None, "Should be Combo - not a known company"),
        ("amazon_com", "Database", "amazon", "Should be Database - known company"),
        ("bestbuy.ca", "Database", "bestbuy.ca", "Should be Database - domain with dot"),
        ("VALID_MEGA_COMBO", "Combo", None, "Should be Combo - combo indicators"),
        ("teamlease.com (india)", "Database", "teamlease.com", "Should be Database - domain with dot"),
        ("random_org", "Database", "random.org", "Should be Database - domain with underscore converted"),
        ("facebook_com", "Database", "facebook", "Should be Database - known company"),
        ("Germany_hotmail", "Combo", None, "Should be Combo - combo indicators"),
        ("shopify_com", "Database", "shopify", "Should be Database - known company"),
        ("6av_top", "Database", "6av.top", "Should be Database - domain with underscore converted"),
        ("aitrip_cl", "Database", "aitrip.cl", "Should be Database - domain with underscore converted"),
        ("example_net", "Database", "example.net", "Should be Database - domain with underscore converted"),
    ]
    
    print("=" * 80)
    print("FILENAME ANALYSIS FIX TEST")
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
        print("ALL TESTS PASSED! Analysis fixes are working correctly.")
    else:
        print(f"WARNING: {failed} tests failed. Need further adjustments.")
    
    return failed == 0

if __name__ == "__main__":
    test_analysis_fixes()
