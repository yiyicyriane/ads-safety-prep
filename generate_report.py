import markdown
from weasyprint import HTML
import os

DOCS = [
    ("System Overview", "README.md"),
    ("Design Document", "design_doc.md"),
    ("Evaluation Report", "evaluation.md"),
]
OUTPUT_PATH = "output/report.pdf"
CSS = """
<style>
    body {
        font-family: Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        margin: 40px;
        color: #222;
    }
    h1 { font-size: 24px; border-bottom: 2px solid #333; padding-bottom: 6px; }
    h2 { font-size: 20px; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
    h3 { font-size: 16px; }
    code {
        background: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 13px;
    }
    pre {
        background: #f4f4f4;
        padding: 12px;
        border-radius: 4px;
        overflow-x: auto;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 16px 0;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px 12px;
        text-align: left;
    }
    th { background: #f0f0f0; }
    .section-divider {
        page-break-before: always;
        border-top: 3px solid #333;
        margin-top: 40px;
        padding-top: 20px;
    }
</style>
"""


def read_markdown(file_path: str) -> str:
    """
    Read a markdown file and return the content.
    Args:
        file_path: path to the markdown file
    Returns:
        The content of the markdown file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def convert_to_html(title: str, md_content: str, first: bool) -> str:
    """
    Convert a markdown section to HTML.
    Args:
        title: the title of the section
        md_content: the markdown content of the section
        first: whether this is the first section
    Returns:
        The HTML content of the section
    """
    body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code"]
    )
    divider_class = "" if first else "section-divider"
    return f"""
    <div class="{divider_class}">
        <h1>{title}</h1>
        {body}
    </div>
    """

def generate_report(docs: list, output_path: str) -> None:
    """
    Generate a PDF report from a list of markdown files.
    Args:
        docs: list of tuples (title, markdown_file)
        output_path: path to save the report
    """
    print("Generating report...")

    sections = []
    for i, (title, file_path) in enumerate(docs):
        print(f" Reading {file_path}...")
        try:
            md_content = read_markdown(file_path)
        except FileNotFoundError as e:
            print(f" [WARNING] Skipping {file_path} - file not found")
            continue
        html_section = convert_to_html(title, md_content, first=(i==0))
        sections.append(html_section)
    
    if not sections:
        print(" [ERROR] No valid sections found. Exiting...")
        return
    
    full_html = f"<html><head>{CSS}</head><body>{''.join(sections)}</body></html>"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    HTML(string=full_html).write_pdf(output_path)
    print(f"Report generated successfully and saved to {output_path}")


if __name__ == "__main__":
    generate_report(DOCS, OUTPUT_PATH)

