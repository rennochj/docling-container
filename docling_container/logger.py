"""Logging configuration for docling-container."""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


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
    logger = logging.getLogger("docling_container")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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

    return logger


class ConversionLogger:
    """Helper class for tracking conversion statistics."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.start_time = datetime.now()
        self.total_files = 0
        self.successful_conversions = 0
        self.failed_conversions = 0
        self.errors = []

    def log_file_start(self, file_path: Path):
        """Log the start of a file conversion."""
        self.total_files += 1
        self.logger.info(f"Processing file {self.total_files}: {file_path.name}")

    def log_file_success(self, file_path: Path, output_path: Path):
        """Log a successful file conversion."""
        self.successful_conversions += 1
        self.logger.info(f"Successfully converted: {file_path.name} -> {output_path.name}")

    def log_file_error(self, file_path: Path, error: Exception):
        """Log a failed file conversion."""
        self.failed_conversions += 1
        error_msg = f"Failed to convert {file_path.name}: {str(error)}"
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
