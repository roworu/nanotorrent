import logging

def setup_logging():
    """Set up logging to both terminal and a log file."""
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Log to terminal
            logging.FileHandler("nanotorrent.log", mode="a")  # Log to file
        ]
    )

# Call setup_logging at the start of the program
setup_logging()
