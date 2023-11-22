from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os,sys

def test_logger_and_exception():
    try:
        logging.info('Starting the test logger and exception')
        result=3/0
        logging.info('Ending point of test_logger and exception')
        
    except Exception as e:
        print(e)
        logging.debug(str(e))
        raise InsuranceException(e,sys)
    

if __name__=="__main__":
    try:
        test_logger_and_exception()
        
    except Exception as e:
        print(e)