import os
import sys

from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.entity.config_entity import DataIngestionConfig 
from network_security.entity.artifact_entity import DataIngestionArtifact

import numpy as np
import pandas as pd
import pymongo
from typing import List
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            ##re ading the data from MongoDB
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            df=self.export_collection_as_dataframe()
            df=self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            dataIngestionArtifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
                )
            return dataIngestionArtifact
        except Exception as e:
            raise CustomException(e,sys)

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the DataFrame")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting train and test file path.")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )

        except Exception as e:
            raise CustomException(e,sys)

