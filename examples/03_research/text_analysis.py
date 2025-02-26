"""
Example of analyzing texts for research purposes.
"""
from sefaria_sdk import SefariaClient
from collections import Counter
from typing import Dict, List, Tuple
import re

class TextAnalyzer:
    def __init__(self):
        self.client = SefariaClient()
    
    def _get_text_content(self, response: Dict) -> str:
        """Extract text content from API response."""
        if 'available_versions' in response:
            for version in response['available_versions']:
                if version['language'] == 'en':
                    text = version.get('text', '')
                    if isinstance(text, list):
                        return ' '.join(text)
                    return text
        return ''
    
    def analyze_word_frequency(self, text_ref: str) -> Dict[str, int]:
        """Analyze word frequency in a text."""
        # Get the text in English
        response = self.client.get_text(text_ref)
        
        # Extract text content
        text = self._get_text_content(response)
        
        # Split into words and count frequency
        words = re.findall(r'\w+', text.lower())
        return dict(Counter(words))
    
    def find_common_links(self, text_ref: str) -> List[Tuple[str, int]]:
        """Find most commonly linked texts."""
        # Get all links for the text
        links = self.client.get_links(text_ref)
        
        # Count references
        refs = []
        if isinstance(links, dict) and 'links' in links:
            refs = [link.get('ref', '') for link in links['links']]
        ref_counts = Counter(refs)
        
        # Return sorted by frequency
        return ref_counts.most_common(10)
    
    def compare_translations(self, text_ref: str) -> Dict[str, str]:
        """Compare different translations of the same text."""
        # Get text with available versions
        response = self.client.get_text(text_ref)
        
        # Get English translations
        translations = {}
        if 'available_versions' in response:
            for version in response['available_versions']:
                if version['language'] == 'en':
                    title = version.get('versionTitle', 'Unknown')
                    text = version.get('text', '')
                    if isinstance(text, list):
                        text = ' '.join(text)
                    translations[title] = text
                    
        return translations

def main():
    analyzer = TextAnalyzer()
    
    # Analyze Psalms 23
    print("Word frequency in Psalms 23:")
    freq = analyzer.analyze_word_frequency("Psalms 23")
    for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{word}: {count}")
    
    # Find common links to Genesis 1
    print("\nMost referenced texts in relation to Genesis 1:")
    links = analyzer.find_common_links("Genesis 1")
    for ref, count in links:
        if ref:  # Only print non-empty references
            print(f"{ref}: {count} references")
    
    # Compare translations of a verse
    print("\nDifferent translations of Genesis 1:1:")
    translations = analyzer.compare_translations("Genesis 1:1")
    for version, text in translations.items():
        if text:  # Only print non-empty translations
            print(f"\n{version}:")
            print(text)

if __name__ == "__main__":
    main()
