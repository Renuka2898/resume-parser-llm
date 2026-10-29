"""Application logging setup."""
import logging
import os

def configure_logging() -> None:
    """Configure consistent logs without logging resume contents."""
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"),
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
