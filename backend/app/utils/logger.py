"""Logging configuration for the application"""
import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Set up a logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Optional log file path. If None, uses default location
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler - write to log file
    if log_file:
        log_path = logs_dir / log_file
    else:
        # Default: use service name with date
        log_path = logs_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_ai_logger(service_name: str) -> logging.Logger:
    """
    Get a logger specifically for AI service results
    
    Args:
        service_name: Name of the AI service (e.g., 'whisper', 'groq')
    
    Returns:
        Configured logger for AI results
    """
    log_file = f"ai_{service_name}_{datetime.now().strftime('%Y%m%d')}.log"
    return setup_logger(f"ai.{service_name}", log_file)

