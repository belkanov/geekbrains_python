import logging
from pathlib import Path

FORMATTER = logging.Formatter("%(asctime)s %(levelname)-8s %(module)s %(message)s")

LOG_DIR = Path('.') / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
