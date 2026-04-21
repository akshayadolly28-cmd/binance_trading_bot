import logging
import os
from datetime import datetime

def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = datetime.now().strftime("bot_%Y-%m-%d.log")
    log_filepath = os.path.join(log_dir, log_filename)

    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)

    # File Handler
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Console Handler (Optional, using Click for console output instead mostly, but good for critical errors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
