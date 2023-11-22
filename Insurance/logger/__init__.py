import logging
from datetime import datetime
import os

#creating logs directory to store log in files.
LOG_DIR="Insurance_log"

#creating file_name for log file based on current timestamp
CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

#Here, We are going to define the path to store log with folder_name
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"

#Creating LOG_DIR if it is does not exists.
os.makedirs(LOG_DIR,exist_ok=True)

#Creating file path for project
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

#Logging basic configuration
logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="w",
                    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
                    #level=logging.INFO,
                    level=logging.DEBUG,
                    )

