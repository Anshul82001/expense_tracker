import logging

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/expense_tracker.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)

logger = get_logger(__name__)