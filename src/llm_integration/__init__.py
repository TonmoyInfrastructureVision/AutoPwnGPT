#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AutoPwnGPT LLM Integration Package.
Contains functionality for integrating with language models.
"""

from src.llm_integration.llm_manager import LlmManager
from src.llm_integration.local_llm import LocalLlmProvider

__all__ = [
    "LlmManager",
    "LocalLlmProvider"
]
