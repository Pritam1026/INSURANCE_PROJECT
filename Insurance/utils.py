import pandas as pd
import numpy as np
import os
import sys

from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        #Reading data from mongoclient
        logging.info(f"reading data from database:{database_name} and collection:{collection_name}")
        data=mongo_client[database_name][collection_name]

        #converting data to dataframe
        df=pd.DataFrame(data)
        logging.info(f"The columns the data are :{df.columns}")
        

        #removing the id column if present
        if "_id" in df.columns:
            df.drop('_id',axis=1,inplace=True)
        logging.info(f"The shape of the data is {df.shape}")


        #returning the dataframe
        return df
    

    except Exception as e:
        raise InsuranceException(e,sys)

