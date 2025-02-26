"""
Example demonstrating how to retrieve specific verses in different languages from Sefaria.
"""
from sefaria_sdk import SefariaClient
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_verse_by_language(ref: str, language: str) -> dict:
    """
    Retrieve a specific verse in the requested language.
    
    Args:
        ref (str): The reference to retrieve (e.g., "Genesis 1:1")
        language (str): The language to retrieve the text in
        
    Returns:
        dict: The API response containing the text
    """
    client = SefariaClient()
    response = client.get_text(ref, version=language)
    return response

def main():
    """Main demo function showing verse retrieval in different languages."""
    # Example reference
    ref = "Genesis 1:1"
    
    # List of languages to try
    languages = ["hebrew", "english", "spanish", "french", "german"]
    
    for language in languages:
        logger.info(f"\nTrying to get {ref} in {language}:")
        try:
            response = get_verse_by_language(ref, language)
            logger.info(f"Response for {language}:")
            logger.info(json.dumps(response, indent=2))
        except Exception as e:
            logger.error(f"Error getting {language} text: {str(e)}")

if __name__ == "__main__":
    main()