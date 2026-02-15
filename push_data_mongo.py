import os
import sys
import json

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
 
import pandas as pd
import numpy as np
import pymongo   # pyright: ignore[reportMissingImports]

from  network_security.exception.exception import CustomException
from network_security.logging.logger import logging

class NetworkDataExtract():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def cv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(
                len(self.records)
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    FILE_PATH="network_data\phisingData.csv"
    DATABASE="CYBERDATA"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    number_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(number_of_records)