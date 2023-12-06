from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys 
import os
from Insurance.entity import config_entity
from Insurance.componets.data_ingestion import DataIngestion
from Insurance.componets.data_validation import DataValidation
from Insurance.componets.data_transformation import DataTransformation
from Insurance.componets.model_trainer import ModelTrainer
from Insurance.componets.model_evaluation import ModelEvaluation
from Insurance.componets.model_pusher import ModelPusher


def start_training_pipeline():
    try:
        training_pipeline_config=config_entity.TrainingPipelineConfig()
        print(type(training_pipeline_config))
        #Data Ingestion
        data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_ingestion_config.to_dict())
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

        #Data Validation
        data_validation_config=config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        daata_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact=daata_validation.initiate_data_validation()


        #Data Transformation
        data_transformation_config=config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config=data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact=data_transformation.intiate_data_transformation()


        #Model Training 
        model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        #Model Evaluation
        model_evaluation_config=config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_evaluation=ModelEvaluation(model_eval_config=model_evaluation_config,
                                         data_ingestion_artifact=data_ingestion_artifact,
                                         data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_artifact=model_trainer_artifact)
        model_evaluation_artifact=model_evaluation.initiate_model_evaluation()

        #Model Pusher
        model_pusher_config=config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher=ModelPusher(model_pusher_config=model_pusher_config,
                                 data_transformation_artifact=data_transformation_artifact,
                                 model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact=model_pusher.initiate_model_pusher()

    except Exception as e:
        raise InsuranceException(e,sys)