import logging

def setup_logger():
    logger = logging.getLogger("Daisy")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Avoid duplicate logs
    if not logger.handlers:
        # Console handler (for terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # File handler (logs will be written to app.log)
        file_handler = logging.FileHandler("app.log", mode="a")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
