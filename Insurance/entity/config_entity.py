import os
import sys
from Insurance.logger import logging
from datetime import datetime
from Insurance.exception import InsuranceException

FILE_NAME="insurance.csv"
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"
TRANSFORMER_OBJECT_FILE_NAME="transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME="target_encoder.pkl"
TRANSFORMED_TRAIN_FILE_NAME="train.npz"
TRANSFORMED_TEST_FILE_NAME="test.npz"

class TrainingPipelineConfig:
    """
    This class will create training pipeline folder
    """
    def __init__(self):
        try:
            self.artifact_dir=os.path.join(os.getcwd(),'artifact',f"{datetime.now().strftime('%m%d%Y-%H%M%S')}")
        except Exception as e:
            raise InsuranceException(e,sys)
        
class DataIngestionConfig:
    """
    This will create the row file or feature store file ,train file and test file paths.

    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="INSURANCE"
            self.collection_name="INSURANCE_PROJECT"

            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,"feature_Store",FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size=0.2

        except Exception as e:
            raise InsuranceException(e,sys)
        
    #convert data to dict

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        
        except Exception as e:
            raise InsuranceException(e,sys)
        

class DataValidationConfig:
    """
    This class defines the data validation file path and report file path
    """
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_validation")
        self.report_file_path=os.path.join(self.data_validation_dir,"report.yaml")
        self.missing_threshold:float=0.2
        self.base_file_path=os.path.join("insurance.csv")


class DataTransformationConfig:
    """
    This class defines the data transformation file path and transformers file path.
    """

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir=os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transform_object_path=os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
        self.transformed_train_path=os.path.join(self.data_transformation_dir,"transformed",TRANSFORMED_TRAIN_FILE_NAME)
        self.transformed_test_path=os.path.join(self.data_transformation_dir,"transformed",TRANSFORMED_TEST_FILE_NAME)
        self.target_encoder_path=os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)






    
        
    
        



