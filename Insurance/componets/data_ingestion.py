import pandas as pd
import numpy as np
import os,sys

from Insurance.entity import config_entity
from Insurance.entity import artifact_entity
from Insurance.exception import InsuranceException
from Insurance import utils
from Insurance.logger import logging

from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise InsuranceException(e,sys)
        
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        """
        This function will read the data and save it as row data, train data ,test data
        """
        try:
            #reading the dataframe
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame=utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )

            #Replace NA value with Nan
            logging.info("replacing nan values to numpy NAN values")
            df.replace(to_replace='na',value=np.NAN,inplace=True)


            #making the feature store,train,test directory if not available
            logging.info("Creating the folders if not exists")
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            train_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(train_dir,exist_ok=True)

            test_dir=os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(test_dir,exist_ok=True)
            

            #saving the dataframe to feature store directory
            logging.info("saving the dataframe to feature store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)


            #splitting the df to training and testing files
            logging.info("splitting data into train and test dataset")
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=1)


            #saving the training and test data in the files
            logging.info("Saving the splitted data into training and test files")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #prepare artifact folder
            data_ingestion_artifact=artifact_entity.DataIngestionArtifact(
                                    feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                                    train_file_path=self.data_ingestion_config.train_file_path,
                                    test_file_path=self.data_ingestion_config.test_file_path
            )

        except Exception as e:
            raise InsuranceException(e,sys)
        
