# Sefaria SDK Examples

This directory contains example applications demonstrating various use cases of the Sefaria Python SDK.

## Examples Overview

### 1. Basic Usage (`01_basic_usage/`)
- `text_retrieval.py`: Demonstrates basic text retrieval and API response handling
- Shows how to get texts in different languages and versions

### 2. Web Application (`02_web_app/`)
- `flask_torah_app.py`: A Flask web app that displays the weekly Torah portion
- Features:
  - Automatically fetches current parsha from Sefaria calendar
  - Shows parallel Hebrew and English text (using JPS 1917 translation)
  - Displays parsha description in both languages
  - Responsive layout with proper Hebrew text alignment
- To run:
  ```bash
  python3 flask_torah_app.py
  ```
  Then visit http://localhost:5000 in your browser

### 3. Research Tools (`03_research/`)
- `text_analysis.py`: Tools for analyzing Jewish texts
- Includes word frequency analysis and cross-reference exploration

### 4. Command Line Interface (`04_cli/`)
- `sefaria_cli.py`: Command-line tool for quick text access
- Supports search, calendar items, and text retrieval

### 5. Async Text Fetching (`05_async/`)
- `async_text_fetcher.py`: Demonstrates asynchronous text retrieval
- Useful for batch processing or fetching multiple texts efficiently

### 6. Data Export (`06_data_export/`)
- `text_exporter.py`: Tools for exporting texts to various formats
- Supports PDF and structured data exports

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

## Notes

- All examples include error handling and logging
- The web app and CLI tools are designed for interactive use
- Research tools focus on programmatic analysis
- Async examples show performance optimization techniques
- Export tools demonstrate data transformation capabilities

## Contributing

Feel free to add your own examples! Please follow these guidelines:
1. Create a new directory for your example category
2. Include a README.md explaining your example
3. Add any required dependencies to requirements.txt
4. Follow the existing code style and documentation patterns
