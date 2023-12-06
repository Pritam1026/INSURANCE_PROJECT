from Insurance.pipeline.batch_prediction import start_batch_prediction
from Insurance.pipeline.batch_prediction import start_batch_prediction
from Insurance.pipeline.training_pipeline import start_training_pipeline

#file_path="insurance.csv"
if __name__=="__main__":
    try:
        #output=start_batch_prediction(input_file_path=file_path)
        output=start_training_pipeline()
    except Exception as e:
        print(e)