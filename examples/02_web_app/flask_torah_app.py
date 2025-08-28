"""
Example Flask web application that serves weekly Torah portions.
"""

from flask import Flask, render_template_string
from datetime import datetime
import logging
from sefaria_sdk import SefariaClient

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = SefariaClient()

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weekly Torah Portion</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .hebrew { font-size: 1.2em; direction: rtl; text-align: right; }
        .english { margin-top: 10px; }
        .verse { margin: 20px 0; padding: 10px; border-bottom: 1px solid #eee; }
        h1 { text-align: center; color: #2d4150; }
        .error { color: red; text-align: center; }
        .description { 
            margin: 20px 0; 
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
        }
        .description-hebrew { 
            direction: rtl; 
            text-align: right;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    {% if description %}
    <div class="description">
        <div>{{ description.en }}</div>
        <div class="description-hebrew">{{ description.he }}</div>
    </div>
    {% endif %}
    {% if error %}
    <div class="error">{{ error }}</div>
    {% else %}
    {% for verse in verses %}
    <div class="verse">
        <div class="hebrew">{{ verse.hebrew }}</div>
        <div class="english">{{ verse.english }}</div>
    </div>
    {% endfor %}
    {% endif %}
</body>
</html>
"""


def get_text_content(response, language):
    """Extract text content from API response."""
    logger.debug(f"Response for {language}: {response}")

    # Check if response has direct text content
    if "text" in response:
        return response["text"]

    # Check in he/text or en/text
    if language in response and "text" in response[language]:
        return response[language]["text"]

    # Check in versions
    if "versions" in response and len(response["versions"]) > 0:
        return response["versions"][0].get("text", [])

    logger.debug(f"No text found for {language}")
    return []


@app.route("/")
def weekly_portion():
    try:
        # Get current Torah portion from calendar
        calendar = client.get_calendar_items(timezone="UTC")
        logger.debug(f"Calendar response: {calendar}")

        parsha = next(
            (
                item
                for item in calendar.get("calendar_items", [])
                if item.get("title", {}).get("en", "").startswith("Parashat")
            ),
            None,
        )

        if not parsha:
            return render_template_string(
                HTML_TEMPLATE,
                title="Weekly Torah Portion",
                error="No Torah portion found for this week",
                description=None,
                verses=[],
            )

        logger.debug(f"Found parsha: {parsha}")

        # Get the text in both Hebrew and English
        ref = parsha["ref"]
        hebrew_response = client.get_text(ref)  # Default is Hebrew
        english_response = client.get_text(
            ref, version="The Holy Scriptures: A New Translation (JPS 1917)"
        )

        # Extract text content
        hebrew_text = get_text_content(hebrew_response, "he")
        english_text = get_text_content(english_response, "english")

        logger.debug(f"Hebrew text length: {len(hebrew_text)}")
        logger.debug(f"English text length: {len(english_text)}")

        # Combine Hebrew and English verses
        verses = (
            [{"hebrew": h, "english": e} for h, e in zip(hebrew_text, english_text)]
            if hebrew_text and english_text
            else []
        )

        return render_template_string(
            HTML_TEMPLATE,
            title=f"{parsha['displayValue']['en']} - {parsha['displayValue']['he']}",
            description=parsha.get("description", {}),
            error="" if verses else "No text available for this portion",
            verses=verses,
        )

    except Exception as e:
        logger.exception("Error in weekly_portion:")
        return render_template_string(
            HTML_TEMPLATE,
            title="Weekly Torah Portion",
            description=None,
            error=f"Error: {str(e)}",
            verses=[],
        )


if __name__ == "__main__":
    app.run(debug=True)
