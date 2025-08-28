Quick Start Guide
=================

Basic Usage
-----------

Initialize the Client
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sefaria_sdk import SefariaClient
   
   # Default configuration
   client = SefariaClient()
   
   # Custom configuration
   client = SefariaClient(
       base_url="https://www.sefaria.org/api",
       user_agent="MyApp/1.0"
   )

Text Retrieval
~~~~~~~~~~~~~~

.. code-block:: python

   # Get a single verse
   text = client.get_text("Genesis 1:1")
   print(text['versions'][0]['text'])
   
   # Get text with specific parameters
   text = client.get_text(
       "Genesis 1:1-3",
       lang="en",
       version="JPS 1917"
   )
   
   # Get Hebrew text
   hebrew_text = client.get_text("Genesis 1:1", lang="he")

Search Functionality
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Basic search
   results = client.search("charity")
   
   # Advanced search with parameters
   results = client.search(
       "charity",
       limit=10,
       field="exact",
       sort_type="relevance"
   )
   
   # Process search results
   for hit in results['hits']['hits']:
       ref = hit['_source']['ref']
       print(f"Found: {ref}")

Related Content
~~~~~~~~~~~~~~

.. code-block:: python

   # Get related texts and commentaries
   related = client.get_related("Genesis 1:1")
   
   for link in related['links']:
       print(f"Related: {link['ref']}")

Text Processing
--------------

The SDK includes utilities for processing Hebrew and English texts:

.. code-block:: python

   from sefaria_sdk.text_processing import TextProcessor
   
   # Extract verses from API response
   text_data = client.get_text("Genesis 1:1-3")
   verses = TextProcessor.extract_verses(text_data)
   
   # Format Hebrew text
   hebrew = "בְּרֵאשִׁית"
   formatted = TextProcessor.format_hebrew(hebrew)
   
   # Create parallel Hebrew/English texts
   hebrew_verses = ["בְּרֵאשִׁית", "בָּרָא אֱלֹהִים"]
   english_verses = ["In the beginning", "God created"]
   parallel = TextProcessor.get_parallel_texts(hebrew_verses, english_verses)
   
   for he, en in parallel:
       print(f"{he} | {en}")

Error Handling
--------------

.. code-block:: python

   from requests.exceptions import HTTPError, RequestException
   
   try:
       text = client.get_text("Invalid Reference")
   except HTTPError as e:
       print(f"HTTP Error: {e}")
   except RequestException as e:
       print(f"Request Error: {e}")

Best Practices
--------------

1. **Reuse Client Instances**: The client uses connection pooling for efficiency
2. **Handle Errors Gracefully**: Always wrap API calls in try/except blocks
3. **Use Specific Parameters**: Specify language and version for consistent results
4. **Respect Rate Limits**: The client includes automatic retry logic
5. **Cache Results**: Store frequently accessed texts locally when possible

Next Steps
----------

* Explore the :doc:`examples` for real-world usage patterns
* Check the :doc:`api_reference` for complete method documentation
* Review the examples directory in the repository for working code
