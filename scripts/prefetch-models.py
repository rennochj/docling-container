#!/usr/bin/env python3
"""Pre-fetch RapidOCR models during Docker build to avoid runtime downloads.

This script triggers the download of RapidOCR models by performing a minimal
PDF conversion. The models are cached in the container's filesystem and won't
need to be downloaded again at runtime.
"""

import sys
import tempfile
from pathlib import Path

# Create a minimal PDF for model download trigger
def create_minimal_pdf(pdf_path: Path) -> None:
    """Create a minimal valid PDF file."""
    # Minimal PDF content (valid but tiny)
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT
/F1 12 Tf
100 700 Td
(Test) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000214 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
307
%%EOF
"""
    pdf_path.write_bytes(pdf_content)


def prefetch_models():
    """Trigger RapidOCR model downloads by converting a minimal PDF."""
    print("=" * 60)
    print("Pre-fetching RapidOCR models...")
    print("=" * 60)

    try:
        # Import after message to show progress
        from docling.document_converter import DocumentConverter
        from docling.datamodel.base_models import InputFormat

        # Create temporary directory and minimal PDF
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            pdf_path = tmpdir_path / "test.pdf"
            output_path = tmpdir_path / "output"
            output_path.mkdir()

            print(f"Creating minimal test PDF: {pdf_path}")
            create_minimal_pdf(pdf_path)

            print("Initializing document converter...")
            print("(This will download RapidOCR models - may take a few minutes)")

            # Initialize converter with PDF support (triggers model downloads)
            converter = DocumentConverter()

            print("Converting test PDF to trigger model downloads...")
            # Convert the minimal PDF (this triggers all model downloads)
            result = converter.convert(pdf_path)

            print("\n" + "=" * 60)
            print("✓ Model pre-fetch completed successfully!")
            print("=" * 60)
            print("\nModels cached in container. Future conversions will be faster.")

    except Exception as e:
        print(f"\n✗ Error during model pre-fetch: {e}", file=sys.stderr)
        print("\nNote: Models will be downloaded on first use instead.", file=sys.stderr)
        # Don't fail the build - models can still be downloaded at runtime
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(prefetch_models())
