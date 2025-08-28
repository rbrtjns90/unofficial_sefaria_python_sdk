Examples
========

The SDK includes comprehensive examples demonstrating various use cases. All examples are tested and working with the current Sefaria API.

Basic Usage Examples
--------------------

Text Retrieval
~~~~~~~~~~~~~~

.. code-block:: python

   from sefaria_sdk import SefariaClient
   
   client = SefariaClient()
   
   # Get a single verse
   text = client.get_text("Genesis 1:1")
   print(f"Reference: {text['ref']}")
   print(f"Text: {text['versions'][0]['text']}")
   
   # Get multiple verses
   text = client.get_text("Psalms 23:1-6")
   verses = text['versions'][0]['text']
   for i, verse in enumerate(verses, 1):
       print(f"Verse {i}: {verse}")

Language-Specific Retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get Hebrew text
   hebrew_text = client.get_text("Genesis 1:1", lang="he")
   
   # Get specific English version
   english_text = client.get_text("Genesis 1:1", lang="en", version="JPS 1917")
   
   # Process both languages
   from sefaria_sdk.text_processing import TextProcessor
   
   hebrew_verses = TextProcessor.extract_verses(hebrew_text)
   english_verses = TextProcessor.extract_verses(english_text)
   
   parallel = TextProcessor.get_parallel_texts(hebrew_verses, english_verses)
   for he, en in parallel:
       print(f"{he} | {en}")

Command Line Interface
----------------------

The CLI tool provides quick access to Sefaria texts from the command line:

.. code-block:: bash

   # Search for texts
   python examples/04_cli/sefaria_cli.py search "charity" -n 5
   
   # Get specific text
   python examples/04_cli/sefaria_cli.py get-text "Genesis 1:1"
   
   # View today's calendar
   python examples/04_cli/sefaria_cli.py today

Web Application
---------------

A Flask web application that displays the weekly Torah portion:

.. code-block:: bash

   python examples/02_web_app/flask_torah_app.py
   # Visit http://localhost:5000

Features:
- Automatically fetches current parsha
- Shows parallel Hebrew and English text
- Responsive layout with proper Hebrew text alignment

Async Text Processing
---------------------

For bulk operations, use the async client:

.. code-block:: python

   import asyncio
   import aiohttp
   from sefaria_sdk import SefariaClient
   
   async def fetch_multiple_texts():
       refs = ["Genesis 1:1", "Genesis 1:2", "Genesis 1:3"]
       
       async with aiohttp.ClientSession() as session:
           tasks = []
           for ref in refs:
               # Create async tasks for concurrent fetching
               task = fetch_text_async(session, ref)
               tasks.append(task)
           
           results = await asyncio.gather(*tasks)
           return results
   
   # Run the async function
   results = asyncio.run(fetch_multiple_texts())

Data Export
-----------

Export texts to various formats:

.. code-block:: python

   from examples.data_export.text_exporter import TextExporter
   
   exporter = TextExporter()
   
   # Export to JSON
   exporter.export_to_json("Genesis 1", "genesis_1.json")
   
   # Export to CSV
   exporter.export_to_csv("Psalms 23", "psalm_23.csv")
   
   # Export to PDF
   exporter.export_to_pdf("Genesis 1", "genesis_1.pdf")

Research and Analysis
---------------------

Text analysis tools for research:

.. code-block:: python

   from examples.research.text_analysis import TextAnalyzer
   
   analyzer = TextAnalyzer()
   
   # Analyze word frequency
   text = client.get_text("Genesis 1")
   frequency = analyzer.word_frequency(text)
   
   # Find cross-references
   related = client.get_related("Genesis 1:1")
   analyzer.analyze_cross_references(related)

Modern API Features
-------------------

Showcase of modernized SDK features:

.. code-block:: python

   # Enhanced search with highlighting
   results = client.search(
       "creation",
       limit=10,
       field="exact",
       sort_type="relevance"
   )
   
   # Get related content
   related = client.get_related("Genesis 1:1")
   
   # Get available languages
   languages = client.get_languages()
   print(f"Available languages: {list(languages.keys())}")

Running Examples
----------------

All examples are located in the ``examples/`` directory:

.. code-block:: bash

   # Install example dependencies
   pip install flask pandas fpdf rich aiohttp
   
   # Run any example
   cd examples/[example_directory]
   python [script_name].py

Example Structure
-----------------

- ``01_basic_usage/`` - Basic text retrieval and processing
- ``02_web_app/`` - Flask web application
- ``03_research/`` - Text analysis tools
- ``04_cli/`` - Command line interface
- ``05_async/`` - Asynchronous text fetching
- ``06_data_export/`` - Multi-format text export
- ``06_improved_api/`` - Modern API feature showcase

All examples include:
- Comprehensive error handling
- Proper logging
- Clear documentation
- Working with current API endpoints
