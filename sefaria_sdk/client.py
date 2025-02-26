import requests
from typing import Optional, List, Dict, Union, Any
from urllib.parse import quote

class SefariaClient:
    """Client for interacting with the Sefaria API."""
    
    def __init__(self, base_url: str = "https://www.sefaria.org/api"):
        """Initialize the Sefaria client.
        
        Args:
            base_url: Base URL for the Sefaria API. Defaults to https://www.sefaria.org/api
        """
        self.base_url = base_url.rstrip('/')
        
    def get_text(self, tref: str, version: Optional[str] = None, 
                 fill_in_missing_segments: bool = False,
                 return_format: str = "default") -> Dict:
        """Get a text from Sefaria.
        
        Args:
            tref: A Sefaria-specific reference
            version: Optional version specification (language or language|versionTitle)
            fill_in_missing_segments: Whether to fill in missing segments from other versions
            return_format: One of ["default", "text_only", "strip_only_footnotes", "wrap_all_entities"]
            
        Returns:
            Dict containing the requested text and metadata
        """
        endpoint = f"{self.base_url}/v3/texts/{quote(tref)}"
        params = {}
        
        if version:
            params["version"] = version
        if fill_in_missing_segments:
            params["fill_in_missing_segments"] = "1"
        if return_format != "default":
            params["return_format"] = return_format
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_versions(self, index: str) -> List[Dict]:
        """Get all available versions of a text.
        
        Args:
            index: A valid Sefaria index title
            
        Returns:
            List of dictionaries containing version metadata
        """
        endpoint = f"{self.base_url}/texts/versions/{quote(index)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_manuscripts(self, tref: str) -> Dict:
        """Get manuscript data for a text reference.
        
        Args:
            tref: A valid Sefaria text reference
            
        Returns:
            Dict containing manuscript data and metadata
        """
        endpoint = f"{self.base_url}/manuscripts/{quote(tref)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_random_text(self, titles: Optional[str] = None, 
                       categories: Optional[str] = None) -> Dict:
        """Get a random text reference.
        
        Args:
            titles: Optional pipe-separated string of book titles
            categories: Optional pipe-separated string of categories
            
        Returns:
            Dict containing random text reference
        """
        endpoint = f"{self.base_url}/texts/random"
        params = {}
        
        if titles:
            params["titles"] = titles
        if categories:
            params["categories"] = categories
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_index(self, index_title: str) -> Dict:
        """Get the full index record for a text.
        
        Args:
            index_title: Title of a valid Sefaria index
            
        Returns:
            Dict containing the full index record
        """
        endpoint = f"{self.base_url}/v2/raw/index/{quote(index_title)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_table_of_contents(self) -> Dict:
        """Get the complete table of contents.
        
        Returns:
            Dict containing the complete table of contents
        """
        endpoint = f"{self.base_url}/index"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_ref_topic_links(self, tref: str) -> Dict:
        """Get topic links for a text reference.
        
        Args:
            tref: A valid Sefaria text reference
            
        Returns:
            Dict containing topic links
        """
        endpoint = f"{self.base_url}/ref-topic-links/{quote(tref)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_translations(self, lang: str) -> Dict:
        """Get translations in a specific language.
        
        Args:
            lang: ISO 639-1 language code
            
        Returns:
            Dict containing translations organized by category
        """
        endpoint = f"{self.base_url}/texts/translations/{quote(lang)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_languages(self) -> Dict:
        """Get list of available languages.
        
        Returns:
            Dict containing available languages
        """
        endpoint = f"{self.base_url}/texts/languages"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def search(self, query: str, type: str = "text", field: Optional[str] = None,
              exact: bool = False, offset: int = 0, limit: int = 10,
              filters: Optional[List[str]] = None, filter_fields: Optional[List[str]] = None,
              aggs: Optional[List[str]] = None, sort_type: Optional[str] = None,
              sort_dir: Optional[str] = None, applied_filters: Optional[List[str]] = None,
              applied_filter_fields: Optional[List[str]] = None,
              group_related: bool = False, with_refs: bool = False) -> Dict:
        """Search Sefaria's library of texts and source sheets.
        
        Args:
            query: The search query string
            type: Type of search ("text" or "sheet")
            field: Field to search in (e.g., "content" for sheets)
            exact: Whether to perform exact match
            offset: Number of results to skip
            limit: Maximum number of results to return
            filters: List of filters to apply
            filter_fields: Fields to apply filters to
            aggs: List of aggregations to return
            sort_type: Type of sorting
            sort_dir: Sort direction
            applied_filters: Already applied filters
            applied_filter_fields: Fields for applied filters
            group_related: Whether to group related results
            with_refs: Whether to include references
            
        Returns:
            Dict containing search results
        """
        endpoint = f"{self.base_url}/search"
        params = {
            "q": query,
            "type": type,
            "offset": offset,
            "limit": limit
        }
        
        if field:
            params["field"] = field
        if exact:
            params["exact"] = 1
        if filters:
            params["filters"] = filters
        if filter_fields:
            params["filter_fields"] = filter_fields
        if aggs:
            params["aggs"] = aggs
        if sort_type:
            params["sort_type"] = sort_type
        if sort_dir:
            params["sort_dir"] = sort_dir
        if applied_filters:
            params["applied_filters"] = applied_filters
        if applied_filter_fields:
            params["applied_filter_fields"] = applied_filter_fields
        if group_related:
            params["group_related"] = 1
        if with_refs:
            params["with_refs"] = 1
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_counts(self, title: str) -> Dict:
        """Get counts of available texts for a given title.
        
        Args:
            title: Title to get counts for
            
        Returns:
            Dict containing text counts
        """
        endpoint = f"{self.base_url}/counts/{quote(title)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_text_list(self) -> Dict:
        """Get a list of all available texts.
        
        Returns:
            Dict containing list of texts
        """
        endpoint = f"{self.base_url}/texts/list"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_links(self, tref: str) -> Dict:
        """Get links for a text reference.
        
        Args:
            tref: Text reference to get links for
            
        Returns:
            Dict containing links
        """
        endpoint = f"{self.base_url}/links/{quote(tref)}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_link_summary(self, tref: str) -> Dict:
        """Get a summary of links for a text reference.
        
        Args:
            tref: Text reference to get link summary for
            
        Returns:
            Dict containing link summary
        """
        endpoint = f"{self.base_url}/links/{quote(tref)}/summary"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_history(self, tref: str, language: Optional[str] = None,
                   version: Optional[str] = None) -> Dict:
        """Get history for a text reference.
        
        Args:
            tref: Text reference to get history for
            language: Optional language filter
            version: Optional version filter
            
        Returns:
            Dict containing text history
        """
        endpoint = f"{self.base_url}/history/{quote(tref)}"
        params = {}
        
        if language:
            params["language"] = language
        if version:
            params["version"] = version
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_calendar_items(self, timezone: Optional[str] = None,
                         custom: Optional[str] = None) -> Dict:
        """Get calendar items.
        
        Args:
            timezone: Optional timezone
            custom: Optional custom calendar items
            
        Returns:
            Dict containing calendar items
        """
        endpoint = f"{self.base_url}/calendars"
        params = {}
        
        if timezone:
            params["timezone"] = timezone
        if custom:
            params["custom"] = custom
            
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def get_ref_data(self, refs: List[str]) -> Dict:
        """Get data for multiple text references.
        
        Args:
            refs: List of text references
            
        Returns:
            Dict containing reference data
        """
        endpoint = f"{self.base_url}/bulktext"
        response = requests.post(endpoint, json={"refs": refs})
        response.raise_for_status()
        return response.json()
