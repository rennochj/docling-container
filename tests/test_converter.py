"""Tests for the document converter module."""

import pytest
from pathlib import Path
from docling_container.converter import DocumentConverter, EXTENSION_TO_FORMAT
from docling.datamodel.base_models import InputFormat


class TestDocumentConverter:
    """Test cases for DocumentConverter class."""

    def test_init(self):
        """Test converter initialization."""
        converter = DocumentConverter(
            output_format="markdown",
            preserve_structure=True
        )
        assert converter.output_format == "markdown"
        assert converter.preserve_structure is True

    def test_detect_format_pdf(self):
        """Test format detection for PDF files."""
        converter = DocumentConverter()
        test_path = Path("/test/document.pdf")
        detected_format = converter._detect_format(test_path)
        assert detected_format == InputFormat.PDF

    def test_detect_format_docx(self):
        """Test format detection for DOCX files."""
        converter = DocumentConverter()
        test_path = Path("/test/document.docx")
        detected_format = converter._detect_format(test_path)
        assert detected_format == InputFormat.DOCX

    def test_detect_format_image(self):
        """Test format detection for image files."""
        converter = DocumentConverter()
        for ext in ['.png', '.jpg', '.jpeg', '.tiff']:
            test_path = Path(f"/test/image{ext}")
            detected_format = converter._detect_format(test_path)
            assert detected_format == InputFormat.IMAGE

    def test_detect_format_unsupported(self):
        """Test format detection for unsupported files."""
        converter = DocumentConverter()
        test_path = Path("/test/document.xyz")
        detected_format = converter._detect_format(test_path)
        assert detected_format is None

    def test_get_output_extension_markdown(self):
        """Test output extension for markdown format."""
        converter = DocumentConverter(output_format="markdown")
        assert converter._get_output_extension() == ".md"

    def test_get_output_extension_html(self):
        """Test output extension for HTML format."""
        converter = DocumentConverter(output_format="html")
        assert converter._get_output_extension() == ".html"

    def test_get_output_extension_json(self):
        """Test output extension for JSON format."""
        converter = DocumentConverter(output_format="json")
        assert converter._get_output_extension() == ".json"

    def test_get_output_extension_text(self):
        """Test output extension for text format."""
        converter = DocumentConverter(output_format="text")
        assert converter._get_output_extension() == ".txt"

    def test_get_supported_formats(self):
        """Test retrieving supported formats."""
        converter = DocumentConverter()
        formats = converter.get_supported_formats()

        assert 'input' in formats
        assert 'output' in formats
        assert isinstance(formats['input'], list)
        assert isinstance(formats['output'], list)

        # Check some expected formats
        assert 'markdown' in formats['output']
        assert 'html' in formats['output']
        assert 'json' in formats['output']

    def test_extension_to_format_mapping(self):
        """Test that all expected extensions are mapped."""
        expected_extensions = [
            '.pdf', '.docx', '.pptx', '.html', '.htm',
            '.md', '.asciidoc', '.adoc', '.png', '.jpg',
            '.jpeg', '.tiff', '.bmp', '.webp'
        ]

        for ext in expected_extensions:
            assert ext in EXTENSION_TO_FORMAT, f"Missing mapping for {ext}"
