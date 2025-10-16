"""
Test domain extraction from complex filenames
"""

from filename_analyzer import FilenameAnalyzer

def test_domain_extraction():
    """Test the new extract_domain_from_filename method"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        # (filename, expected_domain)
        ("teamlease.com (india).txt", "teamlease.com"),
        ("bestbuy.ca.txt", "bestbuy.ca"),
        ("Blibli.com-indonasia.txt", "Blibli.com"),
        ("Lebanon locatefamily_com 2022.05.04 (21 792).txt", "locatefamily.com"),
        ("amazon.com database.sql", "amazon.com"),
        ("paypal.com users (2024).txt", "paypal.com"),
        ("shopify_com_leak.txt", "shopify.com"),
        ("ebay_co_uk database.txt", "ebay.co"),
        ("booking_com.txt", "booking.com"),
        ("aliexpress.ru - russia.txt", "aliexpress.ru"),
        ("flipkart.in india ecommerce.txt", "flipkart.in"),
        ("tokopedia.id indonesia.txt", "tokopedia.id"),
        # Additional complex cases
        ("amazon-com-leak.txt", "amazon.com"),  # dash separator
        ("paypal-net-users.txt", "paypal.net"),
        ("site_org_backup.txt", "site.org"),
        ("https://example.com/leak.txt", "example.com"),  # URL
        ("company.co.uk (UK).txt", "company.co.uk"),
        ("database_nl_2024.txt", "database.nl"),
    ]
    
    print("=" * 80)
    print("DOMAIN EXTRACTION TEST")
    print("=" * 80)
    
    success = 0
    failed = 0
    
    for filename, expected in test_cases:
        extracted = analyzer.extract_domain_from_filename(filename)
        
        if extracted and extracted.lower() == expected.lower():
            status = "PASS"
            success += 1
        else:
            status = "FAIL"
            failed += 1
        
        print(f"\n[{status}] {filename}")
        print(f"      Expected: {expected}")
        print(f"      Got:      {extracted}")
    
    print("\n" + "=" * 80)
    print(f"RESULTS: {success} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    # Test full analysis with prepare
    print("\n" + "=" * 80)
    print("FULL ANALYSIS TEST (with category detection)")
    print("=" * 80)
    
    full_test_cases = [
        "teamlease.com (india).txt",
        "bestbuy.ca database.sql",
        "Blibli.com-indonasia.txt",
        "Lebanon locatefamily_com 2022.05.04 (21 792).txt",
        "VALID_MEGA_COMBO.txt",
        "Germany_hotmail.txt",
    ]
    
    for filename in full_test_cases:
        result = analyzer.analyze_filename(filename)
        extracted = analyzer.extract_domain_from_filename(filename)
        
        print(f"\nFile: {filename}")
        print(f"   Category: {result.suggested_category}")
        print(f"   Extracted domain: {extracted}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Reason: {result.reason}")

if __name__ == "__main__":
    test_domain_extraction()

