#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Local LLM Provider for AutoPwnGPT.
Provides integration with local LLM models for offline operation.
"""

import aiohttp
import json
import logging
import os
from typing import Any, Dict, List, Optional


class LocalLlmProvider:
    """
    Provider for local LLM models.
    Currently supports Ollama API.
    """
    
    def __init__(self, host: str = "localhost", port: int = 11434, model: str = "llama3"):
        """
        Initialize the local LLM provider.
        
        Args:
            host: Host where the local LLM server is running.
            port: Port the local LLM server is listening on.
            model: Model to use for generation.
        """
        self.logger = logging.getLogger("autopwngpt.llm_integration.local_llm")
        self.host = host
        self.port = port
        self.model = model
        self.api_base_url = f"http://{host}:{port}"
        
        self.logger.info(f"Initialized local LLM provider with model {model} at {self.api_base_url}")
    
    async def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 2048) -> str:
        """
        Generate a response from the local LLM.
        
        Args:
            prompt: The prompt to send to the model.
            temperature: The temperature for generation.
            max_tokens: The maximum number of tokens to generate.
            
        Returns:
            The generated response.
        """
        # Check if Ollama is running
        if not await self._is_ollama_running():
            self.logger.error("Ollama is not running or not accessible")
            return "ERROR: Local LLM service (Ollama) is not running or not accessible."
        
        # Check if the model is available
        if not await self._is_model_available():
            self.logger.error(f"Model {self.model} is not available in Ollama")
            return f"ERROR: Model {self.model} is not available in the local LLM service."
        
        try:
            # Set up payload for Ollama
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            # Send request to Ollama
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"Ollama API error ({response.status}): {error_text}")
                        return f"ERROR: Local LLM API returned status {response.status}."
                    
                    response_data = await response.json()
                    
                    if "response" in response_data:
                        return response_data["response"]
                    else:
                        self.logger.error(f"Unexpected response format from Ollama API: {response_data}")
                        return "ERROR: Unexpected response format from local LLM API."
        
        except Exception as e:
            self.logger.exception(f"Error generating local LLM response: {str(e)}")
            return f"ERROR: Failed to generate response from local LLM: {str(e)}"
    
    async def _is_ollama_running(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            True if Ollama is running, False otherwise.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/api/version") as response:
                    return response.status == 200
        except Exception:
            return False
    
    async def _is_model_available(self) -> bool:
        """
        Check if the specified model is available in Ollama.
        
        Returns:
            True if the model is available, False otherwise.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = [model["name"] for model in data.get("models", [])]
                        return self.model in models
                    return False
        except Exception:
            return False
    
    async def list_available_models(self) -> List[str]:
        """
        List all available models in the local LLM service.
        
        Returns:
            A list of available model names.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [model["name"] for model in data.get("models", [])]
                    return []
        except Exception as e:
            self.logger.error(f"Error listing models: {str(e)}")
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from the Ollama library.
        
        Args:
            model_name: The name of the model to pull.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            payload = {"name": model_name}
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/api/pull",
                    json=payload
                ) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.error(f"Error pulling model {model_name}: {str(e)}")
            return False
