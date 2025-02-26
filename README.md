# Unofficial Sefaria Python SDK

A comprehensive Python SDK for accessing Jewish texts through the Sefaria API. This SDK provides easy-to-use interfaces for retrieving texts, translations, and metadata from Sefaria's extensive collection of Jewish texts.

## Features

- **Text Retrieval**: Get Hebrew and English texts with version control
- **Calendar Integration**: Access Jewish calendar data and weekly Torah portions
- **Search Capabilities**: Search across Sefaria's text collection
- **Metadata Access**: Get information about texts, versions, and languages
- **Async Support**: Efficient batch processing of multiple texts
- **Error Handling**: Robust error handling and response validation
- **Type Hints**: Full Python type hints for better IDE support

## Installation

```bash
pip install sefaria-sdk
```

Or install from source:
```bash
git clone https://github.com/rbrtjns90/unofficial_sefaria_python_sdk.git
cd unofficial_sefaria_python_sdk
pip install -e .
```

## Quick Start

```python
from sefaria_sdk import SefariaClient, TextProcessor

# Initialize client
client = SefariaClient()

# Get text in default version (Hebrew)
response = client.get_text("Genesis 1:1")
print(response['text'])

# Get English translation
english = client.get_text("Genesis 1:1", version="The Holy Scriptures: A New Translation (JPS 1917)")
print(english['text'])

# Use text processing utilities
hebrew = response['he']
english = english['text']

# Format Hebrew text with proper RTL
formatted_hebrew = TextProcessor.format_hebrew(hebrew)

# Get parallel texts
verse_pairs = TextProcessor.get_parallel_texts(hebrew, english)
for he, en in verse_pairs:
    print(f"{he} | {en}")
```

## Example Applications

The SDK comes with several example applications demonstrating real-world usage:

1. **Basic Usage** (`examples/01_basic_usage/`)
   - Text retrieval in different languages and versions
   - Response handling and error management

2. **Web Application** (`examples/02_web_app/`)
   - Flask app displaying weekly Torah portions
   - Parallel Hebrew/English text display
   - Responsive design with RTL support

3. **Research Tools** (`examples/03_research/`)
   - Text analysis utilities
   - Word frequency analysis
   - Cross-reference exploration

4. **Command Line Interface** (`examples/04_cli/`)
   - Quick text access from terminal
   - Search functionality
   - Calendar information

5. **Async Implementation** (`examples/05_async/`)
   - Asynchronous text fetching
   - Batch processing capabilities

6. **Data Export** (`examples/06_data_export/`)
   - Export texts to various formats
   - PDF and structured data generation

See the [examples directory](examples/) for detailed documentation and usage instructions.

## API Documentation

### Main Client Methods

- `get_text(ref, version=None)`: Get text for a specific reference
- `get_calendar_items(timezone="UTC")`: Get Jewish calendar information
- `search_text(query)`: Search across Sefaria texts
- `get_index(title)`: Get metadata about a text
- `get_text_versions(title)`: Get available versions of a text

### Response Types

All responses are Python dictionaries containing:
- `text`: The requested text content
- `he`: Hebrew text when available
- `versions`: Available text versions
- `refs`: Text references
- `type`: Content type identifier

## Text Processing Utilities

The SDK includes powerful text processing utilities through the `TextProcessor` class:

### Verse Extraction
```python
verses = TextProcessor.extract_verses(response)
```
- Extracts individual verses from API responses
- Handles various response formats
- Removes empty verses and normalizes whitespace

### Hebrew Text Formatting
```python
formatted = TextProcessor.format_hebrew(hebrew_text)
```
- Adds proper RTL markers
- Handles nikud (vowel points) correctly
- Ensures consistent text display

### Parallel Text Alignment
```python
pairs = TextProcessor.get_parallel_texts(hebrew, english)
```
- Aligns Hebrew and English texts verse by verse
- Handles mismatched verse counts
- Returns paired verses for parallel display

### Text Cleaning
```python
clean = TextProcessor.clean_text(text)
```
- Normalizes whitespace and punctuation
- Removes extra spaces
- Ensures consistent text formatting

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Sefaria](https://www.sefaria.org) for providing the API and text content
- The Jewish community for preserving these texts
- All contributors to this project

## Support

For support, please:
1. Check the [examples](examples/) directory
2. Read the [documentation](docs/)
3. Open an issue for bugs or feature requests

## Disclaimer

This is an unofficial SDK and is not affiliated with or endorsed by Sefaria.
