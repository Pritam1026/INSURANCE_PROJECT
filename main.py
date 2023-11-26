from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity import config_entity


if __name__=="__main__":
    try:
        #get_collection_as_dataframe(database_name="INSURANCE",collection_name="INSURANCE_PROJECT")
        training_pipeline_config=config_entity.TrainingPipelineConfig()
        data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
    except Exception as e:
        print(e)