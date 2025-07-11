from Networksecurity.entity.artifacts_entity import DataIngestionArtifact, DataValidationArtifact
from Networksecurity.entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.consants.training_pipeline import SCHEMA_FILE_PATH
from Networksecurity.logging.logger import logger
import sys
import os
from scipy.stats import ks_2samp
import pandas as pd
from Networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,Data_ingestion_artifact:DataIngestionArtifact,
                 Data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = Data_ingestion_artifact
            self.data_validation_config = Data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path) 
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
        
    def validate_number_of_columns(self,df:pd.DataFrame)->bool:
        try:
            number_of_cols = len(self.schema_config['columns'])
            logger.info(f"Required :{number_of_cols}\ncurrent :{len(df.columns)}")
            if len(df.columns)==number_of_cols:
                return True
            return False
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    
    def detect_dataset_drift(self,main_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {} 
            for col in main_df.columns:
                d1 = main_df[col]
                d2 = current_df[col]
                distribution_diff = ks_2samp(d1,d2)
                if threshold<=distribution_diff.pvalue:
                    Drift_found = False
                else:
                    Drift_found = True 
                    status = False 
                report.update({
                    col:{
                        "p_value":float(distribution_diff.pvalue),
                        "Drift_status":Drift_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            ## Create Directory 
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,report)
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            ## Read the train and test Data from the DataIngestionArtifact 
            train_data_file_path = self.data_ingestion_artifact.train_file_path
            test_data_file_path = self.data_ingestion_artifact.test_file_path
            
            train_df = DataValidation.read_data(train_data_file_path)
            test_df = DataValidation.read_data(test_data_file_path)
            
            logger.info("Loaded the train and test df")
            
            ## validate number of calls
            status = self.validate_number_of_columns(train_df)
            if not status:
                error_message = f"Train df does not contains all columns \n"
            status = self.validate_number_of_columns(test_df)
            if not status:
                error_message = f"Test df does not contains all columns \n"
            
            ## Checking Data Drift
            
            status = self.detect_dataset_drift(train_df,test_df) 
            if status:
                print("No data drift detected.")
            else:
                print("Data drift detected!")
                
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifact = DataValidationArtifact(
                status,
                train_data_file_path,
                test_data_file_path,
                None,None,
                self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)