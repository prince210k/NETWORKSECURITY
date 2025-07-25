import os
import sys 
import json 
import pymongo
import certifi
import pymongo.mongo_client

ca = certifi.where()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import pandas as pd
import numpy as np 
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values()) ##This line converts a Pandas DataFrame into a list of JSON records.
            return records
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
        
    def insert_to_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
        
if __name__=='__main__':
    File_path = "network_data\phisingData.csv"
    Database = 'Prince'
    Collection = 'NetworkData'
    network = NetworkDataExtract()
    records  = network.csv_to_json(File_path)
    print(records)
    no_of_records = network.insert_to_mongo(records=records,database=Database,collection=Collection)
    print(no_of_records)