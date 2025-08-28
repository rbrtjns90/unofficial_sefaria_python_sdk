"""
Command-line interface for accessing Sefaria texts.
"""
import click
from sefaria_sdk import SefariaClient
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

console = Console()
client = SefariaClient()

@click.group()
def cli():
    """Command line interface for Sefaria texts."""
    pass

@cli.command()
@click.argument('reference')
@click.option('--language', '-l', default='en', help='Language (en/he)')
def get_text(reference, language):
    """Get text for a specific reference."""
    try:
        response = client.get_text(reference, version=language)
        
        # Create a panel for the text
        title = f"[bold blue]{response.get('ref', reference)}"
        if 'heRef' in response:
            title += f" / {response['heRef']}"
            
        content = []
        if 'available_versions' in response:
            for version in response['available_versions']:
                if version['language'] == language:
                    text = version.get('text', 'No text available')
                    if isinstance(text, list):
                        for i, verse in enumerate(text, 1):
                            content.append(f"[bold cyan]{i}[/bold cyan]: {verse}")
                    else:
                        content.append(text)
                    break
        
        panel = Panel(
            "\n".join(content) if content else "No text available",
            title=title,
            border_style="blue"
        )
        console.print(panel)
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
@click.argument('query')
@click.option('--limit', '-n', default=5, help='Number of results')
def search(query, limit):
    """Search for texts containing a query."""
    try:
        results = client.search(query, limit=limit)
        
        table = Table(title=f"Search Results for '{query}'",
                     box=box.ROUNDED)
        table.add_column("Reference", style="cyan")
        table.add_column("Text", style="white")
        
        if 'hits' in results and 'hits' in results['hits']:
            for hit in results['hits']['hits']:
                # Extract reference from _id field
                ref = hit.get('_id', 'N/A')
                # Clean up the reference by removing version info in parentheses
                if '(' in ref:
                    ref = ref.split('(')[0].strip()
                
                # Extract highlighted text from highlight.exact field
                highlight_text = 'N/A'
                if 'highlight' in hit and 'exact' in hit['highlight']:
                    highlight_snippets = hit['highlight']['exact']
                    if highlight_snippets:
                        # Take first snippet and clean up HTML tags
                        highlight_text = highlight_snippets[0].replace('<b>', '').replace('</b>', '')
                        # Truncate if too long
                        if len(highlight_text) > 100:
                            highlight_text = highlight_text[:97] + '...'
                
                table.add_row(ref, highlight_text)
        else:
            table.add_row("No results found", "")
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
def today():
    """Get today's calendar items."""
    try:
        calendar = client.get_calendar_items()
        
        table = Table(title="Today's Calendar Items",
                     box=box.ROUNDED)
        table.add_column("Title", style="cyan")
        table.add_column("Description", style="white")
        
        if 'calendar_items' in calendar:
            for item in calendar['calendar_items']:
                table.add_row(
                    item.get('title', {}).get('en', 'N/A'),
                    item.get('description', {}).get('en', 'N/A')
                )
        else:
            table.add_row("No calendar items found", "")
            
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    cli()
