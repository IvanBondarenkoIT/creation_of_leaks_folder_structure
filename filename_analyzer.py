"""
Filename Analyzer Module
Intelligent analysis of filenames to detect domains, URLs, and determine file category
"""

import re
from typing import Optional
from dataclasses import dataclass


@dataclass
class FileAnalysisResult:
    """Result of filename analysis"""
    suggested_category: str  # Combo or Database
    domain_name: Optional[str]  # Extracted domain if found
    confidence: str  # high, medium, low
    reason: str  # Explanation of detection
    detected_patterns: list  # List of detected patterns


class FilenameAnalyzer:
    """Analyzes filenames to extract domain information and suggest categories"""
    
    # Common domain extensions
    DOMAIN_EXTENSIONS = [
        r'\.com', r'\.net', r'\.org', r'\.io', r'\.co', r'\.ru', r'\.de', r'\.fr',
        r'\.uk', r'\.us', r'\.ca', r'\.au', r'\.it', r'\.es', r'\.br', r'\.in',
        r'\.cn', r'\.jp', r'\.kr', r'\.nl', r'\.se', r'\.no', r'\.dk', r'\.fi',
        r'\.pl', r'\.cz', r'\.be', r'\.at', r'\.ch', r'\.mx', r'\.ar', r'\.cl',
        r'\.gov', r'\.edu', r'\.mil', r'\.int', r'\.info', r'\.biz', r'\.app',
        r'\.dev', r'\.tech', r'\.store', r'\.shop', r'\.online', r'\.site',
        r'\.xyz', r'\.top', r'\.vip', r'\.club', r'\.pro', r'\.tv', r'\.cc',
        r'\.am', r'\.id', r'\.me', r'\.ly', r'\.be', r'\.nz', r'\.sg', r'\.hk',
        r'\.tw', r'\.th', r'\.my', r'\.ph', r'\.vn', r'\.tr', r'\.ae', r'\.sa',
        r'\.za', r'\.gr', r'\.pt', r'\.ro', r'\.bg', r'\.hr', r'\.si', r'\.sk',
        r'\.hu', r'\.lt', r'\.lv', r'\.ee', r'\.ie', r'\.is', r'\.mt', r'\.cy'
    ]
    
    def __init__(self):
        # Compile regex patterns for better performance
        self.url_pattern = re.compile(
            r'https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)',
            re.IGNORECASE
        )
        
        # Domain pattern: domain.extension or www.domain.extension
        domain_exts = '|'.join(self.DOMAIN_EXTENSIONS)
        self.domain_pattern = re.compile(
            rf'(?:www\.)?([a-zA-Z0-9-]+(?:{domain_exts}))',
            re.IGNORECASE
        )
        
        # Domain with underscores (common in filenames): domain_com
        self.domain_underscore_pattern = re.compile(
            r'([a-zA-Z0-9-]+)_(com|net|org|io|co|ru|de|fr|uk|us|ca|au|it|es|br|gov|edu|top|cl|me|info|biz|name|pro|tv|cc|ly|be|nl|se|no|dk|fi|ch|at|pl|cz|gr|pt|tr|ae|sa|za|nz|sg|hk|tw|kr|jp|cn|vn|th|my|ph|am|id|nz|ro|bg|hr|si|sk|hu|lt|lv|ee|ie|is|mt|cy)',
            re.IGNORECASE
        )
        
        # Company/brand names that indicate database
        self.company_indicators = [
            'amazon', 'facebook', 'twitter', 'instagram', 'linkedin', 'microsoft',
            'google', 'apple', 'netflix', 'spotify', 'paypal', 'ebay', 'yahoo',
            'twitter', 'reddit', 'github', 'gitlab', 'adobe', 'oracle', 'salesforce',
            'dropbox', 'zoom', 'slack', 'discord', 'telegram', 'whatsapp',
            'tiktok', 'snapchat', 'pinterest', 'tumblr', 'wordpress', 'shopify'
        ]
        
        # Keywords that suggest it's a combo (not database-specific)
        self.combo_indicators = [
            'combo', 'mix', 'mixed', 'valid', 'fresh', 'hq', 'premium', 'private',
            'mega', 'cloud', 'collection', 'pack', 'archive', 'bundle',
            'hotmail', 'gmail', 'yahoo', 'mail', 'email', 'mailaccess',
            'hits', 'good', 'ok', 'checked', 'working',
            'sample', 'test', 'example', 'demo', 'trial', 'mock', 'dummy', 'fake'
        ]
        
        # Country codes that usually indicate combos
        self.country_codes = [
            'usa', 'uk', 'us', 'eu', 'canada', 'france', 'germany', 'spain',
            'italy', 'poland', 'russia', 'china', 'japan', 'korea', 'brazil',
            'india', 'vietnam', 'indonesia', 'denmark', 'netherlands', 'sweden'
        ]
        
        # Geographic indicators that suggest the file is NOT a database
        self.geographic_indicators = [
            'kab', 'kabupaten', 'provinsi', 'province', 'kota', 'city',
            'selatan', 'utara', 'barat', 'timur', 'tengah', 'pusat',
            'jakarta', 'surabaya', 'bandung', 'medan', 'semarang',
            'berlin', 'munich', 'hamburg', 'frankfurt', 'cologne',
            'london', 'paris', 'madrid', 'rome', 'amsterdam',
            'bangka', 'belitung', 'sumatra', 'kalimantan', 'java', 'bali',
            'germany', 'indonesia', 'malaysia', 'singapore', 'philippines',
            'thailand', 'vietnam', 'cambodia', 'laos', 'myanmar'
        ]
    
    def analyze_filename(self, filename: str) -> FileAnalysisResult:
        """
        Main analysis function
        
        Args:
            filename: Name of the file (with or without extension)
        
        Returns:
            FileAnalysisResult with analysis results
        """
        # Remove file extension for analysis
        name_without_ext = re.sub(r'\.[^.]+$', '', filename)
        name_lower = name_without_ext.lower()
        
        detected_patterns = []
        domain_name = None
        category = "Combo"  # Default
        confidence = "low"
        reason = "No specific indicators found"
        
        # 1. Check for full URLs (highest priority)
        url_match = self.url_pattern.search(filename)
        if url_match:
            domain_name = url_match.group(1)
            category = "Database"
            confidence = "high"
            reason = f"Full URL detected: {url_match.group(0)}"
            detected_patterns.append(f"URL: {url_match.group(0)}")
            return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
        
        # 2. Check for domain.extension pattern (PRIORITY: highest for Database)
        domain_match = self.domain_pattern.search(filename)
        if domain_match:
            potential_domain = domain_match.group(1)
            
            # Check for false positives: geographic names, long names, etc.
            # Extract just the domain part (without extension)
            domain_part = potential_domain.split('.')[0] if '.' in potential_domain else potential_domain
            
            # Check for geographic indicators in filename
            has_geographic_indicator = any(indicator in name_lower for indicator in self.geographic_indicators)
            
            # Check if potential domain contains geographic indicators
            domain_has_geo = any(indicator in domain_part.lower() for indicator in self.geographic_indicators)
            
            # Check if domain is too long (likely not a domain)
            is_too_long = len(domain_part) > 20
            
            # Only treat as domain if it doesn't look like geographic name
            if not has_geographic_indicator and not domain_has_geo and not is_too_long:
                # For domain.extension pattern, treat as Database (high confidence)
                # Examples: booktoday.org, amazon.com, bestbuy.ca
                domain_name = potential_domain
                category = "Database"
                confidence = "high"
                reason = f"Domain detected: {potential_domain}"
                detected_patterns.append(f"Domain: {potential_domain}")
                return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
            else:
                # Likely a false positive (geographic name) - treat as Combo
                # Examples: BANGKA.BE (from BANGKA_BELITUNG), etc.
                pass
        
        # 3. Check for domain_extension pattern (e.g., amazon_com, 6av_top)
        # BUT: Check for combo indicators first to avoid false positives
        combo_count = sum(1 for indicator in self.combo_indicators if indicator in name_lower)
        
        # Check for sample/test/demo/examples words (strong indicator it's not a database)
        sample_test_words = ['sample', 'test', 'example', 'demo', 'trial', 'mock', 'dummy', 'fake']
        has_sample_test_word = any(word in name_lower for word in sample_test_words)
        
        underscore_match = self.domain_underscore_pattern.search(name_lower)
        if underscore_match and combo_count < 2 and not has_sample_test_word:  # Only if not combo/sample file
            potential_domain = underscore_match.group(1)
            extension = underscore_match.group(2)
            
            # Check if extension is part of a sample/test word (e.g., "sa" from "sample")
            # If extension is "sa" and next characters form "sample", it's not a domain
            match_end_pos = underscore_match.end()
            is_false_extension = False
            if match_end_pos < len(name_lower):
                next_chars = name_lower[match_end_pos:match_end_pos+4]  # Check next 4 chars
                # Check if "sa" is part of "sample" (sa + mple)
                if extension.lower() == 'sa' and (next_chars.startswith('mpl') or 'sample' in name_lower):
                    is_false_extension = True
                # Check if extension is part of test/example/demo words
                if any(word in name_lower for word in ['test', 'example', 'demo', 'trial', 'mock']):
                    # Check if extension is first part of these words
                    for word in ['test', 'example', 'demo', 'trial', 'mock']:
                        if word.startswith(extension.lower()) and word != extension.lower():
                            is_false_extension = True
                            break
            
            if not is_false_extension:
                # Check if it's a known company (high priority)
                is_known_company = potential_domain in self.company_indicators
                
                if is_known_company:
                    # Known company - definitely Database (but not if sample/test file)
                    domain_name = potential_domain
                    category = "Database"
                    confidence = "high"
                    reason = f"Known company domain with underscore: {potential_domain}"
                    detected_patterns.append(f"Domain_ext: {underscore_match.group(0)}")
                    return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
                else:
                    # Not a known company, but could be a valid domain
                    # Check for false positives: geographic names, long names, etc.
                    
                    # Check for geographic indicators in filename
                    has_geographic_indicator = any(indicator in name_lower for indicator in self.geographic_indicators)
                    
                    # Check if potential domain is too long (likely not a domain)
                    # Real domains are usually short: amazon, google, facebook, etc.
                    is_too_long = len(potential_domain) > 20
                    
                    # Check if potential domain contains geographic indicators
                    domain_has_geo = any(indicator in potential_domain.lower() for indicator in self.geographic_indicators)
                    
                    # Check if there are many words after potential domain (suggests it's not a domain)
                    # Example: BANGKA_BELITUNG_KAB where BELITUNG is continuation, not domain
                    match_end_pos = underscore_match.end()
                    remaining_text = name_lower[match_end_pos:]
                    remaining_words = len([w for w in remaining_text.split('_') if len(w) > 3])
                    has_many_remaining_words = remaining_words > 2
                    
                    # Check if it looks like a real domain (not just random words)
                    is_valid_length = len(potential_domain) >= 2 and len(potential_domain) <= 20
                    no_forbidden_words = not any(word in potential_domain for word in ['store', 'shop', 'market', 'site', 'web', 'valid', 'mega', 'combo'])
                    
                    # Only treat as domain if all checks pass
                    if (is_valid_length and 
                        no_forbidden_words and 
                        not has_geographic_indicator and 
                        not domain_has_geo and 
                        not is_too_long and
                        not has_many_remaining_words):
                        # Convert underscore to dot: 6av_top -> 6av.top
                        domain_with_dot = f"{potential_domain}.{extension}"
                        domain_name = domain_with_dot
                        category = "Database"
                        confidence = "medium"
                        reason = f"Domain with underscore converted: {domain_with_dot}"
                        detected_patterns.append(f"Domain_ext: {underscore_match.group(0)}")
                        return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
                    else:
                        # Looks like geographic name, store/shop name or combo - treat as Combo
                        # Examples: BANGKA_BELITUNG_KAB, 2_Store, VALID_MEGA_COMBO, etc.
                        pass
        
        # 4. Check for known company/brand names (but not if sample/test/demo file)
        if not has_sample_test_word:  # Skip if sample/test/demo file
            for company in self.company_indicators:
                if company in name_lower:
                    # Check if it's surrounded by word boundaries
                    if re.search(rf'\b{company}\b', name_lower):
                        domain_name = company
                        category = "Database"
                        confidence = "medium"
                        reason = f"Company/brand name detected: {company}"
                        detected_patterns.append(f"Company: {company}")
                        # Don't return yet, might find better match
                        break
        
        # 5. Check for strong combo indicators
        combo_count = sum(1 for indicator in self.combo_indicators if indicator in name_lower)
        if combo_count >= 2:
            category = "Combo"
            confidence = "high"
            reason = f"Multiple combo indicators found ({combo_count})"
            detected_patterns.append(f"Combo indicators: {combo_count}")
            return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
        
        # 6. Check for country codes (usually combos)
        for country in self.country_codes:
            if re.search(rf'\b{country}\b', name_lower):
                if category != "Database":  # Don't override database detection
                    category = "Combo"
                    confidence = "medium"
                    reason = f"Country code detected: {country}"
                    detected_patterns.append(f"Country: {country}")
                break
        
        # 7. Pattern-based heuristics
        # If filename has "database", "db", "sql" -> Database
        if any(word in name_lower for word in ['database', '_db_', '_sql_', 'dump', 'backup']):
            if category != "Database" or confidence == "low":
                category = "Database"
                confidence = "medium"
                reason = "Database-related keywords detected"
                detected_patterns.append("DB keywords")
        
        # If we detected a company but no strong combo indicators, keep Database
        if domain_name and category == "Database":
            return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
        
        # Default to Combo with low confidence
        if not detected_patterns:
            detected_patterns.append("Generic filename")
        
        return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
    
    def extract_clean_domain_name(self, domain: str) -> str:
        """
        Clean up extracted domain name for use as folder name
        
        Args:
            domain: Raw domain string
        
        Returns:
            Clean folder-safe domain name
        """
        if not domain:
            return ""
        
        # Remove common prefixes
        domain = re.sub(r'^www\.', '', domain, flags=re.IGNORECASE)
        domain = re.sub(r'^https?://', '', domain, flags=re.IGNORECASE)
        
        # Remove extension for cleaner folder name
        domain = re.sub(r'\.(com|net|org|io|co|ru|de|fr|uk|us)$', '', domain, flags=re.IGNORECASE)
        
        # Replace dots and special chars with underscores
        domain = re.sub(r'[^a-zA-Z0-9_-]', '_', domain)
        
        # Remove multiple underscores
        domain = re.sub(r'_+', '_', domain)
        
        # Remove leading/trailing underscores
        domain = domain.strip('_')
        
        return domain
    
    def extract_domain_from_filename(self, filename: str) -> Optional[str]:
        """
        Extract domain from complex filenames with MAXIMUM attention to find hidden domains.
        
        Examples:
            teamlease.com (india) → teamlease.com
            bestbuy.ca → bestbuy.ca
            Blibli.com-indonasia → Blibli.com
            Lebanon locatefamily_com 2022.05.04 (21 792) → locatefamily.com
            amazon_com_leak → amazon.com
            paypal.com users (2024) → paypal.com
            
        Args:
            filename: Raw filename
            
        Returns:
            Clean domain name with extension or None
        """
        # Remove file extension (but not domain extensions)
        # Only remove if it's not a domain extension
        domain_extensions = r'\.(com|net|org|io|co|uk|us|ca|de|fr|ru|in|id|au|nl|br|mx|es|it|ch|se|no|dk|fi|be|at|pl|cz|gr|pt|tr|ae|sa|za|nz|sg|hk|tw|kr|jp|cn|vn|th|my|ph)$'
        if not re.search(domain_extensions, filename, re.IGNORECASE):
            name = re.sub(r'\.[^.]+$', '', filename)
        else:
            name = filename
        
        # Extended list of domain extensions - using capturing group
        extensions = r'(com|net|org|io|co|uk|us|ca|de|fr|ru|in|id|au|nl|br|mx|es|it|ch|se|no|dk|fi|be|at|pl|cz|gr|pt|tr|ae|sa|za|nz|sg|hk|tw|kr|jp|cn|vn|th|my|ph|am|me|ly|nz|ro|bg|hr|si|sk|hu|lt|lv|ee|ie|is|mt|cy)'
        
        # PRIORITY 1: Full domain.extension pattern (with dots) - most reliable
        # Match: word.com, word.co.uk, site.net anywhere in filename
        domain_with_dots = re.search(rf'([a-zA-Z0-9_-]+\.{extensions})', name, re.IGNORECASE)
        if domain_with_dots:
            # Convert underscores to dots in domain name
            domain = domain_with_dots.group(1)
            domain = domain.replace('_', '.')
            return domain
        
        # PRIORITY 2: domain_extension pattern (with underscore)
        # Match: domain_com, domain_net, paypal_com, etc.
        domain_underscore = re.search(rf'([a-zA-Z0-9-]+)_{extensions}', name, re.IGNORECASE)
        if domain_underscore:
            # Convert underscore to dot: domain_com → domain.com
            return f"{domain_underscore.group(1)}.{domain_underscore.group(2)}"
        
        # PRIORITY 3: domain-extension pattern (with dash)
        # Match: domain-com, site-net, etc.
        domain_dash = re.search(rf'([a-zA-Z0-9]+)-{extensions}', name, re.IGNORECASE)
        if domain_dash:
            # Convert dash to dot: domain-com → domain.com
            return f"{domain_dash.group(1)}.{domain_dash.group(2)}"
        
        # PRIORITY 4: Look for domain at the start of filename
        # Match: bestbuy.ca, amazon.com at the beginning
        start_domain = re.match(rf'^([a-zA-Z0-9-]+\.{extensions})', name, re.IGNORECASE)
        if start_domain:
            return start_domain.group(1)
        
        # PRIORITY 5: Try to find patterns like "domaincom" (no separator)
        # This is less reliable, so check if it's a known company
        domain_nosep = re.search(rf'\b([a-zA-Z0-9]+)({extensions})\b', name, re.IGNORECASE)
        if domain_nosep:
            potential_domain = domain_nosep.group(1)
            # Only accept if it's a known company to avoid false positives
            if potential_domain.lower() in self.company_indicators:
                ext = domain_nosep.group(2)
                return f"{potential_domain}.{ext}"
        
        # PRIORITY 6: Look for URLs with http/https
        url_match = re.search(r'https?://(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+)', name, re.IGNORECASE)
        if url_match:
            return url_match.group(1)
        
        return None


