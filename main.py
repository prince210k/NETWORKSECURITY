from Networksecurity.components.data_ingestion import DataIngestion
from Networksecurity.components.data_validation import DataValidation
from Networksecurity.components.data_transformation import DataTransformation
from Networksecurity.components.model_trainer import ModelTrainer
import sys
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
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
        data_transformation_config = DataTransformationConfig(training_pipeline)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logger.info('Initiate Data Transformation')
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("Data Transformation Completed")
        print(data_transformation_artifact)
        logger.info('model training started')
        model_trainer_artifact = ModelTrainer(ModelTrainerConfig(training_pipeline),data_transformation_artifact).initiate_model_trainer()
        logger.info("Model Training completed") 
        print(model_trainer_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 