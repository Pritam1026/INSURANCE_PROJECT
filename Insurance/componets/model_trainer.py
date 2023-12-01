from Insurance.entity import config_entity,artifact_entity
import os
import sys
import pandas 
import numpy
from Insurance.exception import InsuranceException
from Insurance.entity import config_entity,artifact_entity
from sklearn.linear_model import LinearRegression
from Insurance import utils
from Insurance.logger import logging
from sklearn.metrics import r2_score

class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):#Model trainer config will give the file
        #paths and variables while data transformation artifact will give the transformed dataset.
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)
        
    def train_model(self,X,y):
        try:
            #We are trying only linear model here
            lr=LinearRegression()
            lr.fit(X=X,y=y)
            logging.info("Linear model returned.")
            return lr
        except Exception as e:
            raise InsuranceException(e,sys)
        
    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info("Loading the train and test df")
            #loading the train and test data
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            logging.info(f"{type(train_arr)}")

            #Splitting the data into train and test array
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            #Model training
            logging.info(f"Model training sarted")
            model=self.train_model(X=x_train,y=y_train)
            yhat_train=model.predict(x_train)
            yhat_test=model.predict(x_test)

            #train and test scores
            train_score=r2_score(y_true=y_train,y_pred=yhat_train)
            test_score=r2_score(y_true=y_test,y_pred=yhat_test)

            logging.info("Comparing the test score with expected values")
            if test_score<self.model_trainer_config.expected_accuracy:
                raise Exception(f"Model accuracy:{test_score} is less than expected accuracy\
                                :{self.model_trainer_config.expected_accuracy}")
            
            diff=abs(train_score-test_score)
            logging.info("Checking if the model overfitting or not")

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model score difference is :{diff} but the threshold values is\
                                :{self.model_trainer_config.overfitting_threshold}")
            
            logging.info("saving the model")

            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)

            #Model trainer artifact
            model_trainer_artifact=artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                train_score=train_score,
                test_score=test_score
            )

            return model_trainer_artifact









            





        except Exception as e:
            raise InsuranceException(e,sys)

        


