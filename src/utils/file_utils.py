#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File utilities for AutoPwnGPT.
Provides common file system operations.
"""

import os
import shutil
from pathlib import Path
from typing import Union

# AutoPwnGPT File Utils

# Author: Eshan Roy
# Email: m.eshanized@gmail.com
# GitHub: https://github.com/TonmoyInfrastructureVision
# Date: 2025-04-22

def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path as string or Path object
        
    Returns:
        Path object of the directory
        
    Raises:
        OSError: If directory creation fails
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
