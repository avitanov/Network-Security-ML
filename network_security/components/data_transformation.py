import os
import sys

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from network_security.entity.config_entity import DataTransformationConfig
from network_security.logging.logger import logging
from network_security.exception.exception import CustomException
from network_security.utils.utils import save_object,save_numpy_array_data

class DataTransformation():

    def __init__(
        self,data_validation_artifact:DataValidationArtifact,
            data_transformation_config:DataTransformationConfig
        ):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)


    def get_data_transformer_object(self) -> Pipeline:
        logging.info("Entered the get_data_transformer_object function")
        try:
            knn:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialized KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor=Pipeline(
                [
                    ("KNNImputer",knn)
                ]
            )
            return processor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Entered initiate_data_transformation method of DataTransformation class")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
           
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            logging.info("Replacing all the -1 in the target feature with 0")
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            
            preprocessor=self.get_data_transformer_object()

            transformed_input_train_feature=preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor.transform(input_feature_test_df)

            train_arr= np.c_[ transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr= np.c_[ transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object( self.data_transformation_config.transformed_object_file_path,preprocessor)

            save_object("final_model/preprocessor.pkl",preprocessor)

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)