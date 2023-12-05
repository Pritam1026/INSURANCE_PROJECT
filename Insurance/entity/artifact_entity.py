from dataclasses import dataclass
import os
import sys

@dataclass
class DataIngestionArtifact:
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str

@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str

@dataclass
class ModelTrainerArtifact:
    model_path:str
    train_score:float
    test_score:float


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted:bool
    improved_accuracy:float

''''
class ModelPusherArtifact:
    def __init__(self,pusher_model_dir:str,saved_model_dir:str):
        self.pusher_model_dir=pusher_model_dir
        self.saved_model_dir=saved_model_dir'''


@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str
    saved_model_dir:str