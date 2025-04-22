#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session Manager for AutoPwnGPT.
Handles session lifecycle, state management, and persistence.
"""

import logging
import os
import time
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from ..database.db_manager import DatabaseManager
from ..config.settings import settings
from .context_manager import ContextManager
from ..utils.file_utils import ensure_directory


class Session:
    """Represents a single assessment session."""
    
    def __init__(self, 
                 name: str,
                 description: Optional[str] = None,
                 scope: Optional[List[str]] = None):
        """
        Initialize a new session.
        
        Args:
            name: Name of the session
            description: Optional description of the session
            scope: Optional list of targets/scope for the session
        """
        self.id = f"session-{int(time.time())}"
        self.name = name
        self.description = description or ""
        self.scope = scope or []
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.status = "active"


class SessionManager:
    """
    Manages security assessment sessions.
    Handles session creation, persistence, and state management.
    """
    
    def __init__(self):
        """Initialize the session manager."""
        self.logger = logging.getLogger("autopwngpt.core.session_manager")
        self.db = DatabaseManager()
        self.context_manager = ContextManager()
        self.current_session: Optional[Session] = None
        self.session_dir = Path(settings.get("application.session_directory", "data/sessions"))
        ensure_directory(self.session_dir)
        
    def create_session(self, 
                      name: str,
                      description: Optional[str] = None,
                      scope: Optional[List[str]] = None) -> Session:
        """
        Create a new security assessment session.
        
        Args:
            name: Name of the session
            description: Optional description of the session
            scope: Optional list of targets/scope for the session
            
        Returns:
            The created session object
        """
        session = Session(name=name, description=description, scope=scope)
        self.current_session = session
        
        # Create session directory
        session_path = self.session_dir / session.id
        ensure_directory(session_path)
        
        # Initialize context
        self.context_manager.reset_context()
        if scope:
            for target in scope:
                self.context_manager.add_target(target, {"address": target})
        
        # Save session metadata
        self._save_session_metadata(session)
        
        self.logger.info(f"Created new session: {session.id} - {session.name}")
        return session
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """
        Load an existing session.
        
        Args:
            session_id: ID of the session to load
            
        Returns:
            The loaded session object or None if not found
        """
        session_path = self.session_dir / session_id
        if not session_path.exists():
            self.logger.error(f"Session not found: {session_id}")
            return None
        
        # Load session metadata
        metadata_path = session_path / "metadata.json"
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                session = Session(
                    name=metadata["name"],
                    description=metadata.get("description"),
                    scope=metadata.get("scope", [])
                )
                session.id = session_id
                session.created_at = datetime.fromisoformat(metadata["created_at"])
                session.last_active = datetime.fromisoformat(metadata["last_active"])
                session.status = metadata["status"]
        except Exception as e:
            self.logger.error(f"Error loading session metadata: {str(e)}")
            return None
        
        # Load context
        context_path = session_path / "context.json"
        if not self.context_manager.load_context(str(context_path)):
            self.logger.error(f"Error loading session context for {session_id}")
            return None
        
        self.current_session = session
        self.logger.info(f"Loaded session: {session.id} - {session.name}")
        return session
    
    def save_session(self) -> bool:
        """
        Save the current session state.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.current_session:
            self.logger.error("No active session to save")
            return False
        
        try:
            session_path = self.session_dir / self.current_session.id
            ensure_directory(session_path)
            
            # Update last active timestamp
            self.current_session.last_active = datetime.now()
            
            # Save session metadata
            self._save_session_metadata(self.current_session)
            
            # Save context
            context_path = session_path / "context.json"
            if not self.context_manager.save_context(str(context_path)):
                self.logger.error("Failed to save session context")
                return False
            
            self.logger.info(f"Saved session: {self.current_session.id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving session: {str(e)}")
            return False
    
    def close_session(self) -> bool:
        """
        Close the current session.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.current_session:
            self.logger.error("No active session to close")
            return False
        
        try:
            # Save final state
            self.current_session.status = "closed"
            if not self.save_session():
                return False
            
            # Clear current session
            self.current_session = None
            self.context_manager.reset_context()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error closing session: {str(e)}")
            return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all available sessions.
        
        Returns:
            List of session metadata dictionaries
        """
        sessions = []
        try:
            for session_dir in self.session_dir.iterdir():
                if not session_dir.is_dir():
                    continue
                
                metadata_path = session_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                        sessions.append(metadata)
        
        except Exception as e:
            self.logger.error(f"Error listing sessions: {str(e)}")
        
        return sessions
    
    def get_session_findings(self) -> List[Dict[str, Any]]:
        """
        Get all findings from the current session.
        
        Returns:
            List of finding dictionaries
        """
        if not self.current_session:
            self.logger.error("No active session")
            return []
        
        return list(self.context_manager.get_findings().values())
    
    def _save_session_metadata(self, session: Session) -> None:
        """
        Save session metadata to disk.
        
        Args:
            session: The session to save metadata for
        """
        metadata = {
            "id": session.id,
            "name": session.name,
            "description": session.description,
            "scope": session.scope,
            "created_at": session.created_at.isoformat(),
            "last_active": session.last_active.isoformat(),
            "status": session.status
        }
        
        metadata_path = self.session_dir / session.id / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
