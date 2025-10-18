"""Logging configuration for docling-container."""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class RapidOCRFilter(logging.Filter):
    """Filter to block all RapidOCR log records."""

    def filter(self, record):
        # Block any record from RapidOCR or rapidocr loggers
        logger_name = record.name.lower()
        return not ('rapidocr' in logger_name or record.name == 'RapidOCR')


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None
) -> logging.Logger:
    """Configure and return a logger with specified settings.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional path to log file

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("docling_forge")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent propagation to root logger to avoid duplicate messages
    logger.propagate = False

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")

    # Configure third-party library loggers to reduce verbosity
    # Set docling and other library loggers to WARNING unless in DEBUG mode
    library_loggers = [
        'docling',
        'docling_core',
        'docling.document_converter',
        'rapidocr',
        'RapidOCR',  # RapidOCR uses this logger name
        'rapidocr_onnxruntime',
        'rapidocr_openvino',
        'rapidocr_paddle',
    ]
    for lib_logger_name in library_loggers:
        lib_logger = logging.getLogger(lib_logger_name)
        if log_level == "DEBUG":
            lib_logger.setLevel(logging.DEBUG)
        else:
            # Completely suppress third-party library logs in non-DEBUG mode
            lib_logger.setLevel(logging.CRITICAL)
            lib_logger.propagate = False
            # Remove all handlers from the library logger to prevent direct output
            # This is especially important for RapidOCR which adds its own StreamHandler
            lib_logger.handlers.clear()

    # Configure root logger to suppress duplicate messages
    root_logger = logging.getLogger()
    if log_level == "DEBUG":
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.WARNING)

    # Add RapidOCR filter to root logger to block all RapidOCR messages globally
    # This catches messages even if RapidOCR adds handlers after our initialization
    if log_level != "DEBUG":
        rapidocr_filter = RapidOCRFilter()
        root_logger.addFilter(rapidocr_filter)

        # Also add to all existing handlers (including stderr)
        for handler in logging.root.handlers + root_logger.handlers:
            if not any(isinstance(f, RapidOCRFilter) for f in handler.filters):
                handler.addFilter(rapidocr_filter)

        # Add filter to stderr handler to catch RapidOCR's direct output
        for handler in logging._handlers.values() if hasattr(logging, '_handlers') else []:
            if isinstance(handler, logging.StreamHandler):
                if not any(isinstance(f, RapidOCRFilter) for f in handler.filters):
                    handler.addFilter(rapidocr_filter)

    return logger


class ConversionLogger:
    """Helper class for tracking conversion statistics (thread-safe)."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.start_time = datetime.now()
        self.total_files = 0
        self.successful_conversions = 0
        self.failed_conversions = 0
        self.errors = []
        # Add thread lock for thread-safe operations
        import threading
        self._lock = threading.Lock()

    def log_file_start(self, file_path: Path):
        """Log the start of a file conversion (thread-safe)."""
        with self._lock:
            self.total_files += 1
            file_number = self.total_files
        self.logger.info(f"Processing file {file_number}: {file_path.name}")

    def log_file_success(self, file_path: Path, output_path: Path):
        """Log a successful file conversion (thread-safe)."""
        with self._lock:
            self.successful_conversions += 1
        self.logger.info(f"Successfully converted: {file_path.name} -> {output_path.name}")

    def log_file_error(self, file_path: Path, error: Exception):
        """Log a failed file conversion (thread-safe)."""
        error_msg = f"Failed to convert {file_path.name}: {str(error)}"
        with self._lock:
            self.failed_conversions += 1
            self.errors.append(error_msg)
        self.logger.error(error_msg)

    def log_summary(self):
        """Log the final conversion summary."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        self.logger.info("=" * 60)
        self.logger.info("CONVERSION SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"Total files processed: {self.total_files}")
        self.logger.info(f"Successful conversions: {self.successful_conversions}")
        self.logger.info(f"Failed conversions: {self.failed_conversions}")

        if self.errors:
            self.logger.info("\nErrors encountered:")
            for error in self.errors:
                self.logger.info(f"  • {error}")

        self.logger.info("=" * 60)
