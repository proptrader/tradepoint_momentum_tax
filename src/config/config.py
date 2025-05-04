"""
Configuration module for TradePoint Momentum Tax.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the application."""

    # Default configuration values
    DEFAULT_CONFIG = {
        "initial_capital": 1000000,  # Default initial capital (X) in rupees
        "max_stocks": 20,           # Default maximum number of stocks (N)
        "input_dir": "input",        # Directory for input files
        "output_dir": "output",      # Directory for output files
    }

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration.

        Args:
            config_file: Path to the configuration file (optional)
        """
        self.config_data = self.DEFAULT_CONFIG.copy()
        
        if config_file and os.path.exists(config_file):
            self._load_config(config_file)
            
        # Ensure directories exist
        self._ensure_directories()

    def _load_config(self, config_file: str) -> None:
        """
        Load configuration from a JSON file.

        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                self.config_data.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration file: {e}")
            print("Using default configuration.")

    def _ensure_directories(self) -> None:
        """Ensure that input and output directories exist."""
        for dir_name in ["input_dir", "output_dir"]:
            directory = self.config_data.get(dir_name)
            if directory:
                Path(directory).mkdir(exist_ok=True)
    
    def get(self, key: str) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key

        Returns:
            The configuration value
        """
        return self.config_data.get(key)
    
    def get_initial_capital(self) -> float:
        """Get the initial capital (X)."""
        return float(self.config_data.get("initial_capital", self.DEFAULT_CONFIG["initial_capital"]))
    
    def get_max_stocks(self) -> int:
        """Get the maximum number of stocks (N)."""
        return int(self.config_data.get("max_stocks", self.DEFAULT_CONFIG["max_stocks"]))
    
    def get_input_dir(self) -> str:
        """Get the input directory path."""
        return self.config_data.get("input_dir", self.DEFAULT_CONFIG["input_dir"])
    
    def get_output_dir(self) -> str:
        """Get the output directory path."""
        return self.config_data.get("output_dir", self.DEFAULT_CONFIG["output_dir"])
    
    def save_config(self, config_file: str) -> None:
        """
        Save the current configuration to a file.

        Args:
            config_file: Path to save the configuration
        """
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config_data, f, indent=4)
        except IOError as e:
            print(f"Error saving configuration: {e}")


# Singleton instance
_config_instance = None


def get_config(config_file: Optional[str] = None) -> Config:
    """
    Get the singleton configuration instance.

    Args:
        config_file: Path to the configuration file (optional)

    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_file)
    return _config_instance 