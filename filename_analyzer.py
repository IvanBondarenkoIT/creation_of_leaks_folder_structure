"""
Filename Analyzer Module
Intelligent analysis of filenames to detect domains, URLs, and determine file category
"""

import re
from typing import Optional, Tuple
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
        r'\.xyz', r'\.top', r'\.vip', r'\.club', r'\.pro', r'\.tv', r'\.cc'
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
            r'([a-zA-Z0-9-]+)_(?:com|net|org|io|co|ru|de|fr|uk|us|ca|au|it|es|br|gov|edu)',
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
            'hits', 'good', 'ok', 'checked', 'working'
        ]
        
        # Country codes that usually indicate combos
        self.country_codes = [
            'usa', 'uk', 'us', 'eu', 'canada', 'france', 'germany', 'spain',
            'italy', 'poland', 'russia', 'china', 'japan', 'korea', 'brazil',
            'india', 'vietnam', 'indonesia', 'denmark', 'netherlands', 'sweden'
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
        
        # 2. Check for domain.extension pattern
        domain_match = self.domain_pattern.search(filename)
        if domain_match:
            potential_domain = domain_match.group(1)
            # Verify it's not a common combo word with extension-like ending
            if not any(indicator in potential_domain.lower() for indicator in self.combo_indicators):
                domain_name = potential_domain
                category = "Database"
                confidence = "high"
                reason = f"Domain detected: {potential_domain}"
                detected_patterns.append(f"Domain: {potential_domain}")
                return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
        
        # 3. Check for domain_extension pattern (e.g., amazon_com)
        # BUT: Check for combo indicators first to avoid false positives
        combo_count = sum(1 for indicator in self.combo_indicators if indicator in name_lower)
        
        underscore_match = self.domain_underscore_pattern.search(name_lower)
        if underscore_match and combo_count < 2:  # Only if not strong combo file
            potential_domain = underscore_match.group(1)
            # Additional check: is it a known company?
            is_known_company = potential_domain in self.company_indicators
            
            if is_known_company:
                domain_name = potential_domain
                category = "Database"
                confidence = "high"
                reason = f"Domain with underscore detected: {potential_domain}"
                detected_patterns.append(f"Domain_ext: {underscore_match.group(0)}")
                return FileAnalysisResult(category, domain_name, confidence, reason, detected_patterns)
        
        # 4. Check for known company/brand names
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
        
        # 5. Check for strong combo indicators (recount if not done earlier)
        if 'combo_count' not in locals():
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

