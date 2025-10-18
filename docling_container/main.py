"""Main CLI interface for docling-container."""

import click
import logging
from pathlib import Path
from typing import Optional
import re

from .converter import DocumentConverter
from .logger import setup_logging
from .config import Config


# Supported formats as per PRD
INPUT_FORMATS = [
    "html", "md", "markdown", "docx", "pptx", "xlsx",
    "pdf", "asciidoc", "adoc", "csv", "png", "jpg",
    "jpeg", "tiff", "bmp", "webp"
]

OUTPUT_FORMATS = ["html", "markdown", "json", "text", "doctags"]


def is_url(string: str) -> bool:
    """Check if a string is a valid URL.

    Args:
        string: String to check

    Returns:
        True if string is a URL, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(string) is not None


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0")
def cli(ctx):
    """Docling Container - Document conversion tool.

    Convert documents between various formats including HTML, Markdown,
    Microsoft Office formats, PDFs, images, and more.
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('input_path', type=str, default='/input')
@click.argument('output_dir', type=click.Path(path_type=Path), default='/output')
@click.option(
    '--output-format', '-f',
    type=click.Choice(OUTPUT_FORMATS, case_sensitive=False),
    default='markdown',
    help='Output format for converted documents.'
)
@click.option(
    '--batch/--no-batch', '-b',
    default=True,
    help='Enable batch processing for directories.'
)
@click.option(
    '--recursive/--no-recursive', '-r',
    default=False,
    help='Recursively process subdirectories.'
)
@click.option(
    '--log-level',
    type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
    default='INFO',
    help='Logging verbosity level.'
)
@click.option(
    '--log-file',
    type=click.Path(path_type=Path),
    help='Optional log file path.'
)
@click.option(
    '--config',
    type=click.Path(exists=True, path_type=Path),
    help='Path to configuration file.'
)
@click.option(
    '--preserve-structure/--no-preserve-structure',
    default=True,
    help='Preserve original document structure during conversion.'
)
@click.option(
    '--fail-fast/--no-fail-fast',
    default=False,
    help='Stop on first error (fail-fast) or continue processing.'
)
def convert(
    input_path: str,
    output_dir: Path,
    output_format: str,
    batch: bool,
    recursive: bool,
    log_level: str,
    log_file: Optional[Path],
    config: Optional[Path],
    preserve_structure: bool,
    fail_fast: bool
):
    """Convert document(s) from INPUT_PATH to OUTPUT_DIR.

    INPUT_PATH can be a URL, a single file, or a directory for batch processing.
    Defaults to /input directory if not specified.

    OUTPUT_DIR is where converted documents will be saved.
    Defaults to /output directory if not specified.

    Examples:

        # Convert single PDF from /input to /output (container usage)
        docling-convert document.pdf

        # Convert with custom paths
        docling-convert /custom/path/document.pdf /custom/output

        # Convert from URL
        docling-convert https://arxiv.org/pdf/2408.09869 /output

        # Batch convert all files in /input directory
        docling-convert -f html --batch

        # Recursive processing with custom log level
        docling-convert -r --log-level DEBUG
    """
    # Setup logging
    logger = setup_logging(log_level, log_file)

    try:
        # Load configuration if provided
        app_config = Config(config)
        if config:
            logger.info(f"Loaded configuration from {config}")

        # Initialize converter
        converter = DocumentConverter(
            output_format=output_format,
            preserve_structure=preserve_structure,
            logger=logger
        )

        # Check if input is a URL
        if is_url(input_path):
            logger.info(f"Converting document from URL: {input_path}")
            converter.convert_url(input_path, output_dir)
            logger.info("Conversion completed successfully!")
            return

        # Handle file paths
        path_obj = Path(input_path)

        # Resolve input path
        # If input_path is relative and /input exists, treat it as relative to /input
        input_base = Path('/input')
        if not path_obj.is_absolute() and input_base.exists():
            resolved_input = input_base / input_path
            if resolved_input.exists():
                path_obj = resolved_input

        # Ensure input path exists
        if not path_obj.exists():
            raise click.ClickException(f"Input path does not exist: {path_obj}")

        # Check if input is file or directory
        if path_obj.is_file():
            logger.info(f"Converting single file: {path_obj}")
            converter.convert_file(path_obj, output_dir)
        elif path_obj.is_dir():
            if not batch:
                logger.error("Input is a directory but batch processing is disabled.")
                raise click.ClickException(
                    "Use --batch flag to process directories."
                )
            logger.info(f"Batch converting files from: {path_obj}")
            converter.convert_batch(
                path_obj,
                output_dir,
                recursive=recursive,
                fail_fast=fail_fast
            )
        else:
            raise click.ClickException(f"Invalid input path: {path_obj}")

        logger.info("Conversion completed successfully!")

    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        raise click.ClickException(str(e))


@cli.command()
def formats():
    """List all supported input and output formats."""
    click.echo("\nSupported Input Formats:")
    click.echo("=" * 50)
    for fmt in INPUT_FORMATS:
        click.echo(f"  • {fmt}")

    click.echo("\nSupported Output Formats:")
    click.echo("=" * 50)
    for fmt in OUTPUT_FORMATS:
        click.echo(f"  • {fmt}")
    click.echo()


if __name__ == "__main__":
    cli()
