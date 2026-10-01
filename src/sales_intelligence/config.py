"""Configuration settings for the application."""

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def setup_logging(cls) -> None:
        """Setup application logging."""
        numeric_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
