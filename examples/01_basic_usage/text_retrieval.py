"""
Basic examples of retrieving texts from Sefaria.
"""
from sefaria_sdk import SefariaClient
from pprint import pprint

def main():
    # Initialize the client
    client = SefariaClient()

    '''# Get text in English
    print("\nRetrieving Genesis 1:1 in English:")
    genesis_en = client.get_text("Genesis 1:1")
    pprint(genesis_en)'''

    """ # Get text in Hebrew
    print("\nRetrieving Genesis 1:1 in Hebrew:")
    genesis_he = client.get_text("Genesis 1:1", version="hebrew")
    pprint(genesis_he) """

    # Get an entire chapter
    print("\nRetrieving Psalm 23:")
    psalm_23 = client.get_text("Psalms 23")
    pprint(psalm_23)

    '''# Get text with a specific version
    print("\nRetrieving Rashi on Genesis 1:1:")
    rashi = client.get_text("Genesis 1:1", version="en|Rashi")
    pprint(rashi)'''

if __name__ == "__main__":
    main()
