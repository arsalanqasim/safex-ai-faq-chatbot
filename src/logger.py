# ==============================================================================
# SafeX AI Knowledge Assistant - Application Logger
# ==============================================================================
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "safex_rag", log_level: str = "INFO", log_file: str = "safex_rag.log") -> logging.Logger:
    """
    Configures and returns a rotating logger that prints to console and a file.
    
    Args:
        name (str): Name of the logger.
        log_level (str): String logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file (str): Filepath where logs should be saved.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # If logger is already configured, return it to prevent adding duplicate handlers
    if logger.handlers:
        return logger
        
    # Convert string log level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Formatter for log entries
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 1. Console Handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. File Handler (with rotating files to manage disk space)
    try:
        # Resolve log file path relative to execution directory
        log_dir = os.path.dirname(os.path.abspath(log_file))
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024,  # 5MB per log file
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"WARNING: Could not create file logger at {log_file} due to: {e}. Logging to console only.")
        
    return logger

# Create a default package-level logger
logger = setup_logger()
