"""
Example of exporting Sefaria texts to various formats.
"""

from sefaria_sdk import SefariaClient
import csv
import json
from fpdf import FPDF
from typing import List, Dict
import pandas as pd


class TextExporter:
    def __init__(self):
        self.client = SefariaClient()

    def _extract_text(self, response: Dict, language: str) -> List[str]:
        """Extract text from API response based on language."""
        if "versions" in response and response["versions"]:
            for version in response["versions"]:
                if version.get("language") == language and "text" in version:
                    text = version["text"]
                    if isinstance(text, list):
                        return text
                    else:
                        return [text]
        return []

    def to_json(self, text_ref: str, output_path: str):
        """Export text to JSON format."""
        # Get text in both languages
        hebrew_response = self.client.get_text(text_ref, lang="he")
        english_response = self.client.get_text(text_ref, lang="en")

        # Extract text content
        hebrew_text = self._extract_text(hebrew_response, "he")
        english_text = self._extract_text(english_response, "en")

        # Combine data
        data = {
            "reference": text_ref,
            "hebrew": hebrew_text,
            "english": english_text,
            "metadata": {
                "heTitle": hebrew_response.get("heTitle"),
                "title": english_response.get("title"),
                "categories": english_response.get("categories", []),
            },
        }

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def to_csv(self, text_ref: str, output_path: str):
        """Export text to CSV format."""
        # Get text in both languages
        hebrew_response = self.client.get_text(text_ref, lang="he")
        english_response = self.client.get_text(text_ref, lang="en")

        # Extract text content
        hebrew_text = self._extract_text(hebrew_response, "he")
        english_text = self._extract_text(english_response, "en")

        # Prepare data
        rows = []
        max_verses = max(len(hebrew_text), len(english_text))

        for i in range(max_verses):
            rows.append(
                {
                    "Verse": i + 1,
                    "Hebrew": hebrew_text[i] if i < len(hebrew_text) else "",
                    "English": english_text[i] if i < len(english_text) else "",
                }
            )

        # Write to CSV
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

    def to_pdf(self, text_ref: str, output_path: str):
        """Export text to PDF format (English only due to Hebrew encoding limitations)."""
        # Get text in both languages
        hebrew_response = self.client.get_text(text_ref, lang="he")
        english_response = self.client.get_text(text_ref, lang="en")

        # Extract text content
        hebrew_text = self._extract_text(hebrew_response, "he")
        english_text = self._extract_text(english_response, "en")

        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, text_ref, ln=True, align="C")
        pdf.ln(10)

        # Add note about Hebrew text
        pdf.set_font("Arial", "I", 10)
        pdf.cell(
            0, 10, "Note: Hebrew text excluded due to PDF encoding limitations", ln=True
        )
        pdf.ln(5)

        # Add texts (English only)
        pdf.set_font("Arial", size=12)
        max_verses = max(len(hebrew_text), len(english_text))

        for i in range(max_verses):
            pdf.cell(0, 10, f"Verse {i + 1}:", ln=True)

            # Add English text if available
            if i < len(english_text):
                # Clean HTML tags from English text
                import re

                clean_english = re.sub(r"<[^>]+>", "", english_text[i])
                # Encode to latin-1 compatible characters only
                try:
                    clean_english.encode("latin-1")
                    pdf.cell(0, 10, clean_english, ln=True)
                except UnicodeEncodeError:
                    # Replace non-latin characters with transliterations
                    safe_text = clean_english.encode("ascii", "ignore").decode("ascii")
                    pdf.cell(0, 10, safe_text + " (some characters removed)", ln=True)
            else:
                pdf.cell(0, 10, "(No English text available)", ln=True)

            # Note about Hebrew text
            if i < len(hebrew_text):
                pdf.cell(0, 10, "(Hebrew text available in JSON/CSV exports)", ln=True)

            pdf.ln(5)

        # Save PDF
        pdf.output(output_path)


def main():
    exporter = TextExporter()
    text_ref = "Psalms 23"

    # Export to different formats
    print(f"Exporting {text_ref} to different formats...")

    exporter.to_json(text_ref, "psalm23.json")
    print("Exported to JSON")

    exporter.to_csv(text_ref, "psalm23.csv")
    print("Exported to CSV")

    exporter.to_pdf(text_ref, "psalm23.pdf")
    print("Exported to PDF")


if __name__ == "__main__":
    main()
