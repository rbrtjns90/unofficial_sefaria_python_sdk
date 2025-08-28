"""
Example demonstrating the text processing utilities in the Sefaria SDK.
Shows how to handle Hebrew text, align parallel translations, and format text for display.
"""

from sefaria_sdk import SefariaClient, TextProcessor
from typing import List, Tuple, Dict, Any
import logging
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def display_parallel_texts(pairs: List[Tuple[str, str]], title: str = "") -> None:
    """Display Hebrew and Spanish texts side by side."""
    if title:
        print(f"\n=== {title} ===")
    print("\nHebrew".ljust(40) + "| Spanish")
    print("-" * 80)

    for hebrew, spanish in pairs:
        # Clean and format both texts
        hebrew = TextProcessor.format_hebrew(hebrew) if hebrew else ""
        spanish = TextProcessor.clean_text(spanish) if spanish else ""

        # Display with fixed width for alignment
        print(f"{hebrew[:40].ljust(40)} | {spanish}")


def main():
    """Main demo function."""
    client = SefariaClient()

    try:
        # Get the first chapter of Genesis in both languages
        ref = "Genesis 1:1-5"  # Let's get just the first 5 verses
        logger.info(f"Fetching {ref}...")

        # Get Hebrew text (default version)
        hebrew_response = client.get_text(
            ref,
            version="Miqra Mevoar, trans. and edited by David Kokhav, Jerusalem 2020",
        )
        logger.debug(f"Hebrew response: {json.dumps(hebrew_response, indent=2)}")
        # spanish_response = client.get_text(ref, version="El Pentateuco Con El Comentario de Rabí Shelomó Itzjakí (Rashí) [es]")
        # hebrew_response = client.get_text(ref, version="Miqra Mevoar, trans. and edited by David Kokhav, Jerusalem 2020")

        # Get Spanish text
        spanish_response = client.get_text(
            ref,
            version="El Pentateuco Con El Comentario de Rabí Shelomó Itzjakí (Rashí) [es]",  # Request Spanish
        )
        logger.debug(f"Spanish response: {json.dumps(spanish_response, indent=2)}")

        # Extract verses using TextProcessor
        hebrew_verses = []
        spanish_verses = []

        # Try to get text directly first
        if "text" in hebrew_response:
            hebrew_verses = hebrew_response["text"]
        if "text" in spanish_response:
            spanish_verses = spanish_response["text"]

        # If no verses found in direct text, try versions array
        if not hebrew_verses and "versions" in hebrew_response:
            for version in hebrew_response["versions"]:
                if version.get("version") == "he" and "text" in version:
                    hebrew_verses = version["text"]
                    break

        if not spanish_verses and "versions" in spanish_response:
            for version in spanish_response["versions"]:
                if version.get("version") == "es" and "text" in version:
                    spanish_verses = version["text"]
                    break

        logger.info(
            f"Found {len(hebrew_verses)} Hebrew verses and {len(spanish_verses)} Spanish verses"
        )
        logger.debug(f"Hebrew verses: {hebrew_verses}")
        logger.debug(f"Spanish verses: {spanish_verses}")

        # Get parallel texts
        verse_pairs = TextProcessor.get_parallel_texts(hebrew_verses, spanish_verses)

        # Display the verses
        display_parallel_texts(verse_pairs, ref)

        # Example of handling a single verse
        single_verse_ref = "Genesis 1:1"
        logger.info(f"\nFetching single verse: {single_verse_ref}")

        hebrew_single = client.get_text(single_verse_ref, version="he")
        spanish_single = client.get_text(single_verse_ref, version="es")

        logger.debug(f"Single Hebrew response: {json.dumps(hebrew_single, indent=2)}")
        logger.debug(f"Single Spanish response: {json.dumps(spanish_single, indent=2)}")

        # Extract and pair single verses
        hebrew_verse = []
        spanish_verse = []

        # Try to get text directly first
        if "text" in hebrew_single:
            hebrew_verse = [hebrew_single["text"]]
        if "text" in spanish_single:
            spanish_verse = [spanish_single["text"]]

        # If no verses found in direct text, try versions array
        if not hebrew_verse and "versions" in hebrew_single:
            for version in hebrew_single["versions"]:
                if version.get("version") == "he" and "text" in version:
                    hebrew_verse = version["text"]
                    break

        if not spanish_verse and "versions" in spanish_single:
            for version in spanish_single["versions"]:
                if version.get("version") == "es" and "text" in version:
                    spanish_verse = version["text"]
                    break

        logger.debug(f"Single Hebrew verse: {hebrew_verse}")
        logger.debug(f"Single Spanish verse: {spanish_verse}")

        single_pair = [
            (
                hebrew_verse[0] if hebrew_verse else "",
                spanish_verse[0] if spanish_verse else "",
            )
        ]

        display_parallel_texts(single_pair, "Genesis 1:1 (Single Verse)")

        # Example of cleaning messy text
        messy_text = "This   is  a  messy    text   with extra   spaces  ."
        clean_text = TextProcessor.clean_text(messy_text)
        print(f"\n=== Text Cleaning Example ===")
        print(f"Original: {messy_text}")
        print(f"Cleaned:  {clean_text}")

    except Exception as e:
        logger.error(f"Error in demo: {str(e)}")
        raise


if __name__ == "__main__":
    main()
