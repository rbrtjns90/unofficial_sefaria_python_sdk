"""
Example demonstrating multilingual text retrieval using the improved SDK.

Demonstrates:
- Enhanced get_text() with language parameters
- Available translation languages discovery
- Bilingual and multilingual text retrieval
"""

from sefaria_sdk import SefariaClient
import json


def demonstrate_language_discovery():
    """Show available translation languages using the fixed endpoint."""
    client = SefariaClient(user_agent="Language-Demo/1.0")

    print("Available translation languages:")
    try:
        languages = client.get_languages()
        print(f"Found {len(languages)} languages: {', '.join(languages)}")
        return languages
    except Exception as e:
        print(f"Error getting languages: {e}")
        return []


def get_multilingual_text(ref: str, languages: list) -> dict:
    """
    Retrieve text in multiple languages using the enhanced API.

    Args:
        ref (str): The reference to retrieve (e.g., "Genesis 1:1")
        languages (list): List of language codes to retrieve

    Returns:
        dict: The API response containing multilingual text
    """
    client = SefariaClient(user_agent="Multilingual-Text-Demo/1.0")
    lang_param = ",".join(languages)
    response = client.get_text(ref, language=lang_param, context=0)
    return response


def main():
    """Main demo function showing multilingual text retrieval."""
    # Discover available languages
    available_langs = demonstrate_language_discovery()

    # Example reference
    ref = "Genesis 1:1"

    # Try common languages that are likely available
    target_languages = ["he", "en"]

    # Add other languages if available
    for lang in ["es", "fr", "de", "ru"]:
        if lang in available_langs:
            target_languages.append(lang)
            if len(target_languages) >= 4:  # Limit to 4 languages
                break

    print(f"\n{'='*60}")
    print(f"Retrieving {ref} in languages: {', '.join(target_languages)}")
    print(f"{'='*60}")

    try:
        response = get_multilingual_text(ref, target_languages)

        if "versions" in response:
            print(f"\nFound {len(response['versions'])} versions:")
            for version in response["versions"]:
                lang = version.get("language", "unknown")
                title = version.get("versionTitle", "Unknown Version")
                text = (
                    version.get("text", [""])[0] if version.get("text") else "No text"
                )

                print(f"\n{lang.upper()}: {title}")
                print(f"Text: {text}")
        else:
            print("No versions found in response")

    except Exception as e:
        print(f"Error getting multilingual text: {e}")

    # Demonstrate specific language translation retrieval
    print(f"\n{'='*60}")
    print("Available translations by language:")
    print(f"{'='*60}")

    client = SefariaClient(user_agent="Translation-Demo/1.0")
    for lang in ["en", "es", "fr"][:2]:  # Limit to 2 for brevity
        if lang in available_langs:
            try:
                translations = client.get_translations(lang)
                print(
                    f"\n{lang.upper()} translations available: {len(translations)} categories"
                )
                # Show first few categories
                for category in list(translations.keys())[:3]:
                    count = len(translations[category])
                    print(f"  {category}: {count} texts")
            except Exception as e:
                print(f"Error getting {lang} translations: {e}")


if __name__ == "__main__":
    main()
