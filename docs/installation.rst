Installation
============

Requirements
------------

* Python 3.8 or higher
* requests >= 2.31.0
* urllib3 >= 1.26.0

Install from Source
-------------------

.. code-block:: bash

   git clone https://github.com/yourusername/unofficial_sefaria_python_sdk.git
   cd unofficial_sefaria_python_sdk
   pip install -e .

Install Dependencies
--------------------

For basic usage:

.. code-block:: bash

   pip install -r requirements.txt

For development (includes testing tools):

.. code-block:: bash

   pip install -r requirements.txt
   pip install pytest pytest-asyncio black flake8 isort mypy

For examples (includes additional dependencies):

.. code-block:: bash

   pip install flask pandas fpdf rich aiohttp

Verification
------------

To verify your installation:

.. code-block:: python

   from sefaria_sdk import SefariaClient
   
   client = SefariaClient()
   result = client.get_text("Genesis 1:1")
   print("Installation successful!")
   print(f"Retrieved: {result['ref']}")
