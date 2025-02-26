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
        self.base_url = base_url.rstrip('/')
        
    async def get_text(self, session: aiohttp.ClientSession, 
                      tref: str, version: str = None) -> Dict:
        """Fetch a single text asynchronously."""
        params = {}
        if version:
            params['version'] = version
            
        async with session.get(
            f"{self.base_url}/v3/texts/{quote(tref)}", 
            params=params
        ) as response:
            return await response.json()
            
    async def bulk_fetch_texts(self, refs: List[str], 
                             version: str = None) -> List[Dict]:
        """Fetch multiple texts concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.get_text(session, ref, version)
                for ref in refs
            ]
            return await asyncio.gather(*tasks)

async def main():
    # Initialize client
    client = AsyncSefariaClient()
    
    # List of texts to fetch
    texts_to_fetch = [
        "Genesis 1:1",
        "Exodus 1:1",
        "Leviticus 1:1",
        "Numbers 1:1",
        "Deuteronomy 1:1"
    ]
    
    # Fetch texts in English
    print("Fetching English texts...")
    english_texts = await client.bulk_fetch_texts(texts_to_fetch)
    
    # Fetch texts in Hebrew
    print("Fetching Hebrew texts...")
    hebrew_texts = await client.bulk_fetch_texts(texts_to_fetch, version="he")
    
    # Print results
    print("\nResults:")
    for i, (ref, en, he) in enumerate(zip(
        texts_to_fetch, english_texts, hebrew_texts
    )):
        print(f"\n{ref}:")
        print(f"English: {en['text']}")
        print(f"Hebrew:  {he['text']}")

if __name__ == "__main__":
    asyncio.run(main())
