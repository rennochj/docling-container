"""Tests for the logging module."""

import pytest
import logging
from pathlib import Path
from docling_container.logger import setup_logging, ConversionLogger


class TestLogging:
    """Test cases for logging functionality."""

    def test_setup_logging_default(self):
        """Test default logging setup."""
        logger = setup_logging()
        assert logger.name == "docling_container"
        assert logger.level == logging.INFO

    def test_setup_logging_debug(self):
        """Test logging setup with DEBUG level."""
        logger = setup_logging(log_level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logging_error(self):
        """Test logging setup with ERROR level."""
        logger = setup_logging(log_level="ERROR")
        assert logger.level == logging.ERROR

    def test_conversion_logger_init(self):
        """Test ConversionLogger initialization."""
        logger = setup_logging()
        conv_logger = ConversionLogger(logger)

        assert conv_logger.total_files == 0
        assert conv_logger.successful_conversions == 0
        assert conv_logger.failed_conversions == 0
        assert len(conv_logger.errors) == 0

    def test_conversion_logger_file_start(self):
        """Test logging file start."""
        logger = setup_logging()
        conv_logger = ConversionLogger(logger)

        file_path = Path("/test/document.pdf")
        conv_logger.log_file_start(file_path)

        assert conv_logger.total_files == 1

    def test_conversion_logger_file_success(self):
        """Test logging successful conversion."""
        logger = setup_logging()
        conv_logger = ConversionLogger(logger)

        input_path = Path("/test/document.pdf")
        output_path = Path("/output/document.md")

        conv_logger.log_file_start(input_path)
        conv_logger.log_file_success(input_path, output_path)

        assert conv_logger.successful_conversions == 1
        assert conv_logger.failed_conversions == 0

    def test_conversion_logger_file_error(self):
        """Test logging failed conversion."""
        logger = setup_logging()
        conv_logger = ConversionLogger(logger)

        file_path = Path("/test/document.pdf")
        error = ValueError("Test error")

        conv_logger.log_file_start(file_path)
        conv_logger.log_file_error(file_path, error)

        assert conv_logger.successful_conversions == 0
        assert conv_logger.failed_conversions == 1
        assert len(conv_logger.errors) == 1

    def test_conversion_logger_multiple_files(self):
        """Test logging multiple file conversions."""
        logger = setup_logging()
        conv_logger = ConversionLogger(logger)

        # Process 5 files: 3 successful, 2 failed
        for i in range(3):
            file_path = Path(f"/test/doc{i}.pdf")
            output_path = Path(f"/output/doc{i}.md")
            conv_logger.log_file_start(file_path)
            conv_logger.log_file_success(file_path, output_path)

        for i in range(2):
            file_path = Path(f"/test/bad{i}.pdf")
            conv_logger.log_file_start(file_path)
            conv_logger.log_file_error(file_path, ValueError("Error"))

        assert conv_logger.total_files == 5
        assert conv_logger.successful_conversions == 3
        assert conv_logger.failed_conversions == 2
        assert len(conv_logger.errors) == 2