# Test function
def test_analyzer():
    """Test the filename analyzer with various examples"""
    analyzer = FilenameAnalyzer()
    
    test_cases = [
        "amazon_com_database.txt",
        "facebook.com_users.sql",
        "https://linkedin.com_leak.txt",
        "twitter_dump_2024.txt",
        "combo_fresh_valid.txt",
        "USA_mail_access.txt",
        "MegaCloud_valid.txt",
        "shopify_customers.sql",
        "Mixed_HQ_Premium.txt",
        "Germany_hotmail.txt",
        "paypal_database.txt",
        "random_file_12345.txt",
        "VALID_BY_MEGA.txt",
        "ebay.com.txt",
        "discord_tokens.txt"
    ]
    
    print("=" * 80)
    print("FILENAME ANALYZER TEST RESULTS")
    print("=" * 80)
    
    for filename in test_cases:
        result = analyzer.analyze_filename(filename)
        print(f"\nFile: {filename}")
        print(f"   Category: {result.suggested_category}")
        print(f"   Domain: {result.domain_name or 'None'}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Reason: {result.reason}")
        print(f"   Patterns: {', '.join(result.detected_patterns)}")
        
        if result.domain_name:
            clean = analyzer.extract_clean_domain_name(result.domain_name)
            print(f"   Clean name: {clean}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_analyzer()

