#!/usr/bin/env python3
"""
Demonstration of the improved Sefaria SDK with modern API endpoints.

This script showcases:
1. Fixed get_languages() using /texts/translations endpoint
2. Modern search() using POST /search-wrapper
3. New get_related() method for related content
4. Robust client with retries, timeouts, and proper headers
5. Parameter pass-through for Texts v3 API
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sefaria_sdk.client import SefariaClient

def demo_modern_features():
    """Demonstrate the improved SDK features."""
    
    # Initialize client with custom user agent
    client = SefariaClient(user_agent="Modern-SDK-Demo/1.0")
    
    print("=== Modern Sefaria SDK Demo ===\n")
    
    # 1. Get available translation languages (fixed endpoint)
    print("1. Available translation languages:")
    try:
        languages = client.get_languages()
        print(f"   Found {len(languages)} languages: {', '.join(languages[:10])}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 2. Enhanced text retrieval with v3 parameters
    print("\n2. Enhanced text retrieval (with language parameters):")
    try:
        text = client.get_text("Genesis 1:1", language="he,en", context=0)
        if 'versions' in text:
            for version in text['versions']:
                lang = version.get('language', 'unknown')
                title = version.get('versionTitle', 'Unknown Version')
                print(f"   {lang}: {title}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 3. Modern search using search-wrapper
    print("\n3. Modern search (using search-wrapper):")
    try:
        results = client.search(
            query="Genesis",  # Use English for better results
            type="text",
            field="naive_lemmatizer",  # More flexible matching
            limit=5
        )
        
        # Handle the correct search response structure
        if 'hits' in results and 'hits' in results['hits']:
            hits = results['hits']['hits']
            # Handle different total field formats
            total_info = results['hits'].get('total', 0)
            if isinstance(total_info, dict):
                total = total_info.get('value', len(hits))
            else:
                total = total_info if isinstance(total_info, int) else len(hits)
            
            print(f"   Found {total} results:")
            for hit in hits[:3]:
                # Extract reference from _id field and clean it
                ref = hit.get('_id', 'Unknown ref')
                if '(' in ref:
                    ref = ref.split('(')[0].strip()
                print(f"   - {ref}")
        else:
            print("   Found 0 results")
    except Exception as e:
        print(f"   Found 0 results:")
        print(f"   Error: {e}")
    
    # 4. Get related content using modern API
    print("\n4. Related content (modern Related API):")
    try:
        related = client.get_related("Genesis 1:1")
        if 'topics' in related:
            topics = related['topics'][:3]  # First 3 topics
            print(f"   Related topics:")
            for topic in topics:
                title = topic.get('title', {}).get('en', 'Unknown topic')
                print(f"   - {title}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 5. Calendar integration
    print("\n5. Today's calendar items:")
    try:
        calendar = client.get_calendar_items()
        if 'items' in calendar:
            for item in calendar['items'][:3]:
                title = item.get('title', 'Unknown item')
                ref = item.get('ref', '')
                print(f"   - {title} ({ref})")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Demo Complete ===")

def demo_parasha_outline():
    """Create a Parasha outline as suggested in the analysis."""
    
    client = SefariaClient()
    
    print("\n=== Weekly Parasha Outline ===\n")
    
    try:
        # Get today's calendar
        cal = client.get_calendar_items()
        
        # Find the Parasha
        parasha_ref = None
        for item in cal.get('items', []):
            title = item.get('title', '').lower()
            if 'parashat' in title or 'parsha' in title:
                parasha_ref = item.get('ref')
                parasha_name = item.get('title')
                break
        
        if not parasha_ref:
            print("No Parasha found in today's calendar")
            return
        
        print(f"This week's Parasha: {parasha_name}")
        print(f"Reference: {parasha_ref}")
        
        # Get the opening verse
        opening_verse = f"{parasha_ref.split('-')[0]} 1:1"  # First verse of first chapter
        print(f"\nOpening verse: {opening_verse}")
        
        try:
            text = client.get_text(opening_verse, language="he,en")
            if 'versions' in text:
                for version in text['versions']:
                    lang = version.get('language')
                    if lang in ['he', 'en'] and version.get('text'):
                        print(f"  {lang.upper()}: {version['text'][0] if version['text'] else 'N/A'}")
        except Exception as e:
            print(f"  Error getting text: {e}")
        
        # Get commentary links
        try:
            links = client.get_links(opening_verse)
            commentary_refs = [
                link['ref'] for link in links 
                if link.get('type') == 'commentary'
            ][:3]  # First 3 commentaries
            
            if commentary_refs:
                print(f"\nClassic commentaries on {opening_verse}:")
                for ref in commentary_refs:
                    print(f"  - {ref}")
            
        except Exception as e:
            print(f"Error getting commentaries: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    demo_modern_features()
    demo_parasha_outline()
