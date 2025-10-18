# Docling Forge

[![GitHub release](https://img.shields.io/github/v/release/rennochj/docling-forge)](https://github.com/rennochj/docling-forge/releases)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/rennochj/docling-forge/pkgs/container/docling-forge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Docker-based document conversion tool built with [Docling](https://docling-project.github.io/docling/). Transform documents between various formats including markdown, HTML, JSON, text, and more.

## Features

- **Multiple Input Formats**: PDF, DOCX, PPTX, HTML, Markdown, ASCIIDOC, and images (PNG, JPEG, TIFF, BMP, WEBP)
- **Multiple Output Formats**: Markdown, HTML, JSON, Text, Doctags
- **URL Support**: Convert documents directly from URLs (e.g., arxiv.org papers, online PDFs)
- **Image Extraction**: Extract and save images (figures, tables) from documents with configurable resolution
- **OCR Support**: Built-in OCR for extracting text from images and scanned PDFs (can be disabled for digital-only docs)
- **Table Detection**: Advanced table structure recognition and extraction (can be disabled for faster processing)
- **Pre-cached Models**: OCR models downloaded during build for instant first-run performance
- **Parallel Batch Processing**: Multi-threaded conversion for 30-60% faster batch operations
- **Performance Optimized**: Fast startup (80-90% faster), optimized Docker build, minimal image size
- **Pattern Filtering**: Use glob patterns to selectively process files (e.g., only PDFs)
- **Organized Output**: Files automatically organized in subdirectories (default: `docling/`, configurable)
- **Recursive Processing**: Process nested directory structures
- **Comprehensive Logging**: Detailed logs with conversion statistics (clean output, no log spam)
- **Flexible Configuration**: YAML config file support for default settings
- **Error Handling**: Graceful error handling with meaningful messages

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
- **Multi-stage Build**: Optimized for minimal image size with layer caching
- **Package Manager**: UV (fast Python package installer with lock file support)
- **Docling Version**: 2.0.0+
- **Architecture**: Supports amd64 and arm64
- **OCR Models**: RapidOCR models pre-downloaded during build (no runtime downloads needed)
- **Parallel Processing**: ThreadPoolExecutor for concurrent file conversion
- **Startup Time**: Lazy module loading for 80-90% faster CLI response
- **Dependencies**: Optimized with opencv-python-headless for smaller image size

## Performance

This container is highly optimized for both speed and efficiency:

- **⚡ Fast Startup**: 80-90% faster CLI response with lazy module loading
- **🚀 Parallel Processing**: Auto-detects CPU cores for 30-60% faster batch conversions
- **⚙️ Configurable Features**: Disable OCR (`--no-ocr`) or table detection (`--no-table-detection`) for 50-80% speed boost on digital documents
- **📦 Efficient Builds**: Docker layer caching reduces rebuild time by 3-5 minutes
- **💾 Optimized Size**: ~30MB smaller with opencv-python-headless
- **🎯 Pre-cached Models**: OCR models downloaded during build (no runtime delays)

**Example Performance**: Converting 7 documents in batch mode with 14 workers takes ~75 seconds with full OCR and table detection enabled.

## Installation

### Prerequisites
- Docker installed on your system
- Input documents to convert

### Using Pre-built Image (Recommended)

Pull the latest image from GitHub Container Registry:

```bash
# Pull latest version
docker pull ghcr.io/rennochj/docling-forge:latest

# Or pull a specific version
docker pull ghcr.io/rennochj/docling-forge:0.3.1
```

### Building from Source

```bash
# Clone the repository
git clone https://github.com/rennochj/docling-forge.git
cd docling-forge

# Build the Docker image
docker build -t docling-forge .

# Or build for multiple platforms
make build-multiplatform
```

## Quick Start

The fastest way to get started with the pre-built image:

```bash
# Pull the image
docker pull ghcr.io/rennochj/docling-forge:latest

# Convert a PDF
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  ghcr.io/rennochj/docling-forge:latest \
  convert document.pdf
```

### Shell Aliases (Recommended)

For easier usage, add an alias to your shell configuration:

**macOS / Linux (Bash/Zsh):**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias docling='docker run --rm -v $(pwd)/input:/input -v $(pwd)/output:/output ghcr.io/rennochj/docling-forge:latest'

# Reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc
```

**Windows (PowerShell):**

```powershell
# Add to your PowerShell profile (run: notepad $PROFILE)
function docling {
    docker run --rm -v ${PWD}/input:/input -v ${PWD}/output:/output ghcr.io/rennochj/docling-forge:latest $args
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

The application uses `/input` and `/output` as default directories, so you only need to specify filenames.

**Note**: By default, converted files are organized in a `docling/` subdirectory within the output directory (e.g., `output/docling/document.md`). You can customize this with `--output-subdir`.

Convert a single file:

```bash
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-forge convert document.pdf

# Output: /path/to/output/docling/document.md
```

### URL Conversion

Convert documents directly from URLs:

```bash
docker run -v /path/to/output:/output \
  docling-forge convert https://arxiv.org/pdf/2408.09869 /output
```

```bash
# Convert any publicly accessible PDF
docker run -v $(pwd)/output:/output \
  docling-forge convert https://example.com/document.pdf /output -f markdown
```

### Image Extraction

Extract images from documents while converting. By default, only figures and tables are extracted:

```bash
# Extract figures and tables (recommended)
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-forge convert document.pdf /output --export-images
```

```bash
# Extract with high resolution (4x scale = 288 DPI)
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-forge convert document.pdf /output --export-images --images-scale 4.0
```

```bash
# Extract ALL images including full page renders
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-forge convert document.pdf /output --export-images --export-page-images
```

Images are saved to a subdirectory named `{document}_images/` and referenced in the output:
```markdown
![Image](document_images/figure_1.png)
```

### Batch Conversion

Convert all documents in the input directory:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert --batch
```

Or use an explicit directory:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert . --batch
```

Filter files using glob patterns:

```bash
# Convert only PDF files
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert --batch --pattern "*.pdf"

# Convert multiple file types
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert --batch --pattern "*.pdf" --pattern "*.docx"

# Pattern matching for specific filenames
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert --batch --pattern "report_*.pdf"
```

### Recursive Processing

Process directories recursively:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert -r --log-level INFO
```

Combine recursive mode with patterns:

```bash
# Convert all PDFs recursively
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert -r --pattern "*.pdf"

# Convert specific file types from all subdirectories
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert -r --pattern "*.pdf" --pattern "*.docx" --pattern "*.pptx"
```

### Output Format Selection

Convert to HTML instead of markdown:

```bash
docker run -v /path/to/input:/input -v /path/to/output:/output \
  docling-forge convert document.pdf -f html
```

### Advanced Options

Full example with all options:

```bash
docker run -v /path/to/docs:/input -v /path/to/output:/output \
  docling-forge convert \
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
  docling-forge convert /data/document.pdf /data/output
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
| `--workers` | | `CPU count` | Number of parallel worker threads for batch processing |
| `--ocr` / `--no-ocr` | | `True` | Enable/disable OCR (20-40% faster when disabled for digital docs) |
| `--table-detection` / `--no-table-detection` | | `True` | Enable/disable table detection (10-20% faster when disabled) |
| `--output-subdir` | | `docling` | Subdirectory name within output directory for converted files |
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
  docling-forge convert report.pdf
```

**Output**: `output/report.md`

### Example 2: Convert PDF from URL with Image Extraction

```bash
docker run -v $(pwd)/output:/output \
  docling-forge convert https://arxiv.org/pdf/2408.09869 /output \
    -f markdown --export-images
```

**Output**:
- `output/2408.09869.md` - Converted markdown
- `output/2408.09869_images/` - Directory with extracted images

### Example 3: Batch Convert All Office Documents

```bash
docker run -v $(pwd)/documents:/input -v $(pwd)/converted:/output \
  docling-forge convert -f html --batch
```

**Result**: All supported documents in `documents/` converted to HTML in `converted/`

### Example 4: Recursive Conversion with Logging

```bash
docker run -v $(pwd)/docs:/input -v $(pwd)/output:/output -v $(pwd)/logs:/logs \
  docling-forge convert \
    -r \
    --log-level DEBUG \
    --log-file /logs/conversion.log
```

**Result**: Recursively processes all documents with debug logging saved to `logs/conversion.log`

### Example 5: Convert Images to Text with OCR

```bash
docker run -v $(pwd)/images:/input -v $(pwd)/text:/output \
  docling-forge convert -f text --batch
```

**Result**: OCR extraction from images exported as text files

### Example 6: Convert PowerPoint with High-Resolution Images

```bash
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-forge convert presentation.pptx /output \
    --export-images --images-scale 4.0
```

**Result**: Markdown with 288 DPI images extracted

### Example 7: Batch Convert with File Patterns

```bash
# Convert only PDF files
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert --batch --pattern "*.pdf"

# Convert multiple specific file types
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert --batch --pattern "*.pdf" --pattern "*.docx" --pattern "*.pptx"

# Pattern matching with recursive processing
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert -r --pattern "report_*.pdf"
```

**Result**: Only files matching the specified pattern(s) are converted

### Example 8: List Supported Formats

```bash
docker run docling-forge formats
```

### Example 9: Fast Batch Processing with Parallel Workers

```bash
# Use 8 parallel workers for faster processing
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert --batch --workers 8

# Process with maximum parallelism (auto-detects CPU cores)
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert --batch
```

**Result**: Files processed concurrently for 30-60% faster batch conversions

### Example 10: Speed Up Digital Document Processing

```bash
# Disable OCR and table detection for digital-only PDFs
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-forge convert document.pdf /output \
    --no-ocr --no-table-detection

# Batch process digital documents at maximum speed
docker run -v $(pwd)/documents:/input -v $(pwd)/output:/output \
  docling-forge convert --batch --workers 8 \
    --no-ocr --no-table-detection --pattern "*.pdf"
```

**Result**: 50-80% faster processing for documents that don't need OCR or table extraction

### Example 11: Organize Output with Custom Subdirectories

```bash
# Default behavior - files saved to output/docling/
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-forge convert document.pdf /output

# Custom subdirectory name
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-forge convert document.pdf /output --output-subdir converted

# Different subdirectories for different projects
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  docling-forge convert --batch --output-subdir project-alpha
```

**Result**:
- Files organized in `output/docling/document.md` (default)
- Or `output/converted/document.md` (custom)
- Or `output/project-alpha/` for batch projects

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
docling-forge/
├── docling_forge/         # Main application package
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
docker run docling-forge formats
```

### Issue: Out of Memory

**Problem**: Container runs out of memory with large PDFs

**Solution**: Increase Docker memory limit:

```bash
docker run --memory=4g -v /input:/input -v /output:/output \
  docling-forge convert /input /output
```

### Issue: Conversion Fails Silently

**Problem**: Some files don't convert but no error is shown

**Solution**: Enable debug logging to see detailed error messages:

```bash
docker run -v /input:/input -v /output:/output \
  docling-forge convert /input /output --log-level DEBUG
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
  docling-forge convert doc.pdf /output --export-images

# Includes page renders (usually not needed)
docker run -v /input:/input -v /output:/output \
  docling-forge convert doc.pdf /output --export-images --export-page-images
```

## Performance Tips

1. **Parallel Processing**: Use `--workers N` to control parallelism (automatically uses all CPU cores by default for 30-60% faster batch conversions)
2. **Disable Unnecessary Features**: Use `--no-ocr` for digital-only documents (20-40% faster) and `--no-table-detection` when tables aren't needed (10-20% faster)
3. **Batch Processing**: Use batch mode for multiple files to reuse model loading and enable parallel processing
4. **Memory Allocation**: Allocate sufficient memory for large documents (4GB+ recommended for PDFs with OCR)
5. **Fail-Fast Mode**: Use `--fail-fast` to stop on errors and save processing time
6. **Format Selection**: JSON output is typically faster than other formats
7. **Image Extraction**: Only use `--export-page-images` if you specifically need full page renders
8. **Image Resolution**: Use lower `--images-scale` values (e.g., 1.0 or 2.0) for faster processing
9. **Pattern Filtering**: Use `--pattern` to process only specific file types, avoiding unnecessary work

### Performance Comparison

| Configuration | Relative Speed | Best Use Case |
|---------------|----------------|---------------|
| Default (OCR + Tables + Auto Workers) | 1x (baseline) | Comprehensive document conversion |
| `--workers 8` (parallel) | 1.3-1.6x faster | Batch processing on multi-core systems |
| `--no-ocr --no-table-detection` | 1.5-2x faster | Digital-only documents without tables |
| Combined (parallel + no OCR/tables) | 2-3x faster | Large batches of digital documents |

## Configuration

You can create a configuration file to set default options:

```yaml
# config.yaml
output_format: markdown
preserve_structure: true
log_level: INFO
batch: true
recursive: false
workers: 8              # Number of parallel workers (omit to auto-detect)
ocr: true              # Enable OCR for scanned documents
table_detection: true  # Enable table structure detection
output_subdir: docling # Subdirectory for converted files (default: "docling")
export_images: true
images_scale: 2.0
export_page_images: false
```

Use with:

```bash
docker run -v $(pwd)/config.yaml:/config.yaml -v /input:/input -v /output:/output \
  docling-forge convert /input /output --config /config.yaml
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
- Open an issue on [GitHub](https://github.com/rennochj/docling-forge/issues)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Recent Highlights

**v0.4.0 - Performance Optimizations:**
- **Parallel Batch Processing**: Multi-threaded conversion with `--workers` option (30-60% faster batch operations)
- **Fast Startup**: Lazy module loading provides 80-90% faster CLI response for `--help` and `formats` commands
- **Configurable OCR**: `--no-ocr` option for 20-40% faster processing of digital-only documents
- **Configurable Table Detection**: `--no-table-detection` option for 10-20% speed boost when tables aren't needed
- **Optimized Docker Build**: Better layer caching with uv.lock for 3-5 minute faster rebuilds
- **Smaller Image Size**: Switched to opencv-python-headless, reducing image size by ~30MB
- **Clean Logging**: Properly suppressed RapidOCR log messages for consistent, readable output
- **Pre-cached Models**: OCR models downloaded during build (no runtime downloads)

**Previous Features:**
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
