import logging

# Create the main application logger
logger = logging.getLogger("backend")

# Set the minimum log level
logger.setLevel(logging.INFO)

# Prevent duplicate logs when the server reloads
logger.propagate = False

# Create the format used for every log message
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a handler that prints logs to the terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Create a handler that writes logs to app.log
file_handler = logging.FileHandler(
    "app.log",
    mode="a"
)
file_handler.setFormatter(formatter)

# Add handlers only if they haven't already been added
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)