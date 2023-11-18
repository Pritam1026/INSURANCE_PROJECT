import pymongo
import pandas as pd
import numpy as np
import json


#connection_string
uri="mongodb+srv://singhpritam382:rYCq7TiYelUQ9yYN@cluster0.hm3g8y3.mongodb.net/"

#Creating a mongodb client to interact with mongodb cloud
client=pymongo.MongoClient(uri)

#Data file path that is present in local system
data_file_path=(r"insurance.csv")

if __name__=="__main__":
    try:
        #read the dataset
        df=pd.read_csv(data_file_path)
        print(f"Rows and columns in the dataset are {df.shape}")

        #Transform the data to json.
        json_record=list(json.loads(df.T.to_json()).values())
        print(json_record[0])

        #load data to mongodb
        database_name="INSURANCE"
        collection_name="INSURANCE_PROJECT"

        insurance_database=client[database_name]
        insurance_collection=insurance_database[collection_name]

        insurance_collection.insert_many(json_record)
    
    except Exception as e:
        print(e)




