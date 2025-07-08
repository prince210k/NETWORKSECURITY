from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger

## Configuration of the data ingestion
from Networksecurity.entity.config_entity import DataIngestionConfig
from Networksecurity.entity.artifacts_entity import DataIngestionArtifact
import os 
import sys 
import pymongo
import pandas as pd  
import numpy as np
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv('MONGO_DB_URL')

class DataIngestion():
    def __init__(self,Data_ingestion_config:DataIngestionConfig):
        try:
            self.database_ingestion_config = Data_ingestion_config
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
        
    def export_collection_as_df(self):
        """
        TO Read Data from mongoDB client
        and when we read it from  mongoDB a column named _id gets added so remove it
        
        """
        try:
            database_name = self.database_ingestion_config.database_name
            collection_name = self.database_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            logger.info("Initialized the mongo client object")
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=['_id'],axis=1)
            
            df.replace({"na":np.nan})
            logger.info("Read data from client and converted to df")
            return df
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    
    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.database_ingestion_config.feature_store_file_path
            ## Creating folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logger.info("Created feature store dir")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
        
    def train_test_split(self,dataframe : pd.DataFrame):
        try:
            train_set,test_set = train_test_split(
                dataframe,test_size=self.database_ingestion_config.train_test_split_ratio
                )
            logger.info(" Train test Split performed")
            dir_name = os.path.dirname(self.database_ingestion_config.train_file_path)
            os.makedirs(dir_name,exist_ok=True)
            logger.info("Train Test Split dir created")
            train_set.to_csv(self.database_ingestion_config.train_file_path,index=False,header=True)
            test_set.to_csv(self.database_ingestion_config.test_file_path,index=False,header=True)
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
            
            
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_df()
            logger.info("Data Exportation from mongoDB completed")
            dataframe = self.export_data_to_feature_store(dataframe)
            logger.info("Converted the dataframe to a raw csv file and stored in feature store")
            self.train_test_split(dataframe=dataframe)
            logger.info("Exported train test split file path")
            Dataingestionartifact = DataIngestionArtifact(
                self.database_ingestion_config.train_file_path,self.database_ingestion_config.test_file_path
            )
            return Dataingestionartifact
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    