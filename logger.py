
import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create logger
logger = logging.getLogger('vuln_app_logger')
logger.setLevel(logging.INFO)

# Rotating file handler
file_handler = RotatingFileHandler('logs/app.log', maxBytes=1_000_000, backupCount=5)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers (avoid duplicates)
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
