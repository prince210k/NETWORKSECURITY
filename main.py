from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
import sys
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from Networksecurity.entity.config_entity import TrainingPipelineConfig
if __name__=='__main__':
    try:
        training_pipeline = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline)
        data_ingestion = DataIngestion(Data_ingestion_config=data_ingestion_config)
        logger.info("Initiate data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logger.info("Data Initialization completed")
        
        data_validation_config = DataValidationConfig(training_pipeline)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logger.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info("Data Validation completed")
        print(data_validation_artifact) 
    except Exception as e:
        raise NetworkSecuirtyException(e,sys)