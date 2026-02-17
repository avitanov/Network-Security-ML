from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
import sys

if __name__=="__main__":
    try:
        training_pipeline_config_obj=TrainingPipelineConfig()

        print("Initiate Data Ingestion")
        data_ingestion_config_obj=DataIngestionConfig(training_pipeline_config=training_pipeline_config_obj)
        data_ingestion_obj=DataIngestion(data_ingestion_config=data_ingestion_config_obj)
        dataIngestionArtifact=data_ingestion_obj.initiate_data_ingestion()
        print(dataIngestionArtifact)
        print("Completed Data Ingestion")

        print("Initiate Data Validation")
        data_validation_config_obj=DataValidationConfig(training_pipeline_config_obj)
        data_validation_obj=DataValidation(dataIngestionArtifact,data_validation_config_obj)
        data_validation_artifact_obj=data_validation_obj.initiate_data_validation()
        print(data_validation_artifact_obj)
        print("Completed Data Validation")

        print("Initiate Data Transformation")
        data_transformation_config_obj=DataTransformationConfig(training_pipeline_config=training_pipeline_config_obj)
        data_transformation_obj=DataTransformation(data_validation_artifact_obj,data_transformation_config_obj)
        data_transformation_artifact_obj=data_transformation_obj.initiate_data_transformation()
        print(data_transformation_artifact_obj)
        print("Completed Data Transformation")

        print("Initiate Model Trainer")
        model_trainer_config_obj=ModelTrainerConfig(training_pipeline_config=training_pipeline_config_obj)
        model_trainer_obj=ModelTrainer(data_transformation_artifact_obj,model_trainer_config_obj)
        model_trainer_artifact_obj=model_trainer_obj.initiate_model_trainer()
        print(model_trainer_artifact_obj)
        print("Completed Model Training")

    except Exception as e:
        raise CustomException(e,sys)