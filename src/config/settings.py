# AutoPwnGPT Settings Manager

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-22

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import ValidationError

from .defaults import DEFAULT_CONFIG
from .schema import ConfigSchema
from ..utils.file_utils import load_yaml, save_yaml
from ..utils.validation import validate_path

logger = logging.getLogger(__name__)

class SettingsManager:
    """Central configuration settings manager for AutoPwnGPT"""
    
    def __init__(self, config_path: Optional[str] = None):
        self._config = DEFAULT_CONFIG.copy()
        self._user_config = {}
        self._config_path = config_path or os.getenv('AUTOPWNGPT_CONFIG', 'config.yaml')
        self._schema = ConfigSchema
        
        # Initialize with defaults and load user config
        self._load_config()
        
    def _load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self._config_path):
                user_config = load_yaml(self._config_path)
                self._validate_config(user_config)
                self._user_config = user_config
                self._merge_configs()
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            raise

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration against schema"""
        try:
            self._schema.parse_obj(config)
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            raise

    def _merge_configs(self) -> None:
        """Merge default and user configurations"""
        for key, value in self._user_config.items():
            if key in self._config:
                if isinstance(value, dict) and isinstance(self._config[key], dict):
                    self._config[key].update(value)
                else:
                    self._config[key] = value
            else:
                self._config[key] = value

    def save_config(self, path: Optional[str] = None) -> None:
        """Save current configuration to file"""
        save_path = path or self._config_path
        try:
            save_yaml(save_path, self._config)
        except Exception as e:
            logger.error(f"Failed to save config: {str(e)}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any, save: bool = False) -> None:
        """Set a configuration value"""
        self._config[key] = value
        if save:
            self.save_config()

    def reload(self) -> None:
        """Reload configuration from file"""
        self._load_config()

    @property
    def all_settings(self) -> Dict[str, Any]:
        """Get all current settings"""
        return self._config.copy()

# Global settings instance
settings = SettingsManager()
