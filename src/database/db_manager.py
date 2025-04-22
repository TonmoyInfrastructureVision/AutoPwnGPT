#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Manager for AutoPwnGPT.
Handles database connections and operations.
"""

import sqlite3
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path


class DatabaseManager:
    """Manages database operations for the application."""
    
    def __init__(self, db_path: str = "data/autopwngpt.db"):
        """Initialize database manager."""
        self.logger = logging.getLogger("autopwngpt.database.db_manager")
        self.db_path = db_path
        
        # Ensure database directory exists
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self.init_db()
    
    def init_db(self) -> None:
        """Initialize the database schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create necessary tables
                cursor.executescript("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP NOT NULL,
                        last_active TIMESTAMP NOT NULL,
                        status TEXT NOT NULL
                    );
                    
                    CREATE TABLE IF NOT EXISTS findings (
                        id TEXT PRIMARY KEY,
                        session_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        severity TEXT NOT NULL,
                        created_at TIMESTAMP NOT NULL,
                        FOREIGN KEY (session_id) REFERENCES sessions(id)
                    );
                """)
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            raise

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
