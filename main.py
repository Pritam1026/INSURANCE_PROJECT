from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import get_collection_as_dataframe
import sys, os
from Insurance.entity import config_entity
from Insurance.componets.data_ingestion import DataIngestion
from Insurance.componets.data_validation import DataValidation
from Insurance.componets.data_transformation import DataTransformation
from Insurance.componets.model_trainer import ModelTrainer
from Insurance.componets.model_evaluation import ModelEvaluation
from Insurance.componets.model_pusher import ModelPusher


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

        #Model Trainer
        logging.info("Model training started")
        model_trainer_config=config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,
                                   data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model training done")

        #Model Evaluation
        logging.info("model evaluation has started")
        model_eval_config=config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval=ModelEvaluation(model_eval_config=model_eval_config,
                                   data_ingestion_artifact=data_ingestion_artifact,
                                   data_transformation_artifact=data_transformation_artifact,
                                   model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact=model_eval.initiate_model_evaluation()
        logging.info("model evaluation ends")

        #Model pusher
        logging.info("Model pusher has started")
        model_pusher_config=config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher=ModelPusher(model_pusher_config=model_pusher_config,
                                 data_transformation_artifact=data_transformation_artifact,
                                 model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact=model_pusher.initiate_model_pusher()
        logging.info("Model pusher ends")

    except Exception as e:
        raise InsuranceException(e,sys)

    
