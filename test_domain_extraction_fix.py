#!/usr/bin/env python3
"""
Test script for domain extraction fix
"""

from filename_analyzer import FilenameAnalyzer

def test_domain_extraction():
    """Test domain extraction for specific cases"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_domain, description)
        ("order_bnaia.com", "order.bnaia.com", "Should convert underscore to dot in domain"),
        ("teamlease.com (india)", "teamlease.com", "Should extract domain with dots"),
        ("bestbuy.ca", "bestbuy.ca", "Should extract domain with dots"),
        ("6av_top", "6av.top", "Should convert underscore to dot"),
        ("aitrip_cl", "aitrip.cl", "Should convert underscore to dot"),
        ("amazon_com", "amazon.com", "Should convert underscore to dot"),
        ("Blibli.com-indonesia", "Blibli.com", "Should extract domain with dots"),
        ("Lebanon locatefamily_com 2022.05.04", "locatefamily.com", "Should extract domain with underscore"),
    ]
    
    print("=" * 80)
    print("DOMAIN EXTRACTION TEST")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for filename, expected_domain, description in test_cases:
        extracted = analyzer.extract_domain_from_filename(filename)
        
        if extracted == expected_domain:
            print(f"[PASS] {filename}")
            print(f"       Expected: {expected_domain}")
            print(f"       Got:      {extracted}")
            print(f"       Reason:   {description}")
            passed += 1
        else:
            print(f"[FAIL] {filename}")
            print(f"       Expected: {expected_domain}")
            print(f"       Got:      {extracted}")
            print(f"       Issue:    {description}")
            failed += 1
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    if failed == 0:
        print("ALL TESTS PASSED! Domain extraction is working correctly.")
    else:
        print(f"WARNING: {failed} tests failed. Need further adjustments.")
    
    return failed == 0

if __name__ == "__main__":
    test_domain_extraction()
