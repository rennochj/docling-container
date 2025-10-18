# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project creates a Docker container for Docling, a document conversion tool. The container provides a CLI interface to convert various document formats (HTML, Markdown, DOCX, PPTX, XLSX, PDF, ASCIIDOC, CSV, and images) to output formats (HTML, Markdown, JSON, Text, Doctags).

Key design principles from prd.md:
- Use Python 3.13 as the base
- Use `uv` as the package manager (not pip)
- Multi-stage Docker build for efficiency
- Support mount points for input/output directories
- Batch processing capability
- Comprehensive logging and error handling

## Development Setup

### Package Management
This project uses `uv` for dependency management. Common commands:

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Run Python with the virtual environment
uv run python main.py

# Run tests (when implemented)
uv run pytest
```

### Docker Commands
```bash
# Build the container
docker build -t docling-forge .

# Run with mounted volumes (uses /input and /output as defaults)
docker run -v /path/to/input:/input -v /path/to/output:/output docling-forge convert document.pdf

# Batch convert all files in input directory
docker run -v /path/to/input:/input -v /path/to/output:/output docling-forge convert --batch

# Custom paths can still be specified
docker run -v /data:/data docling-forge convert /data/file.pdf /data/output
```

## Architecture

### Current Structure
- `docling_forge/main.py`: Entry point for the CLI with Click framework
- `docling_forge/converter.py`: Document conversion logic using Docling API
- `docling_forge/logger.py`: Structured logging system with conversion statistics
- `docling_forge/config.py`: YAML configuration file support
- `Dockerfile`: Multi-stage build (uv install + slim runtime)
- `pyproject.toml`: Project metadata and dependencies (uv-managed)
- `tests/`: Comprehensive test suite (28 tests covering CLI, converter, logging)

### Docling Integration
The official Docling documentation is at https://docling-project.github.io/docling/getting_started/

Implementation uses:
- Python API to drive conversions (not CLI invocation)
- Batch processing for multiple files with progress tracking
- Document structure preservation during conversion
- Configurable options via CLI arguments or YAML config file

### Container Design
Multi-stage Docker build:
- **Stage 1 (builder)**: Uses uv to install dependencies in Python 3.13
- **Stage 2 (runtime)**: Slim image with only runtime artifacts
- **Default paths**: `/input` for source files, `/output` for converted files
- **CLI interface**: Exposed via ENTRYPOINT for easy Docker execution
- **Error handling**: Comprehensive logging with conversion statistics

## Supported Formats

**Input:** HTML, Markdown, DOCX, PPTX, XLSX, PDF, ASCIIDOC, CSV, PNG, JPEG, TIFF, BMP, WEBP

**Output:** HTML, Markdown, JSON, Text, Doctags
