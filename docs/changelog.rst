Changelog
=========

Version 0.1.0 (2024-08-28)
---------------------------

Initial release of the modernized Sefaria Python SDK.

**New Features**

* Modern API support with full compatibility for current Sefaria endpoints
* Robust client architecture with connection pooling and retry strategies
* Comprehensive async support for bulk operations
* Text processing utilities for Hebrew and English content
* Multi-format data export capabilities (JSON, CSV, PDF)
* Command line interface for quick text access
* Flask web application example
* Complete test suite with 59+ passing tests

**API Improvements**

* Updated search functionality using POST /search-wrapper endpoint
* Enhanced text retrieval with v3 Texts API support
* Added get_related() method for modern content relationships
* Fixed get_languages() method to use correct /texts/translations endpoint
* Improved error handling with exponential backoff retry logic

**Examples and Documentation**

* 7 comprehensive example categories with working code
* CLI tool with search, text retrieval, and calendar features
* Async text fetcher for concurrent operations
* Data export tools supporting multiple formats
* Research and analysis utilities
* Complete Sphinx documentation
* GitHub Actions CI/CD workflows

**Technical Enhancements**

* Session-based HTTP client with connection pooling
* Configurable timeouts and headers
* Comprehensive error handling and logging
* Type hints throughout the codebase
* Full test coverage with pytest
* Code quality tools (Black, flake8, isort, mypy)
* Security scanning with Bandit and Safety

**Breaking Changes**

* Modernized API endpoints may not be compatible with older Sefaria API versions
* Search method now uses different parameter structure
* Text response structure updated to match current API format

**Dependencies**

* Python 3.8+ required
* requests >= 2.31.0
* urllib3 >= 1.26.0
* Optional: aiohttp for async functionality
* Optional: pandas, fpdf, flask, rich for examples
