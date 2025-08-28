"""
Basic examples of retrieving texts from Sefaria using the improved SDK.

Demonstrates:
- Enhanced get_text() with parameter pass-through
- Bilingual text retrieval
- Robust client with retries and proper headers
"""

from sefaria_sdk import SefariaClient
from pprint import pprint


def main():
    # Initialize the client with custom user agent
    client = SefariaClient(user_agent="Basic-Usage-Example/1.0")

    # Get text in both Hebrew and English using enhanced API
    print("\nRetrieving Genesis 1:1 in Hebrew and English:")
    genesis = client.get_text("Genesis 1:1", language="he,en", context=0)

    # Display versions found
    if "versions" in genesis:
        for version in genesis["versions"]:
            lang = version.get("language", "unknown")
            title = version.get("versionTitle", "Unknown Version")
            text = version.get("text", [""])[0] if version.get("text") else "No text"
            # Handle HTML entities and empty content
            if text and text != "<":
                display_text = (
                    text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                )
                print(f"\n{lang.upper()}: {title}")
                print(
                    f"Text: {display_text[:100]}..."
                    if len(display_text) > 100
                    else f"Text: {display_text}"
                )
            else:
                print(f"\n{lang.upper()}: {title}")
                print("Text: [No text content available]")

    # Get an entire chapter with language specification
    print("\n" + "=" * 50)
    print("Retrieving Psalm 23 in Hebrew:")
    psalm_23 = client.get_text("Psalms 23", language="he")

    if "versions" in psalm_23:
        for version in psalm_23["versions"]:
            if version.get("language") == "he":
                print(f"\nVersion: {version.get('versionTitle', 'Unknown')}")
                text_array = version.get("text", [])
                for i, verse in enumerate(text_array[:3], 1):  # First 3 verses
                    print(f"Verse {i}: {verse}")

    # Demonstrate error handling with invalid reference
    print("\n" + "=" * 50)
    print("Testing error handling with invalid reference:")
    try:
        invalid = client.get_text("InvalidBook 999:999")
    except Exception as e:
        print(f"Caught expected error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
