import logging
import sys

# Define a standard log format
LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] "
    "[%(name)s.%(funcName)s:%(lineno)d] - %(message)s"
)

# Create a root logger for the entire app
logging.basicConfig(
    level=logging.INFO,  # You can set to DEBUG for more verbosity
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)  # Logs to console
    ]
)

# Optional: you can define a logger for specific parts of the app
logger = logging.getLogger("crypto_app")
