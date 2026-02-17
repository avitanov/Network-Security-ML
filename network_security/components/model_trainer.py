import os
import sys
from tabnanny import verbose

import numpy as np
import pandas as pd

from network_security.entity.artifact_entity import DataTransformationArtifact,ClassificationMetricArtifact,ModelTrainerArtifact
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.logging.logger import logging
from network_security.exception.exception import CustomException
from network_security.utils.utils import save_object,load_object,load_numpy_array_data
from network_security.utils.ml_utils import evaluate_models, get_classification_score
from network_security.utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)

class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact:DataTransformationArtifact,
            model_trainer_config:ModelTrainerConfig
        ):
        try:
            self.model_trainer_config:ModelTrainerConfig=model_trainer_config
            self.data_transformation_artifact:DataTransformationArtifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def train_model(self,X_train,y_train,X_test,y_test):
        models= {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Logistic Regression": LogisticRegression(verbose=1),
            "KNNClasifier": KNeighborsClassifier()
        }
        param_grid = {
            "Random Forest": {
                "n_estimators": [200, 500],
                "max_depth": [None, 20],
                "min_samples_split": [2, 5],
            },
            "Gradient Boosting": {
                "n_estimators": [100, 200],
                "learning_rate": [0.05, 0.1],
                "max_depth": [3, 5],
            },
            "Decision Tree": {
                "max_depth": [None, 10],
                "min_samples_split": [2, 5],
                "criterion": ["gini", "entropy"],
            },
            "Logistic Regression": {
                "C": [0.1, 1.0, 10.0],
                "solver": ["lbfgs"],
                "max_iter": [500],
            },
            "KNNClasifier": {
                "n_neighbors": [3, 7, 11],
                "weights": ["uniform", "distance"],
            },
        }
        model_report:dict=evaluate_models(
            X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,params=param_grid)
        

        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model=models[best_model_name]


        y_train_pred=best_model.predict(X_train)
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        y_test_pred=best_model.predict(X_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

        preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=network_model)

        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)