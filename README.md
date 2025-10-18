# Docling Container

[![GitHub release](https://img.shields.io/github/v/release/rennochj/docling-container)](https://github.com/rennochj/docling-container/releases)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/rennochj/docling-container/pkgs/container/docling-container)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Docker container for [Docling](https://docling-project.github.io/docling/), a powerful document conversion tool that converts various document formats to markdown, HTML, JSON, text, and more.

## Features

- **Multiple Input Formats**: PDF, DOCX, PPTX, HTML, Markdown, ASCIIDOC, and images (PNG, JPEG, TIFF, BMP, WEBP)
- **Multiple Output Formats**: Markdown, HTML, JSON, Text, Doctags
- **URL Support**: Convert documents directly from URLs (e.g., arxiv.org papers, online PDFs)
- **Image Extraction**: Extract and save images (figures, tables) from documents with configurable resolution
- **OCR Support**: Built-in OCR for extracting text from images and scanned PDFs
- **Table Detection**: Advanced table structure recognition and extraction
- **Batch Processing**: Convert entire directories of documents
- **Pattern Filtering**: Use glob patterns to selectively process files (e.g., only PDFs)
- **Recursive Processing**: Process nested directory structures
- **Comprehensive Logging**: Detailed logs with conversion statistics
- **Performance Optimized**: Multi-stage Docker build for minimal image size
- **Error Handling**: Graceful error handling with meaningful messages
- **Flexible Configuration**: YAML config file support for default settings

## Supported Formats

### Input Formats
- **Documents**: PDF, DOCX, PPTX, HTML, Markdown, ASCIIDOC
- **Images**: PNG, JPEG, TIFF, BMP, WEBP
- **URLs**: Any publicly accessible document URL (HTTP/HTTPS)

### Output Formats
- Markdown (`.md`)
- HTML (`.html`)
- JSON (`.json`)
- Plain Text (`.txt`)
- Doctags (`.doctags`)

## Technical Details

- **Base Image**: Python 3.13 (slim)
- **Multi-stage Build**: Optimized for minimal image size
- **Package Manager**: UV (fast Python package installer)
- **Docling Version**: 2.0.0+
- **Architecture**: Supports amd64 and arm64

## Installation

### Prerequisites
- Docker installed on your system
- Input documents to convert

### Using Pre-built Image (Recommended)

Pull the latest image from GitHub Container Registry:

```bash
# Pull latest version
docker pull ghcr.io/rennochj/docling-container:latest

# Or pull a specific version
docker pull ghcr.io/rennochj/docling-container:0.3.1
```

### Building from Source

```bash
# Clone the repository
git clone https://github.com/rennochj/docling-container.git
cd docling-container

# Build the Docker image
docker build -t docling-container .

# Or build for multiple platforms
make build-multiplatform
```

## Quick Start

The fastest way to get started with the pre-built image:

```bash
# Pull the image
docker pull ghcr.io/rennochj/docling-container:latest

# Convert a PDF
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  ghcr.io/rennochj/docling-container:latest \
  convert document.pdf
```

### Shell Aliases (Recommended)

For easier usage, add an alias to your shell configuration:

**macOS / Linux (Bash/Zsh):**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias docling='docker run --rm -v $(pwd)/input:/input -v $(pwd)/output:/output ghcr.io/rennochj/docling-container:latest'

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# Add to your PowerShell profile (run: notepad $PROFILE)
function docling {
    docker run --rm -v ${PWD}/input:/input -v ${PWD}/output:/output ghcr.io/rennochj/docling-container:latest $args
}
```

**After setting up the alias, you can use it like this:**

```bash
# Convert a PDF
docling convert document.pdf

# Convert from URL
docling convert https://arxiv.org/pdf/2408.09869 /output

# Batch convert with image extraction
docling convert --batch --export-images

# Batch convert only PDFs
docling convert --batch --pattern "*.pdf"

# Batch convert multiple file types
docling convert --batch --pattern "*.pdf" --pattern "*.docx"

# See all options
docling convert --help
```

### Building from Source

Or if you're building from source, use Make targets:

```bash
# Build the image
make build

# Convert a PDF with image extraction
make run-pdf-images

# Convert a PowerPoint presentation
make run-pptx-images

# See all available commands
make help
```

## Usage

### Basic Usage

The application uses `/input` and `/output` as default directories, so you only need to specify filenames:

Convert a single file:

```bash
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-container convert document.pdf
```

### URL Conversion

Convert documents directly from URLs:

```bash
docker run -v /path/to/output:/output \
  docling-container convert https://arxiv.org/pdf/2408.09869 /output
```

```bash
# Convert any publicly accessible PDF
docker run -v $(pwd)/output:/output \
  docling-container convert https://example.com/document.pdf /output -f markdown
```

### Image Extraction

Extract images from documents while converting. By default, only figures and tables are extracted:

```bash
# Extract figures and tables (recommended)
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-container convert document.pdf /output --export-images
```

```bash
# Extract with high resolution (4x scale = 288 DPI)
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-container convert document.pdf /output --export-images --images-scale 4.0
```

```bash
# Extract ALL images including full page renders
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-container convert document.pdf /output --export-images --export-page-images
```

Images are saved to a subdirectory named `{document}_images/` and referenced in the output:
```markdown
![Image](document_images/figure_1.png)
```

### Batch Conversion

Convert all documents in the input directory:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert --batch
```

Or use an explicit directory:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert . --batch
```

Filter files using glob patterns:

```bash
# Convert only PDF files
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert --batch --pattern "*.pdf"

# Convert multiple file types
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert --batch --pattern "*.pdf" --pattern "*.docx"

# Pattern matching for specific filenames
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert --batch --pattern "report_*.pdf"
```

### Recursive Processing

Process directories recursively:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert -r --log-level INFO
```

Combine recursive mode with patterns:

```bash
# Convert all PDFs recursively
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert -r --pattern "*.pdf"

# Convert specific file types from all subdirectories
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert -r --pattern "*.pdf" --pattern "*.docx" --pattern "*.pptx"
```

### Output Format Selection

Convert to HTML instead of markdown:

```bash
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-container convert document.pdf -f html
```

### Advanced Options

Full example with all options:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-container convert \
    --output-format markdown \
    --batch \
    --recursive \
    --log-level DEBUG \
    --preserve-structure \
    --fail-fast \
    --export-images \
    --images-scale 2.0
```

### Custom Paths

You can still specify custom paths if needed:

```bash
docker run -v /path/to/data:/data \
  docling-container convert /data/document.pdf /data/output
```

## CLI Options

### Commands

- `convert` - Convert document(s) from input to output
- `formats` - List all supported input and output formats

### Convert Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--output-format` | `-f` | `markdown` | Output format (markdown, html, json, text, doctags) |
| `--batch` / `--no-batch` | `-b` | `True` | Enable/disable batch processing for directories |
| `--recursive` / `--no-recursive` | `-r` | `False` | Recursively process subdirectories |
| `--pattern` | | `None` | Glob pattern(s) to filter files (e.g., "*.pdf"). Can be specified multiple times |
| `--log-level` | | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `--log-file` | | `None` | Optional log file path |
| `--config` | | `None` | Path to configuration file |
| `--preserve-structure` | | `True` | Preserve original document structure |
| `--fail-fast` | | `False` | Stop processing on first error |
| `--export-images` | | `False` | Extract and save images from documents |
| `--images-scale` | | `2.0` | Resolution scale for images (1.0 = 72 DPI, 2.0 = 144 DPI) |
| `--export-page-images` | | `False` | Include full page images in extraction |

## Examples

### Example 1: Convert Single PDF to Markdown

```bash
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-container convert report.pdf
```

**Output**: `output/report.md`

### Example 2: Convert PDF from URL with Image Extraction

```bash
docker run -v $(pwd)/output:/output \
  docling-container convert https://arxiv.org/pdf/2408.09869 /output \
    -f markdown --export-images
```

**Output**:
- `output/2408.09869.md` - Converted markdown
- `output/2408.09869_images/` - Directory with extracted images

### Example 3: Batch Convert All Office Documents

```bash
docker run -v $(pwd)/documents:/input -v $(pwd)/converted:/output \
  docling-container convert -f html --batch
```

**Result**: All supported documents in `documents/` converted to HTML in `converted/`

### Example 4: Recursive Conversion with Logging

```bash
docker run -v $(pwd)/docs:/input -v $(pwd)/output:/output -v $(pwd)/logs:/logs \
  docling-container convert \
    -r \
    --log-level DEBUG \
    --log-file /logs/conversion.log
```

**Result**: Recursively processes all documents with debug logging saved to `logs/conversion.log`

### Example 5: Convert Images to Text with OCR

```bash
docker run -v $(pwd)/images:/input -v $(pwd)/text:/output \
  docling-container convert -f text --batch
```

**Result**: OCR extraction from images exported as text files

### Example 6: Convert PowerPoint with High-Resolution Images

```bash
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-container convert presentation.pptx /output \
    --export-images --images-scale 4.0
```

**Result**: Markdown with 288 DPI images extracted

### Example 7: Batch Convert with File Patterns

```bash
# Convert only PDF files
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-container convert --batch --pattern "*.pdf"

# Convert multiple specific file types
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-container convert --batch --pattern "*.pdf" --pattern "*.docx" --pattern "*.pptx"

# Pattern matching with recursive processing
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-container convert -r --pattern "report_*.pdf"
```

**Result**: Only files matching the specified pattern(s) are converted

### Example 8: List Supported Formats

```bash
docker run docling-container formats
```

## Using the Makefile

The project includes a comprehensive Makefile for common operations:

```bash
# Show all available commands
make help

# Setup directories
make setup

# Build the Docker image
make build

# Run examples
make run-pdf              # Convert PDF to markdown
make run-pptx             # Convert PowerPoint to markdown
make run-url              # Convert from URL
make run-pdf-images       # Convert PDF with image extraction
make run-images-hires     # Convert with high-resolution images

# Batch operations
make run-batch            # Convert all files to markdown
make run-batch-html       # Convert all files to HTML

# Utilities
make show-output          # List output directory contents
make shell                # Open shell in container
make clean                # Clean everything
make clean-output         # Clean output files only

# Quick start
make quick-start          # Setup + build + run batch
```

## Development

### Local Development Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the CLI locally
uv run python -m docling_container.main --help

# Run tests
uv run pytest
```

### Project Structure

```
docling-container/
├── docling_container/      # Main application package
│   ├── __init__.py
│   ├── main.py            # CLI interface
│   ├── converter.py       # Document conversion logic
│   ├── logger.py          # Logging configuration
│   └── config.py          # Configuration handling
├── tests/                 # Test suite
├── examples/              # Example documents
├── Dockerfile             # Multi-stage Docker build
├── Makefile               # Build and run automation
├── pyproject.toml         # Project dependencies
├── CLAUDE.md              # AI assistant instructions
└── README.md              # This file
```

## Troubleshooting

### Issue: Permission Denied

**Problem**: Cannot write to output directory

**Solution**: Ensure the output directory has proper write permissions:

```bash
chmod -R 777 /path/to/output
```

### Issue: Unsupported Format

**Problem**: "Unsupported file format" error

**Solution**: Check the list of supported formats:

```bash
docker run docling-container formats
```

### Issue: Out of Memory

**Problem**: Container runs out of memory with large PDFs

**Solution**: Increase Docker memory limit:

```bash
docker run --memory=4g -v /input:/input -v /output:/output \
  docling-container convert /input /output
```

### Issue: Conversion Fails Silently

**Problem**: Some files don't convert but no error is shown

**Solution**: Enable debug logging to see detailed error messages:

```bash
docker run -v /input:/input -v /output:/output \
  docling-container convert /input /output --log-level DEBUG
```

### Issue: URL Conversion Fails

**Problem**: Cannot convert document from URL

**Solution**:
1. Ensure the URL is publicly accessible
2. Check if the URL requires authentication
3. Verify the URL points directly to a document (not a landing page)

### Issue: Too Many Images Extracted

**Problem**: Extraction creates many page_*.png files

**Solution**: By default, only figures and tables are extracted. If you're seeing page images, remove the `--export-page-images` flag:

```bash
# Good - only figures and tables
docker run -v /input:/input -v /output:/output \
  docling-container convert doc.pdf /output --export-images

# Includes page renders (usually not needed)
docker run -v /input:/input -v /output:/output \
  docling-container convert doc.pdf /output --export-images --export-page-images
```

## Performance Tips

1. **Batch Processing**: Use batch mode for multiple files to reuse the model loading
2. **Memory Allocation**: Allocate sufficient memory for large documents (4GB+ recommended for PDFs with OCR)
3. **Fail-Fast Mode**: Use `--fail-fast` to stop on errors and save processing time
4. **Format Selection**: JSON output is typically faster than other formats
5. **Image Extraction**: Only use `--export-page-images` if you specifically need full page renders
6. **Image Resolution**: Use lower `--images-scale` values (e.g., 1.0 or 2.0) for faster processing
7. **OCR Processing**: OCR is automatically enabled for PDFs and images - this improves accuracy but increases processing time

## Configuration

You can create a configuration file to set default options:

```yaml
# config.yaml
output_format: markdown
preserve_structure: true
log_level: INFO
batch: true
recursive: false
export_images: true
images_scale: 2.0
export_page_images: false
```

Use with:

```bash
docker run -v $(pwd)/config.yaml:/config.yaml -v /input:/input -v /output:/output \
  docling-container convert /input /output --config /config.yaml
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure tests pass: `uv run pytest`
5. Use conventional commits (e.g., `feat:`, `fix:`, `docs:`)
6. Submit a pull request

### Release Process (Maintainers)

This project uses semantic versioning and automated releases:

```bash
# Prerequisites
pip install bump2version
brew install git-cliff gh
gh auth login

# Create a release (patch, minor, or major)
make release-minor

# This will:
# - Run tests
# - Bump version
# - Generate changelog
# - Build multi-platform images
# - Push to GHCR
# - Create GitHub release
```

**Release Commands:**
- `make release-patch` - Bug fixes (0.1.0 → 0.1.1)
- `make release-minor` - New features (0.1.0 → 0.2.0)
- `make release-major` - Breaking changes (0.1.0 → 1.0.0)

**Individual Steps:**
- `make show-version` - Show current version
- `make changelog` - Generate changelog
- `make build-multiplatform` - Build for amd64 + arm64
- `make push-ghcr` - Push to GitHub Container Registry

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Docling](https://docling-project.github.io/docling/) by IBM Research
- Uses [Click](https://click.palletsprojects.com/) for CLI interface
- Package management with [uv](https://github.com/astral-sh/uv)
- Image extraction powered by Docling's built-in capabilities

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review [Docling Documentation](https://docling-project.github.io/docling/)
- Open an issue on [GitHub](https://github.com/rennochj/docling-container/issues)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Recent Highlights
- **Glob Pattern Filtering**: Filter files in batch mode using patterns (e.g., `--pattern "*.pdf"`)
- **OCR Support**: Automatic text extraction from images and scanned PDFs
- **Table Structure Detection**: Advanced table recognition and extraction
- **URL Support**: Convert documents directly from URLs (e.g., arxiv.org papers)
- **Image Extraction**: Extract figures and tables with configurable resolution
- **Smart Image Handling**: Option to exclude full page renders (only extract meaningful figures/tables)
- **GHCR Integration**: Pre-built images available on GitHub Container Registry
- **Comprehensive Makefile**: Easy-to-use targets for common operations
- **Shell Aliases**: Quick setup for macOS, Linux, and Windows users
- **YAML Configuration**: Support for configuration files to set default options
