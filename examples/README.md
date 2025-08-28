# Sefaria SDK Examples

This directory contains example applications demonstrating various use cases of the Sefaria Python SDK. All examples have been updated to work with the modernized SDK and current Sefaria API.

## Examples Overview

### 1. Basic Usage (`01_basic_usage/`)
- `text_retrieval.py`: Demonstrates basic text retrieval and API response handling
- `text_ret_lang.py`: Shows language-specific text retrieval
- `text_processing_demo.py`: Text processing and formatting examples
- **Status**: ✅ Working with current API

### 2. Web Application (`02_web_app/`)
- `flask_torah_app.py`: A Flask web app that displays the weekly Torah portion
- Features:
  - Automatically fetches current parsha from Sefaria calendar
  - Shows parallel Hebrew and English text
  - Displays parsha description in both languages
  - Responsive layout with proper Hebrew text alignment
- To run:
  ```bash
  python3 flask_torah_app.py
  ```
  Then visit http://localhost:5000 in your browser
- **Status**: ✅ Working with current API

### 3. Research Tools (`03_research/`)
- `text_analysis.py`: Tools for analyzing Jewish texts
- Includes word frequency analysis and cross-reference exploration
- **Status**: ✅ Working with current API

### 4. Command Line Interface (`04_cli/`)
- `sefaria_cli.py`: Command-line tool for quick text access
- **Fixed Features**:
  - ✅ Search functionality now working with proper result display
  - ✅ Text retrieval with clean reference formatting
  - ✅ Calendar items display
- Usage examples:
  ```bash
  python3 sefaria_cli.py search -n 5 "charity"
  python3 sefaria_cli.py get-text "Genesis 1:1"
  python3 sefaria_cli.py today
  ```
- **Status**: ✅ Fixed and working

### 5. Async Text Fetching (`05_async/`)
- `async_text_fetcher_fixed.py`: Demonstrates asynchronous text retrieval
- **Fixed Features**:
  - ✅ Now retrieves actual English text content (not just availability)
  - ✅ Proper Hebrew text display with formatting
  - ✅ Concurrent fetching for multiple texts
  - ✅ Uses correct API endpoints for English versions
- **Status**: ✅ Fixed and working

### 6. Data Export (`06_data_export/`)
- `text_exporter.py`: Tools for exporting texts to various formats
- **Fixed Features**:
  - ✅ JSON export with both Hebrew and English text
  - ✅ CSV export with verse-by-verse structure
  - ✅ PDF export (English only due to encoding limitations)
  - ✅ Proper API response structure handling
- **Status**: ✅ Fixed and working

### 7. Modern API Features (`06_improved_api/`)
- `modern_client_demo.py`: Showcases the modernized SDK features
- **Features**:
  - ✅ Fixed search functionality using search-wrapper endpoint
  - ✅ Modern get_related() method for related content
  - ✅ Enhanced text retrieval with v3 API parameters
  - ✅ Robust client with retries and proper error handling
- **Status**: ✅ Working with all modern features

## Running the Examples

1. Make sure you have the SDK installed:
   ```bash
   pip install -e ..
   ```

2. Install example-specific dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run any example script directly:
   ```bash
   python3 example_directory/script_name.py
   ```

## Recent Fixes and Updates

All examples have been updated to work with the modernized Sefaria SDK:

### API Compatibility Fixes
- **Search functionality**: Updated to use POST /search-wrapper endpoint with proper response parsing
- **Text retrieval**: Fixed to handle current API response structure with `versions` array
- **Language parameters**: Corrected parameter names and endpoint usage for multilingual content
- **Error handling**: Enhanced robustness with proper exception handling and fallbacks

### Key Improvements
- **CLI Search**: Now displays actual search results instead of "N/A" values
- **Async Fetcher**: Retrieves real English text content, not just availability status
- **Text Exporter**: Properly extracts text from API responses for all export formats
- **Modern Demo**: Showcases all new SDK features with working search and related content

### Dependencies
The examples now require:
- `aiohttp` for async functionality
- `pandas` for CSV export
- `fpdf` for PDF generation
- `flask` for web applications
- `rich` for CLI formatting

## Notes

- All examples are compatible with the current Sefaria API (as of August 2024)
- Examples include comprehensive error handling and user feedback
- The web app and CLI tools provide interactive interfaces
- Research tools focus on programmatic text analysis
- Async examples demonstrate performance optimization for bulk operations
- Export tools support multiple output formats with proper encoding

## Contributing

Feel free to add your own examples! Please follow these guidelines:
1. Create a new directory for your example category
2. Include a README.md explaining your example
3. Add any required dependencies to requirements.txt
4. Follow the existing code style and documentation patterns
5. Ensure compatibility with the current SDK API structure
