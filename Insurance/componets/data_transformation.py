import os
import sys
import numpy as np
import pandas as pd
from Insurance.entity import config_entity
from Insurance.entity import artifact_entity
from Insurance.exception import InsuranceException
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from Insurance.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from Insurance import utils
from Insurance.logger import logging





class DataTransformation:

    def __init__(self,
                 data_transformation_config:config_entity.DataTransformationConfig,
                 data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys)
        
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer=SimpleImputer(strategy='constant',fill_value=0)
            Robust_scaler=RobustScaler()
            pipeline=Pipeline([('rmputer',simple_imputer),
                               ('robust_scaler',Robust_scaler)])
            
            return pipeline

        except Exception as e:
            raise InsuranceException(e,sys)
        
    def intiate_data_transformation(self)->artifact_entity.DataTransformationArtifact:
        try:
            #Raeding the training and test dataset
            logging.info("Reading the training and test csv")
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #Creating the input features dataset for train and test df
            target_column=TARGET_COLUMN
            logging.info(f"Target column is defined as {target_column}")
            input_feature_train_df=train_df.drop(target_column,axis=1)
            input_feature_test_df=test_df.drop(target_column,axis=1)

            #creating the output features in train and test dataset
            logging.info("creating the target train and test array")
            target_feature_train_df=train_df[target_column]
            target_feature_test_df=test_df[target_column]
            
            #Label encoder instance
            label_encoder=LabelEncoder()

            #Converting the training and test array in the series format.
            target_feature_train_arr=target_feature_train_df.squeeze()
            target_feature_test_arr=target_feature_test_df.squeeze()


            #Encoding the categorical columns with label encoding.
            logging.info("Encoding the labels of the categorical coliumns")
            for column in input_feature_train_df.columns:
                if input_feature_train_df[column].dtype=='O':
                    input_feature_train_df[column]=label_encoder.fit_transform(input_feature_train_df[column])
                    input_feature_test_df[column]=label_encoder.transform(input_feature_test_df[column])

                else:
                    input_feature_train_df[column]=input_feature_train_df[column]
                    input_feature_train_df[column]=input_feature_train_df[column]

            logging.debug(f"{input_feature_train_df.head()}")
            logging.info("transforming the input features")
            transformation_pipeline=DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            input_feature_train_arr=transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr=transformation_pipeline.transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr=np.c_[input_feature_test_arr,target_feature_test_arr]

            logging.info('Saving the training,test,transformation_pipeline object label_encoder')
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array=test_arr)
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,obj=label_encoder)

            #data transformation artifact
            logging.info("creating the data transformation artifact")
            data_transformation_artifact=artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path=self.data_transformation_config.transformed_train_path,
                transformed_test_path=self.data_transformation_config.transformed_test_path,
                target_encoder_path=self.data_transformation_config.target_encoder_path
            )

            return data_transformation_artifact

            
        except Exception as e:
            raise InsuranceException(e,sys)
    

