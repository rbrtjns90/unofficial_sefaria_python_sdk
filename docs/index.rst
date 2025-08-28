Unofficial Sefaria Python SDK
===============================

A comprehensive, modernized Python SDK for interacting with the Sefaria API, featuring robust client architecture, extensive examples, and full compatibility with current API endpoints.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api_reference
   examples
   changelog

Features
--------

* **Modern API Support**: Fully aligned with current Sefaria API (2024)
* **Robust Client Architecture**: Connection pooling, retry strategies, comprehensive error handling
* **Async Support**: High-performance async client for bulk operations
* **Data Export Tools**: Multiple format support (JSON, CSV, PDF)
* **Comprehensive Examples**: Working examples for all use cases

Installation
------------

.. code-block:: bash

   pip install unofficial-sefaria-sdk

Quick Start
-----------

.. code-block:: python

   from sefaria_sdk import SefariaClient

   # Initialize client
   client = SefariaClient()

   # Search for texts
   results = client.search("charity", limit=5)
   print(f"Found {results['hits']['total']} results")

   # Get text with specific version
   text = client.get_text("Genesis 1:1", lang="en")
   print(text['versions'][0]['text'])

   # Get related content
   related = client.get_related("Genesis 1:1")
   print(f"Found {len(related['links'])} related texts")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
