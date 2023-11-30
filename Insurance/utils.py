import pandas as pd
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.config import mongo_client
import os,sys
import numpy as np
import yaml
import dill

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise InsuranceException(e, sys)
    

def convert_columns_float(df:pd.DataFrame,exclude_column:list)->pd.DataFrame:
    """
    Description:This function will convert the numerical columns of the datframe to float.
    =========================================================
    params:
    df(pd.DataFrame):Dataframe whose column we want to convert
    exclude_column(list): The list of columns that we donot want to convert.
    =========================================================
    return:pandas dataframe with converted columns.

    """
    try:
        for column in df.columns:
            if column not in exclude_column:
                if df[column].dtype!='O':
                    df[column]=df[column].astype(float)
        
        return df
    
    except Exception as e:
        raise InsuranceException(e,sys)
    

def write_yaml(file_path:str,data:dict):
    """
    Description:This function return the yaml format report that is present in the dictionary
    =========================================================
    params:
    file_path(str):file path of the report where it is to be dumped
    data(dict):Data in dict format.
    =========================================================
    """
    try:
        #file path where report is to be saved
        report_file_dir=os.path.dirname(file_path)
        #MAking a directory where file is present
        os.makedirs(report_file_dir,exist_ok=True)
        #Dumping the file
        with open(file_path, "w") as file_obj:
            yaml.dump(data,file_obj)

    except Exception as e:
        raise InsuranceException(e,sys)
    
def save_object(file_path:str,obj:object)->None:
    """saves the object in binary format"""
    try:
        obj_dir=os.path.dirname(file_path)
        os.makedirs(obj_dir,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise InsuranceException(e,sys)
    
def load_object(file_path:str)->object:
    """Loads the binary object"""
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file :{file_path} is not exists")
        
        with open(file_path,"rb") as file_object:
            return dill.load(file_object)

    except Exception as e:
        raise InsuranceException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.savez(file_path,array)

    except Exception as e:
        raise InsuranceException(e,sys)


        