import os,sys
import numpy as np
import pandas as pd
from Insurance.logger import logging
from Insurance.exception import InsuranceException
from Insurance.utils import load_object
from datetime import datetime
from Insurance.predictor import ModelResolver
from datetime import datetime

PREDICTION_DIR="prediction"

def start_batch_prediction(input_file_path):
    #Reading the file
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info("creating model resolver object")
        model_resolver=ModelResolver(model_registry="saved_models")
        logging.info(f"Reading the input:{input_file_path}")
        df=pd.read_csv(input_file_path)
        df.replace({"na":np.NaN},inplace=True)

        #data preparation
        logging.info("Loading transformer to transform dataset")
        transformer=load_object(file_path=model_resolver.get_latest_transformer_path())

        logging.info("Target encoder to convert categorical column ")
        target_encoder=load_object(file_path=model_resolver.get_latest_target_encoder_path())

        input_feature_name=list(transformer.feature_names_in_)
        for i in input_feature_name:
            if df[i].dtypes=="O":
                df[i]=target_encoder.fit_transform(df[i])


        input_arr=transformer.transform(df[input_feature_name])
        logging.info("Loading model to make prediction")


        model=load_object(file_path=model_resolver.get_latest_model_path())
        predict=model.predict(input_arr)

        df["prediction"]=predict

        predict_file_name=os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path=os.path.join(PREDICTION_DIR,predict_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return predict_file_name
    
    except Exception as e:
        raise InsuranceException(e,sys)



