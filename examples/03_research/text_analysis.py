"""
Example of analyzing texts for research purposes using the improved SDK.

Demonstrates:
- Enhanced text retrieval with language parameters
- Modern search functionality
- Related content analysis
- Robust error handling
"""

from sefaria_sdk import SefariaClient
from collections import Counter
from typing import Dict, List, Tuple
import re


class TextAnalyzer:
    def __init__(self):
        self.client = SefariaClient(user_agent="Text-Analysis-Research/1.0")

    def _get_text_content(self, response: Dict, language: str = "en") -> str:
        """Extract text content from API response using v3 format."""
        if "versions" in response:
            for version in response["versions"]:
                if version.get("language") == language:
                    text = version.get("text", "")
                    if isinstance(text, list):
                        return " ".join(text)
                    return text
        return ""

    def analyze_word_frequency(
        self, text_ref: str, language: str = "en"
    ) -> Dict[str, int]:
        """Analyze word frequency in a text using enhanced API."""
        # Get the text with specific language parameter
        response = self.client.get_text(text_ref, language=language)

        # Extract text content
        text = self._get_text_content(response, language)

        if not text:
            print(f"No {language} text found for {text_ref}")
            return {}

        # Split into words and count frequency
        words = re.findall(r"\w+", text.lower())
        return dict(Counter(words))

    def find_common_links(self, text_ref: str) -> List[Tuple[str, int]]:
        """Find most commonly linked texts."""
        try:
            # Get all links for the text
            links = self.client.get_links(text_ref)

            # Count references
            refs = []
            if isinstance(links, list):
                refs = [link.get("ref", "") for link in links if link.get("ref")]
            elif isinstance(links, dict) and "links" in links:
                refs = [
                    link.get("ref", "") for link in links["links"] if link.get("ref")
                ]

            ref_counts = Counter(refs)
            return ref_counts.most_common(10)
        except Exception as e:
            print(f"Error getting links for {text_ref}: {e}")
            return []

    def compare_translations(self, text_ref: str) -> Dict[str, str]:
        """Compare different translations using enhanced API."""
        try:
            # Get text with multiple languages
            response = self.client.get_text(text_ref, language="en,he")

            # Get all versions
            translations = {}
            if "versions" in response:
                for version in response["versions"]:
                    lang = version.get("language", "unknown")
                    title = version.get("versionTitle", "Unknown")
                    text = version.get("text", "")
                    if isinstance(text, list):
                        text = " ".join(text)
                    if text:  # Only include non-empty translations
                        key = f"{title} ({lang})"
                        translations[key] = text

            return translations
        except Exception as e:
            print(f"Error getting translations for {text_ref}: {e}")
            return {}

    def analyze_related_topics(self, text_ref: str) -> List[str]:
        """Analyze related topics using the modern Related API."""
        try:
            related = self.client.get_related(text_ref)
            topics = []
            if "topics" in related:
                for topic in related["topics"]:
                    title = topic.get("title", {})
                    if isinstance(title, dict):
                        topic_name = title.get("en", title.get("he", "Unknown"))
                    else:
                        topic_name = str(title)
                    topics.append(topic_name)
            return topics[:10]  # Return top 10 topics
        except Exception as e:
            print(f"Error getting related topics for {text_ref}: {e}")
            return []

    def search_related_passages(self, query: str, limit: int = 5) -> List[str]:
        """Search for passages related to a query using modern search."""
        try:
            results = self.client.search(
                query=query, type="text", field="naive_lemmatizer", limit=limit
            )

            passages = []
            # Handle different response formats
            if isinstance(results, dict) and "hits" in results:
                for hit in results["hits"]:
                    if isinstance(hit, dict):
                        ref = hit.get("ref", "Unknown")
                        if ref != "Unknown":
                            passages.append(ref)
            elif isinstance(results, list):
                for hit in results:
                    if isinstance(hit, dict):
                        ref = hit.get("ref", "Unknown")
                        if ref != "Unknown":
                            passages.append(ref)
            return passages
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            return []


def main():
    analyzer = TextAnalyzer()

    # Analyze Psalms 23 word frequency - try both English and Hebrew
    print("=" * 60)
    print("Word frequency analysis in Psalms 23:")
    print("=" * 60)

    # Try English first
    freq_en = analyzer.analyze_word_frequency("Psalms 23", "en")
    if freq_en:
        print("English word frequency:")
        for word, count in sorted(freq_en.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]:
            print(f"  {word}: {count}")
    else:
        # Fall back to Hebrew if no English available
        print("No English text available, showing Hebrew word frequency:")
        freq_he = analyzer.analyze_word_frequency("Psalms 23", "he")
        if freq_he:
            for word, count in sorted(
                freq_he.items(), key=lambda x: x[1], reverse=True
            )[:5]:
                print(f"  {word}: {count}")

    # Find common links to Genesis 1
    print("\n" + "=" * 60)
    print("Most referenced texts in relation to Genesis 1:")
    print("=" * 60)
    links = analyzer.find_common_links("Genesis 1")
    for ref, count in links[:5]:  # Show top 5
        if ref:  # Only print non-empty references
            print(f"{ref}: {count} references")

    # Compare translations of a verse
    print("\n" + "=" * 60)
    print("Different translations of Genesis 1:1:")
    print("=" * 60)
    translations = analyzer.compare_translations("Genesis 1:1")
    for version, text in translations.items():
        if text:  # Only print non-empty translations
            print(f"\n{version}:")
            print(f"{text[:200]}..." if len(text) > 200 else text)

    # Analyze related topics
    print("\n" + "=" * 60)
    print("Related topics for Genesis 1:1:")
    print("=" * 60)
    topics = analyzer.analyze_related_topics("Genesis 1:1")
    for i, topic in enumerate(topics[:5], 1):
        print(f"{i}. {topic}")

    # Search for related passages
    print("\n" + "=" * 60)
    print("Passages related to 'creation':")
    print("=" * 60)
    passages = analyzer.search_related_passages("creation", limit=5)
    for i, passage in enumerate(passages, 1):
        print(f"{i}. {passage}")


if __name__ == "__main__":
    main()
