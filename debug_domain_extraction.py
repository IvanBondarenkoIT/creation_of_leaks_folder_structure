#!/usr/bin/env python3
"""
Debug script for domain extraction
"""

from filename_analyzer import FilenameAnalyzer
import re

def debug_domain_extraction():
    """Debug domain extraction for specific cases"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        "order_bnaia.com",
        "teamlease.com (india)",
        "bestbuy.ca",
        "6av_top",
        "aitrip_cl",
        "amazon_com",
        "Blibli.com-indonesia",
        "Lebanon locatefamily_com 2022.05.04",
    ]
    
    print("=" * 80)
    print("DEBUG DOMAIN EXTRACTION")
    print("=" * 80)
    
    for filename in test_cases:
        print(f"\nTesting: {filename}")
        
        # Remove file extension
        name = re.sub(r'\.[^.]+$', '', filename)
        print(f"  After removing extension: {name}")
        
        # Test regex patterns
        extensions = r'(com|net|org|io|co|uk|us|ca|de|fr|ru|in|id|au|nl|br|mx|es|it|ch|se|no|dk|fi|be|at|pl|cz|gr|pt|tr|ae|sa|za|nz|sg|hk|tw|kr|jp|cn|vn|th|my|ph)'
        
        # Test domain with dots
        domain_with_dots = re.search(rf'([a-zA-Z0-9_-]+\.{extensions})', name, re.IGNORECASE)
        if domain_with_dots:
            domain = domain_with_dots.group(1)
            domain = domain.replace('_', '.')
            print(f"  Domain with dots: {domain}")
        else:
            print(f"  Domain with dots: No match")
        
        # Test domain with underscore
        domain_underscore = re.search(rf'([a-zA-Z0-9-]+)_{extensions}', name, re.IGNORECASE)
        if domain_underscore:
            domain = f"{domain_underscore.group(1)}.{domain_underscore.group(2)}"
            print(f"  Domain with underscore: {domain}")
        else:
            print(f"  Domain with underscore: No match")
        
        # Test actual method
        result = analyzer.extract_domain_from_filename(filename)
        print(f"  Final result: {result}")

if __name__ == "__main__":
    debug_domain_extraction()
