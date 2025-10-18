# Example Documents

This directory contains sample documents for testing the docling-container conversion functionality.

## Available Examples

### 1. sample.md
A sample Markdown document demonstrating:
- Headings and formatting
- Code blocks
- Tables
- Lists

### 2. sample.html
A sample HTML document demonstrating:
- Basic HTML structure
- Tables
- Lists
- Semantic markup

## Testing Conversions

### Convert Markdown to HTML

```bash
uv run python -m docling_container.main convert examples/sample.md output/ -f html
```

### Convert HTML to Markdown

```bash
uv run python -m docling_container.main convert examples/sample.html output/ -f markdown
```

### Batch Convert All Examples

```bash
uv run python -m docling_container.main convert examples/ output/ --batch
```

## Adding Your Own Examples

To test with your own documents:

1. Add your files to this directory
2. Supported formats: PDF, DOCX, PPTX, XLSX, HTML, Markdown, images, etc.
3. Run the conversion commands above

## Output

Converted files will be saved to the `output/` directory with the appropriate extension based on the target format.
