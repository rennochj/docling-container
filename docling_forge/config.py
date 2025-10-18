"""Configuration file handling for docling-forge."""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for docling-forge."""

    DEFAULT_CONFIG = {
        'output_format': 'markdown',
        'preserve_structure': True,
        'log_level': 'INFO',
        'batch': True,
        'recursive': False,
        'fail_fast': False,
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.

        Args:
            config_path: Optional path to YAML configuration file
        """
        self.config = self.DEFAULT_CONFIG.copy()

        if config_path and config_path.exists():
            self.load_from_file(config_path)

    def load_from_file(self, config_path: Path):
        """Load configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Raises:
            ValueError: If config file is invalid
        """
        try:
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)

            if file_config:
                # Validate and update configuration
                for key, value in file_config.items():
                    if key in self.DEFAULT_CONFIG:
                        self.config[key] = value
                    else:
                        raise ValueError(f"Unknown configuration option: {key}")

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}") from e
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self.config.copy()

    @classmethod
    def create_example_config(cls, output_path: Path):
        """Create an example configuration file.

        Args:
            output_path: Path where to save the example config
        """
        example_config = """# Docling Container Configuration File
# This file contains default settings for document conversion

# Output format: markdown, html, json, text, or doctags
output_format: markdown

# Preserve original document structure during conversion
preserve_structure: true

# Logging verbosity level: DEBUG, INFO, WARNING, or ERROR
log_level: INFO

# Enable batch processing for directories
batch: true

# Recursively process subdirectories
recursive: false

# Stop processing on first error
fail_fast: false
"""
        with open(output_path, 'w') as f:
            f.write(example_config)
