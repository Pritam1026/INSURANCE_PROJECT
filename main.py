from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity import config_entity
from Insurance.componets.data_ingestion import DataIngestion
from Insurance.componets.data_validation import DataValidation
from Insurance.componets.data_transformation import DataTransformation


if __name__=="__main__":
    try:
        #Data Ingestion
        logging.info('data ingestion started')
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        data_ingestion_config= config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion done")



        #Data Validation
        logging.info("Data validation started")
        data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=data_validation_config,
                                       data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data validation completed")



        #Data Transformation
        logging.info("data transformation has started")
        data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
                                               data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact=data_transformation.intiate_data_transformation()
        logging.info("Data transformation completed")


    except Exception as e:
        raise InsuranceException(e,sys)
    
