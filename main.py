from Insurance.logger import logging
from Insurance.exception import InsuranceException
import os,sys
from Insurance.utils import get_collection_as_dataframe

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
        database_name="INSURANCE"
        collection_name="INSURANCE_PROJECT"
        #test_logger_and_exception()
        get_collection_as_dataframe(database_name=database_name,collection_name=collection_name)
        
    except Exception as e:
        print(e)