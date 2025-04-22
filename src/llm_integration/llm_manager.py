#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM Manager for AutoPwnGPT.
Manages interactions with language models.
"""

import asyncio
import logging
import os
import aiohttp
import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from src.llm_integration.local_llm import LocalLlmProvider


class LlmManager:
    """
    Manages interactions with language models.
    Supports both OpenAI API and local LLM providers.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM manager.
        
        Args:
            config: Configuration dictionary.
        """
        self.logger = logging.getLogger("autopwngpt.llm_integration.llm_manager")
        self.config = config
        self.llm_config = config.get("llm", {})
        
        # Get the provider from config (default: openai)
        self.provider = self.llm_config.get("provider", "openai")
        
        # Load API key from environment or config
        if self.provider == "openai":
            self.api_key = os.environ.get("OPENAI_API_KEY") or self.llm_config.get("api_key", "")
            if not self.api_key:
                self.logger.warning("No OpenAI API key found. LLM functionality will be limited.")
            
            self.model = self.llm_config.get("model", "gpt-4-0125-preview")
            self.temperature = self.llm_config.get("temperature", 0.1)
            self.max_tokens = self.llm_config.get("max_tokens", 4096)
        
        # Initialize local LLM if configured
        elif self.provider == "local":
            local_config = self.llm_config.get("local", {})
            self.local_provider = LocalLlmProvider(
                host=local_config.get("host", "localhost"),
                port=local_config.get("port", 11434),
                model=local_config.get("model", "llama3")
            )
            self.logger.info(f"Using local LLM provider with model: {local_config.get('model', 'llama3')}")
        
        else:
            self.logger.error(f"Unsupported LLM provider: {self.provider}")
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
        
        self.logger.info(f"Initialized LLM manager with provider: {self.provider}")
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the language model.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            The generated response.
        """
        if self.provider == "openai":
            return await self._generate_openai_response(prompt)
        elif self.provider == "local":
            return await self._generate_local_response(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def _generate_openai_response(self, prompt: str) -> str:
        """
        Generate a response using the OpenAI API.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            The generated response.
        """
        if not self.api_key:
            self.logger.error("Cannot generate response: No OpenAI API key")
            return "ERROR: No OpenAI API key configured."
        
        try:
            # Prepare the request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an AI assistant for a penetration testing tool. Provide concise, accurate information about security topics."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            # Send the request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"OpenAI API error ({response.status}): {error_text}")
                        return f"ERROR: OpenAI API returned status {response.status}."
                    
                    # Parse the response
                    response_data = await response.json()
                    
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        return response_data["choices"][0]["message"]["content"]
                    else:
                        self.logger.error(f"Unexpected response format from OpenAI API: {response_data}")
                        return "ERROR: Unexpected response format from OpenAI API."
        
        except Exception as e:
            self.logger.exception(f"Error generating OpenAI response: {str(e)}")
            return f"ERROR: Failed to generate response: {str(e)}"
    
    async def _generate_local_response(self, prompt: str) -> str:
        """
        Generate a response using a local LLM provider.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            The generated response.
        """
        try:
            return await self.local_provider.generate(prompt)
        except Exception as e:
            self.logger.exception(f"Error generating local LLM response: {str(e)}")
            return f"ERROR: Failed to generate response from local LLM: {str(e)}"
    
    async def generate_chain_of_thought(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a chain-of-thought reasoning response.
        
        Args:
            question: The question to reason about.
            context: Additional context for the question.
            
        Returns:
            A dictionary containing the reasoning steps and final answer.
        """
        # Build the prompt for chain-of-thought reasoning
        prompt = """I need you to solve a security problem step by step, showing your reasoning.

Question: {question}

Please think through this carefully:
1. What are the key facts and constraints?
2. What approaches could solve this problem?
3. What are the tradeoffs of each approach?
4. What is the best approach and why?
5. What is the final solution?

Respond with a JSON object containing:
- "reasoning": an array of reasoning steps
- "solution": the final solution
- "confidence": a number from 0 to 1 indicating confidence
"""
        
        # Add context if provided
        if context:
            context_str = "\nAdditional context:\n"
            for key, value in context.items():
                if isinstance(value, dict):
                    context_str += f"- {key}: {json.dumps(value, sort_keys=True)}\n"
                else:
                    context_str += f"- {key}: {value}\n"
            prompt = prompt.replace("{question}", f"{question}\n{context_str}")
        else:
            prompt = prompt.replace("{question}", question)
        
        # Generate response
        response = await self.generate_response(prompt)
        
        # Parse the response
        try:
            # Extract JSON from the response
            json_match = json.loads(response)
            return json_match
        except Exception as e:
            self.logger.error(f"Failed to parse chain-of-thought response: {str(e)}")
            return {
                "reasoning": ["Error parsing response"],
                "solution": "Failed to generate a valid response",
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def check_command_safety(self, command: str) -> Tuple[bool, str]:
        """
        Check if a command is safe to execute.
        
        Args:
            command: The command to check.
            
        Returns:
            A tuple of (is_safe, reason).
        """
        # Build the safety check prompt
        prompt = f"""Evaluate whether this command is safe to execute in a pen testing context:

Command: {command}

Consider:
1. Could this command cause unintended damage?
2. Is this command targeting systems in scope?
3. Could this command affect availability?
4. Is this command appropriate for a security assessment?

Respond with a JSON object:
{{
  "is_safe": true/false,
  "reason": "explanation of safety determination",
  "suggested_alternative": "safer alternative if applicable" (optional)
}}
"""
        
        # Generate and parse response
        try:
            response = await self.generate_response(prompt)
            
            # Extract JSON
            import re
            json_match = re.search(r'({.*})', response, re.DOTALL)
            if json_match:
                safety_data = json.loads(json_match.group(1))
                return (
                    safety_data.get("is_safe", False),
                    safety_data.get("reason", "Unknown reason") +
                    (f"\nSuggested alternative: {safety_data['suggested_alternative']}" 
                     if "suggested_alternative" in safety_data else "")
                )
            else:
                return False, "Could not parse safety check response"
                
        except Exception as e:
            self.logger.error(f"Error in safety check: {str(e)}")
            return False, f"Safety check failed: {str(e)}"
