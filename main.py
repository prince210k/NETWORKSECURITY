from Networksecurity.components.data_ingestion import DataIngestion
import sys
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import DataIngestionConfig
from Networksecurity.entity.config_entity import TrainingPipelineConfig
if __name__=='__main__':
    try:
        training_pipeline = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline)
        data_ingestion = DataIngestion(Data_ingestion_config=data_ingestion_config)
        logger.info("Initiate data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
    except Exception as e:
        raise NetworkSecuirtyException(e,sys)