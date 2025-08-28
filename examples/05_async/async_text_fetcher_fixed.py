"""
Example of asynchronous text fetching using aiohttp.
"""

import asyncio
import aiohttp
from typing import List, Dict
from urllib.parse import quote
import json


class AsyncSefariaClient:
    def __init__(self, base_url: str = "https://www.sefaria.org/api"):
        self.base_url = base_url.rstrip("/")

    async def get_text(
        self,
        session: aiohttp.ClientSession,
        tref: str,
        version_title: str = None,
        lang: str = None,
    ) -> Dict:
        """Fetch a single text asynchronously."""
        if version_title and lang:
            # Use the /texts/ endpoint with version in URL path
            url = f"{self.base_url}/texts/{quote(tref)}/{quote(version_title)}/{lang}"
            params = None
        else:
            # Use the v3/texts endpoint with parameters
            url = f"{self.base_url}/v3/texts/{quote(tref)}"
            params = {}
            if lang:
                params["lang"] = lang

        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                # Return empty dict on error to avoid breaking the flow
                return {}

    async def bulk_fetch_texts(
        self, refs: List[str], version_title: str = None, lang: str = None
    ) -> List[Dict]:
        """Fetch multiple texts concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_text(session, ref, version_title, lang) for ref in refs]
            return await asyncio.gather(*tasks)

    async def get_english_version_title(
        self, session: aiohttp.ClientSession, book: str
    ) -> str:
        """Get the first available English version title for a book."""
        async with session.get(
            f"{self.base_url}/texts/versions/{quote(book)}"
        ) as response:
            versions = await response.json()
            for version in versions:
                if version.get("language") == "en":
                    return version.get("versionTitle", "")
            return None


async def main():
    # Initialize client
    client = AsyncSefariaClient()

    # List of texts to fetch
    texts_to_fetch = [
        "Genesis 1:1",
        "Exodus 1:1",
        "Leviticus 1:1",
        "Numbers 1:1",
        "Deuteronomy 1:1",
    ]

    # First, get metadata to find English versions
    print("Getting version information...")
    async with aiohttp.ClientSession() as session:
        # Get unique book names from references
        books = list(set(ref.split()[0] for ref in texts_to_fetch))
        version_tasks = [
            client.get_english_version_title(session, book) for book in books
        ]
        english_versions = await asyncio.gather(*version_tasks)

        # Create book to version mapping
        book_versions = dict(zip(books, english_versions))

    # Fetch English and Hebrew texts concurrently
    print("Fetching English and Hebrew texts...")

    async with aiohttp.ClientSession() as session:
        # Create tasks for English texts with specific versions
        english_tasks = []
        hebrew_tasks = []

        for ref in texts_to_fetch:
            book = ref.split()[0]
            version_title = book_versions.get(book)

            # English task with specific version
            if version_title:
                english_tasks.append(client.get_text(session, ref, version_title, "en"))
            else:
                english_tasks.append(client.get_text(session, ref, lang="en"))

            # Hebrew task
            hebrew_tasks.append(client.get_text(session, ref, lang="he"))

        # Gather results
        english_texts, hebrew_texts = await asyncio.gather(
            asyncio.gather(*english_tasks), asyncio.gather(*hebrew_tasks)
        )

    # Print results
    print("\nResults:")
    for i, (ref, en_data, he_data) in enumerate(
        zip(texts_to_fetch, english_texts, hebrew_texts)
    ):
        print(f"\n{ref}:")

        # Handle English text (direct text field for /texts/ endpoint)
        if "text" in en_data:
            text = en_data["text"]
            if isinstance(text, list) and text:
                text = text[0]  # Take first verse/segment
            # Clean up HTML tags for display
            import re

            text = re.sub(r"<[^>]+>", "", text)
            print(f"English: {text}")
        else:
            print("English: No English text available")

        # Handle Hebrew text (from versions array)
        hebrew_found = False
        if "versions" in he_data and he_data["versions"]:
            for version in he_data["versions"]:
                if version.get("language") == "he" and "text" in version:
                    text = version["text"]
                    if isinstance(text, list) and text:
                        text = text[0]  # Take first verse/segment
                    print(f"Hebrew:  {text}")
                    hebrew_found = True
                    break

        if not hebrew_found:
            print("Hebrew:  No Hebrew text available")


if __name__ == "__main__":
    asyncio.run(main())
