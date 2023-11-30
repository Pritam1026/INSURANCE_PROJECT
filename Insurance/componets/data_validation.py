import os
import sys
from Insurance.entity import artifact_entity,config_entity
from Insurance.logger import logging
from Insurance.exception import InsuranceException
import pandas as pd
from typing import Optional
from scipy.stats import ks_2samp
import numpy as np
from Insurance import config
from Insurance.utils import write_yaml,convert_columns_float

class DataValidation:
    def __init__(self,
                 data_validation_config:config_entity.DataValidationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"Data validation has started")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()
        
        except Exception  as e:
            raise InsuranceException(e,sys)
        




    def drop_missing_values(self,report_key_name:str,df:pd.DataFrame)->Optional[pd.DataFrame]:
        """
        This method handles missing values in a pandas DataFrame based on a specified threshold.

        Parameters:
        - report_key_name (str): The key name for the report or validation being conducted.
        - df (pd.DataFrame): The pandas DataFrame may be containing missing values.

        Returns:
        - Optional[pd.DataFrame]: The modified DataFrame after dropping columns, or None if all columns are dropped.

        """
        try:
            #getting the columns wise missing values numbers as fraction of total missing values
            threshold=self.data_validation_config.missing_threshold
            null_report=df.isna().sum()/df.shape[0]

            #getting the list of columns with missing values greater than threshold
            drop_column_names=null_report[null_report>=threshold].index
            drop_column_list=list(drop_column_names) #converting the indexes to list
            self.validation_error[report_key_name]=drop_column_list #saving the dropped column as list

            #dropping the columns
            df.drop(drop_column_list,axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            
            return df
    
        except Exception as e:
            raise InsuranceException(e,sys)
        



    def is_required_column_exits(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:

        """
        Checks if required columns specified in the base DataFrame exist in the current DataFrame.

        Parameters:
        - base_df (pd.DataFrame): The base DataFrame containing the required columns.
        - current_df (pd.DataFrame): The current DataFrame to check for the existence of required columns.
        - report_key_name (str): The key name for the report or validation being conducted.

        Returns:
        - bool: True if all required columns exist, False otherwise.
        """

        try:
            #columns the dataframe against which it is validated.
            base_columns=base_df.columns
            #columns the dataframe which is to be validated.
            current_columns=current_df.columns

            #list of missing columns
            missing_column=[]


            #finding the missing columns
            for columns in base_columns:
                if columns not in current_columns:
                    logging.info(f"{columns} doesnot exists in base_df")
                    missing_column.append(columns)

            
            #If there is missing column return False
            if len(missing_column)>0:
                self.validation_error[report_key_name]=missing_column
                return False
            #if there is not any missing column return True
            return True
        
        except Exception as e:
            raise InsuranceException(e,sys)
        

    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        """
        Checks if the base datframe and current dataframe the column distributions matches exactly.
        This function uses the Kolmogorov-Smirnov two-sample test.

        Parameters:
        - base_df (pd.DataFrame): The base DataFrame containing the required columns.
        - current_df (pd.DataFrame): The current DataFrame to check for the drift of required columns.
        - report_key_name (str): The key name for the report or drift being conducted.
        """

        try:
            #creating a dictonary for saving the test reports
            drift_report={}
            #original dataframe
            base_columns=base_df.columns
            #New dataframe
            current_columns=current_df.columns

            #looping over the current df's columns and base df's columns and test the KS test to confirm that
            # there is no data drift and both the data comes from the same distribution
            for base_column in base_columns:
                base_data=base_df[base_column]
                current_data=current_df[base_column]
                same_distribution=ks_2samp(base_data,current_data)
                
                #if p_value less than 0..05 then diffrenece between the data is not significant that means
                #they come from same distribution
                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        "p_values":float(same_distribution.pvalue),
                        "same_distribution":True
                    }
                else:
                    drift_report[base_column]={
                        "p_values":float(same_distribution.pvalue),
                        "same_distribution":False
                    }

            #saving the report in validation_error with a report_key_name
            self.validation_error[report_key_name]=drift_report


        except Exception as e:
            raise InsuranceException(e,sys)
        


    def initiate_data_validation(self)->artifact_entity.DataIngestionArtifact:

        try:
            #Reading the base dataframe
            logging.info("Reading the base dataframe")
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({'na':np.NaN},inplace=True)
            logging.info("Replacing na values in the base df")


            #reading the training and test dataset
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)


            #Dropping the missing values from the base,train,test Dataframes.
            base_df=self.drop_missing_values(report_key_name="missing_values_in_base_dataset",df=base_df)
            train_df=self.drop_missing_values(report_key_name="missing_values_in_base_dataset",df=train_df)
            test_df=self.drop_missing_values(report_key_name="missing_values_in_base_dataset",df=test_df)


            #Columns to be excluded from float type conversion
            exclude_column_list=[config.TARGET_COLUMN]
            #converting the numerical columns to the float values in the dataframe
            base_df=convert_columns_float(df=base_df,exclude_column=exclude_column_list)
            train_df=convert_columns_float(df=train_df,exclude_column=exclude_column_list)
            test_df=convert_columns_float(df=test_df,exclude_column=exclude_column_list)


            #checkiong if required column exists in the dataframe
            logging.info("is all columns exists in train dataset")
            train_df_column_status=self.is_required_column_exits(base_df=base_df,
                                                                 current_df=train_df,
                                                                 report_key_name="Missing_column_within_train_dataset")
            logging.info("is all columns exists in test dataset")
            test_df_column_status=self.is_required_column_exits(base_df=base_df,
                                                                 current_df=train_df,
                                                                 report_key_name="Missing_column_within_train_dataset")
            

            #If there is no missing values then we will proceed to find the data drift in the train dataframe.
            if train_df_column_status:
                logging.info("All columns exists in the train data hence checking the data drift")
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_within_train_dataset")

            #If there is no missing values then we will proceed to find the data drift in the train dataframe.
            if test_df_column_status:
                logging.info("All columns exists in the test data hence checking the data drift")
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="data_drift_within_test_dataset")


            # Write report in YAML file.
            write_yaml(file_path=self.data_validation_config.report_file_path,data=self.validation_error)
            
            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=
                                                                            self.data_validation_config.report_file_path)
            
            return data_validation_artifact
        
            logging.info(f"Data validation artifact :{data_validation_artifact}")

        except Exception as e:
            raise InsuranceException(e,sys)
    
    