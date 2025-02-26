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
    
    def to_json(self, text_ref: str, output_path: str):
        """Export text to JSON format."""
        # Get text in both languages
        hebrew = self.client.get_text(text_ref, version="he")
        english = self.client.get_text(text_ref)
        
        # Combine data
        data = {
            'reference': text_ref,
            'hebrew': hebrew['text'],
            'english': english['text'],
            'metadata': {
                'heTitle': hebrew.get('heTitle'),
                'title': english.get('title'),
                'categories': english.get('categories', [])
            }
        }
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def to_csv(self, text_ref: str, output_path: str):
        """Export text to CSV format."""
        # Get text in both languages
        hebrew = self.client.get_text(text_ref, version="he")
        english = self.client.get_text(text_ref)
        
        # Prepare data
        rows = []
        if isinstance(hebrew['text'], list):
            for i, (he, en) in enumerate(zip(hebrew['text'], english['text']), 1):
                rows.append({
                    'Verse': i,
                    'Hebrew': he,
                    'English': en
                })
        else:
            rows.append({
                'Verse': 1,
                'Hebrew': hebrew['text'],
                'English': english['text']
            })
            
        # Write to CSV
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    def to_pdf(self, text_ref: str, output_path: str):
        """Export text to PDF format."""
        # Get text in both languages
        hebrew = self.client.get_text(text_ref, version="he")
        english = self.client.get_text(text_ref)
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Add title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, text_ref, ln=True, align='C')
        
        # Add texts
        pdf.set_font("Arial", size=12)
        if isinstance(hebrew['text'], list):
            for i, (he, en) in enumerate(zip(hebrew['text'], english['text']), 1):
                pdf.cell(0, 10, f"Verse {i}:", ln=True)
                pdf.cell(0, 10, en, ln=True)  # English
                pdf.cell(0, 10, he, ln=True)  # Hebrew
                pdf.ln(5)
        else:
            pdf.cell(0, 10, english['text'], ln=True)  # English
            pdf.cell(0, 10, hebrew['text'], ln=True)   # Hebrew
        
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
