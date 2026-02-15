from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
import sys

if __name__=="__main__":
    try:
        training_pipeline_config_obj=TrainingPipelineConfig()
        data_ingestion_config_obj=DataIngestionConfig(training_pipeline_config=training_pipeline_config_obj)
        data_ingestion_obj=DataIngestion(data_ingestion_config=data_ingestion_config_obj)
        dataIngestionArtifact=data_ingestion_obj.initiate_data_ingestion()
        print(dataIngestionArtifact)
    except Exception as e:
        raise CustomException(e,sys)