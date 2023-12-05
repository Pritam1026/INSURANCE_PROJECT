from Insurance.entity import artifact_entity,config_entity
from Insurance.exception import InsuranceException
from Insurance.logger import logging
from typing import Optional
import os,sys
from sklearn.pipeline import Pipeline
import pandas as pd
from Insurance import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from Insurance.predictor import ModelResolver
from Insurance.config import TARGET_COLUMN


class ModelEvaluation:
    def __init__(self,model_eval_config:config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver=ModelResolver()
        except Exception as e:
            raise InsuranceException(e,sys)
        
    def initiate_model_evaluation(self):
        try:
            latest_dir_path=self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=None)
                logging.info(f"Model evaluation artifact:{model_eval_artifact}")
                return model_eval_artifact
        
            #Find loaction of objects of previous model/Paths
            logging.info("Loading the path of previous objects ")
            prev_transformer_path=self.model_resolver.get_latest_transformer_path()
            prev_model_path=self.model_resolver.get_latest_model_path()
            prev_target_encoder_path=self.model_resolver.get_latest_target_encoder_path()

            #Previous model objects
            logging.info("Loading previous model object")
            prev_transformer=utils.load_object(file_path=prev_transformer_path)
            prev_model=utils.load_object(file_path=prev_model_path)
            prev_target_encoder=utils.load_object(file_path=prev_target_encoder_path)




            #Location of new models objects
            logging.info("Loading the path of new model object")
            current_transformer_path=self.data_transformation_artifact.transform_object_path
            current_model_path=self.model_trainer_artifact.model_path
            current_target_encoder_path=self.data_transformation_artifact.target_encoder_path

            #current model object
            logging.info("Loading new model objects")
            current_transformer=utils.load_object(file_path=current_transformer_path)
            current_model=utils.load_object(file_path=current_model_path)
            current_target_encoder=utils.load_object(file_path=current_target_encoder_path)


            #loading the new data
            logging.info("Loading new data")
            test_file_path=self.data_ingestion_artifact.test_file_path
            test_df=pd.read_csv(test_file_path)
            target_df=test_df[TARGET_COLUMN]
            y_true=target_df

            #Processing and evaluation of previous model score
            logging.info("calculating previous model score")
            input_feature_names=list(prev_transformer.feature_names_in_)
            for i in input_feature_names:
                if test_df[i].dtypes=='O':
                    test_df[i]=prev_target_encoder.transform(test_df[i])
            input_arr=prev_transformer.transform(test_df[input_feature_names])
            y_pred=prev_model.predict(input_arr)
            prev_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Previous model score is {prev_model_score}")

            #Processing and evaluation of new model score
            logging.info("calculating the current model score")
            input_feature_names=list(current_transformer.feature_names_in_)
            for i in input_feature_names:
                if test_df[i].dtypes=='O':
                    test_df[i]=current_target_encoder.transform(test_df[i])
            input_arr=current_transformer.transform(test_df[input_feature_names])
            y_pred=current_model.predict(input_arr)
            current_model_score=r2_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"current model score is {current_model_score}")

            #Final comparison between two models
            if current_model_score<=prev_model_score:
                logging.info("Current model is not better than previous model")
                raise Exception("current model is not better than previous model")
            
            improved_accuracy=current_model_score-prev_model_score
            model_eval_artifact=artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,improved_accuracy=improved_accuracy)
            logging.info("Returning model_eval_artifact")
            return model_eval_artifact
    
        except Exception as e:
            raise InsuranceException(e,sys)
        


        
