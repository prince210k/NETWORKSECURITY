import os 
import sys 
import numpy as np 
import pandas as pd

'''
Common constant variables for training pipeline

'''
TARGET_VARIABLE = "Result"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "NetworkData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

''' 
Data ingestion ingestion related constants 

'''

DATA_INGESTION_COLLECTION_NAME:str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME:str = 'Prince'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2 