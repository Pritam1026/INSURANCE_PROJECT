from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity import config_entity
from Insurance.componets.data_ingestion import DataIngestion


if __name__=="__main__":
    try:
        #data ingestion
        logging.info('data ingestion started')
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config= config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion done")
    
    except Exception as e:
        print(e,sys)