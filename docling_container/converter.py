"""Document converter using Docling."""

import logging
from pathlib import Path
from typing import List, Optional
import mimetypes

from docling.document_converter import DocumentConverter as DoclingConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption
from docling_core.types.doc import PictureItem, TableItem, ImageRefMode

from .logger import ConversionLogger


# Map file extensions to Docling InputFormat
EXTENSION_TO_FORMAT = {
    # Documents
    '.pdf': InputFormat.PDF,
    '.docx': InputFormat.DOCX,
    '.pptx': InputFormat.PPTX,
    '.html': InputFormat.HTML,
    '.htm': InputFormat.HTML,
    '.md': InputFormat.MD,
    '.asciidoc': InputFormat.ASCIIDOC,
    '.adoc': InputFormat.ASCIIDOC,
    # Images
    '.png': InputFormat.IMAGE,
    '.jpg': InputFormat.IMAGE,
    '.jpeg': InputFormat.IMAGE,
    '.tiff': InputFormat.IMAGE,
    '.tif': InputFormat.IMAGE,
    '.bmp': InputFormat.IMAGE,
    '.webp': InputFormat.IMAGE,
}


class DocumentConverter:
    """Wrapper for Docling document conversion."""

    def __init__(
        self,
        output_format: str = "markdown",
        preserve_structure: bool = True,
        export_images: bool = False,
        images_scale: float = 2.0,
        export_page_images: bool = False,
        logger: Optional[logging.Logger] = None
    ):
        """Initialize the document converter.

        Args:
            output_format: Target output format (markdown, html, json, text, doctags)
            preserve_structure: Whether to preserve document structure
            export_images: Whether to extract and save images
            images_scale: Resolution scale for images (1.0 = 72 DPI, 2.0 = 144 DPI)
            export_page_images: Whether to extract full page images (default: False)
            logger: Optional logger instance
        """
        self.output_format = output_format.lower()
        self.preserve_structure = preserve_structure
        self.export_images = export_images
        self.images_scale = images_scale
        self.export_page_images = export_page_images
        self.logger = logger or logging.getLogger(__name__)

        # Initialize Docling converter with optimized settings
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True

        # Enable image generation if export_images is True
        if export_images:
            pipeline_options.images_scale = images_scale
            pipeline_options.generate_page_images = export_page_images
            pipeline_options.generate_picture_images = True

        self.docling_converter = DoclingConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        self.conversion_logger = ConversionLogger(self.logger)

    def _detect_format(self, file_path: Path) -> Optional[InputFormat]:
        """Detect the input format from file extension.

        Args:
            file_path: Path to the input file

        Returns:
            InputFormat enum value or None if unsupported
        """
        extension = file_path.suffix.lower()
        return EXTENSION_TO_FORMAT.get(extension)

    def _get_output_extension(self) -> str:
        """Get the file extension for the output format."""
        extension_map = {
            'markdown': '.md',
            'html': '.html',
            'json': '.json',
            'text': '.txt',
            'doctags': '.doctags'
        }
        return extension_map.get(self.output_format, '.md')

    def _extract_images(self, result, output_dir: Path, doc_name: str) -> int:
        """Extract and save images from conversion result.

        Args:
            result: Docling conversion result
            output_dir: Directory to save images
            doc_name: Base name for the document (used in image filenames)

        Returns:
            Number of images extracted
        """
        if not self.export_images:
            return 0

        # Create images subdirectory
        images_dir = output_dir / f"{doc_name}_images"
        images_dir.mkdir(parents=True, exist_ok=True)

        # Relative path for image references (relative to output document)
        images_dir_name = f"{doc_name}_images"

        image_count = 0

        # Extract page images (only if export_page_images is True)
        if self.export_page_images:
            for page_no, page in result.document.pages.items():
                if hasattr(page, 'image') and page.image and hasattr(page.image, 'pil_image'):
                    page_image_filename = f"page_{page.page_no}.png"
                    page_image_path = images_dir / page_image_filename
                    try:
                        page.image.pil_image.save(str(page_image_path), format="PNG")
                        # Update the image URI to point to the saved file
                        page.image.uri = f"{images_dir_name}/{page_image_filename}"
                        self.logger.debug(f"Saved page image: {page_image_path}")
                        image_count += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to save page {page.page_no} image: {e}")

        # Extract figure and table images
        picture_counter = 0
        table_counter = 0

        for element, _level in result.document.iterate_items():
            if isinstance(element, PictureItem):
                if hasattr(element, 'image') and element.image and hasattr(element.image, 'pil_image'):
                    picture_counter += 1
                    picture_filename = f"figure_{picture_counter}.png"
                    picture_path = images_dir / picture_filename
                    try:
                        element.image.pil_image.save(str(picture_path), format="PNG")
                        # Update the image URI to point to the saved file
                        element.image.uri = f"{images_dir_name}/{picture_filename}"
                        self.logger.debug(f"Saved figure: {picture_path}")
                        image_count += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to save figure {picture_counter}: {e}")

            elif isinstance(element, TableItem):
                if hasattr(element, 'image') and element.image and hasattr(element.image, 'pil_image'):
                    table_counter += 1
                    table_filename = f"table_{table_counter}.png"
                    table_path = images_dir / table_filename
                    try:
                        element.image.pil_image.save(str(table_path), format="PNG")
                        # Update the image URI to point to the saved file
                        element.image.uri = f"{images_dir_name}/{table_filename}"
                        self.logger.debug(f"Saved table: {table_path}")
                        image_count += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to save table {table_counter}: {e}")

        if image_count > 0:
            self.logger.info(f"Extracted {image_count} images to {images_dir}")

        return image_count

    def convert_file(self, input_path: Path, output_dir: Path) -> Path:
        """Convert a single file.

        Args:
            input_path: Path to input file
            output_dir: Directory for output file

        Returns:
            Path to the converted output file

        Raises:
            ValueError: If file format is unsupported
            RuntimeError: If conversion fails
        """
        self.conversion_logger.log_file_start(input_path)

        # Detect input format
        input_format = self._detect_format(input_path)
        if input_format is None:
            error_msg = f"Unsupported file format: {input_path.suffix}"
            raise ValueError(error_msg)

        try:
            # Perform conversion using Docling
            self.logger.debug(f"Converting {input_path} with format {input_format}")
            result = self.docling_converter.convert(str(input_path))

            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate output filename
            output_filename = input_path.stem + self._get_output_extension()
            output_path = output_dir / output_filename

            # Extract images if requested
            if self.export_images:
                self._extract_images(result, output_dir, input_path.stem)

            # Export to the desired format
            self._export_result(result, output_path)

            self.conversion_logger.log_file_success(input_path, output_path)
            return output_path

        except Exception as e:
            self.conversion_logger.log_file_error(input_path, e)
            raise RuntimeError(f"Failed to convert {input_path}: {e}") from e

    def convert_url(self, url: str, output_dir: Path) -> Path:
        """Convert a document from a URL.

        Args:
            url: URL of the document to convert
            output_dir: Directory for output file

        Returns:
            Path to the converted output file

        Raises:
            RuntimeError: If conversion fails
        """
        self.logger.info(f"Processing URL: {url}")

        try:
            # Perform conversion using Docling (supports URLs natively)
            self.logger.debug(f"Converting document from URL: {url}")
            result = self.docling_converter.convert(url)

            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)

            # Generate output filename from URL
            # Extract filename from URL or use a default
            import urllib.parse
            parsed_url = urllib.parse.urlparse(url)
            url_path = parsed_url.path
            if url_path and '/' in url_path:
                filename = url_path.split('/')[-1]
                # Remove extension if present
                if '.' in filename:
                    filename = filename.rsplit('.', 1)[0]
            else:
                filename = 'document'

            output_filename = filename + self._get_output_extension()
            output_path = output_dir / output_filename

            # Extract images if requested
            if self.export_images:
                self._extract_images(result, output_dir, filename)

            # Export to the desired format
            self._export_result(result, output_path)

            self.logger.info(f"Successfully converted URL to: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Failed to convert URL {url}: {e}")
            raise RuntimeError(f"Failed to convert URL {url}: {e}") from e

    def _export_result(self, result, output_path: Path):
        """Export conversion result to specified format.

        Args:
            result: Docling conversion result
            output_path: Path to save the output
        """
        # Use REFERENCED mode for images if we're extracting them
        image_mode = ImageRefMode.REFERENCED if self.export_images else ImageRefMode.PLACEHOLDER

        if self.output_format == 'markdown':
            content = result.document.export_to_markdown(image_mode=image_mode)
        elif self.output_format == 'html':
            content = result.document.export_to_html(image_mode=image_mode)
        elif self.output_format == 'json':
            content = result.document.export_to_json()
        elif self.output_format == 'text':
            content = result.document.export_to_text()
        elif self.output_format == 'doctags':
            content = result.document.export_to_document_tokens()
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            if isinstance(content, str):
                f.write(content)
            else:
                import json
                json.dump(content, f, indent=2, ensure_ascii=False)

    def convert_batch(
        self,
        input_dir: Path,
        output_dir: Path,
        recursive: bool = False,
        fail_fast: bool = False
    ) -> List[Path]:
        """Convert multiple files from a directory.

        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            recursive: Whether to process subdirectories
            fail_fast: Whether to stop on first error

        Returns:
            List of successfully converted output file paths

        Raises:
            RuntimeError: If fail_fast is True and conversion fails
        """
        self.logger.info(f"Starting batch conversion from {input_dir}")
        self.logger.info(f"Output directory: {output_dir}")
        self.logger.info(f"Recursive: {recursive}, Fail-fast: {fail_fast}")

        # Find all supported files
        supported_files = []
        pattern = "**/*" if recursive else "*"

        for file_path in input_dir.glob(pattern):
            if file_path.is_file() and self._detect_format(file_path):
                supported_files.append(file_path)

        self.logger.info(f"Found {len(supported_files)} supported files")

        # Convert each file
        converted_files = []
        for file_path in supported_files:
            try:
                # Create subdirectory structure if recursive
                if recursive:
                    relative_path = file_path.relative_to(input_dir)
                    file_output_dir = output_dir / relative_path.parent
                else:
                    file_output_dir = output_dir

                output_path = self.convert_file(file_path, file_output_dir)
                converted_files.append(output_path)

            except Exception as e:
                if fail_fast:
                    self.conversion_logger.log_summary()
                    raise RuntimeError(
                        f"Batch conversion stopped due to error: {e}"
                    ) from e
                # Otherwise continue processing remaining files

        # Log summary
        self.conversion_logger.log_summary()

        return converted_files

    def get_supported_formats(self) -> dict:
        """Get list of supported input and output formats.

        Returns:
            Dictionary with 'input' and 'output' format lists
        """
        return {
            'input': list(set(EXTENSION_TO_FORMAT.keys())),
            'output': ['markdown', 'html', 'json', 'text', 'doctags']
        }
