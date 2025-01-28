import logging
import os

    
def setup_logging(log_file=os.path.join(os.getcwd(), "Configurations", "Logs", "logs.log")):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s', 
        handlers=[
            logging.FileHandler(log_file),
        ],
    )

