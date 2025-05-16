import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    """
    Sets up a logger to log scan details to /var/log/sentra_scans.log.
    Handles permission errors gracefully and rotates logs after 10MB.
    """
    log_file = "/var/log/sentra_scans.log"
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Set up the logger
        logger = logging.getLogger("sentra_logger")
        logger.setLevel(logging.INFO)

        # Create a rotating file handler
        handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    except PermissionError:
        print("Permission denied: Unable to write to /var/log/sentra_scans.log. Please run with appropriate permissions.")
        return None

def log_scan(logger, target, result):
    """
    Logs the scan details.

    Args:
        logger (logging.Logger): The logger instance.
        target (str): The target of the scan.
        result (str): The scan result.
    """
    if logger:
        summary = result[:100]  # First 100 characters of the result
        logger.info(f"Target: {target} | Result: {summary}")
