import os 
import sys 
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger
import pandas as pd 
import numpy as np 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from Networksecurity.entity.artifacts_entity import DataValidationArtifact,DataTransformationArtifact
from Networksecurity.entity.config_entity import DataTransformationConfig
from Networksecurity.consants.training_pipeline import TARGET_VARIABLE
from Networksecurity.consants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from Networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact 
            self.data_transformation_config:DataTransformationConfig = data_transformation_config 
            
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
        
    @staticmethod 
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
        
    def impute_missing(cls) -> Pipeline:
        try:
            ## This function initializes knn imputer with the specifed params in training_pipeline and returns an pipeline object with knn imputer
            ## ** just spreads the dictionary keys and values into named arguments.
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
            pass
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df  = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## Splitting dependent and independent featurs 
            input_feature_train_df = train_df.drop(columns=[TARGET_VARIABLE],axis=1)
            target_feature_train_df = train_df[TARGET_VARIABLE]
            input_feature_test_df = test_df.drop(columns=[TARGET_VARIABLE],axis=1)
            target_feature_test_df = test_df[TARGET_VARIABLE]
            ## Since we have two values in our target variable i.e -1 and 1
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            preprocessor = self.impute_missing()
            transformed_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_test_feature = preprocessor.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_test_feature,np.array(target_feature_test_df)]
            
            ## Save numpy array and preprocessor object 
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            
            data_transformation_artifact = DataTransformationArtifact(
             self.data_transformation_config.transformed_object_file_path,
             self.data_transformation_config.transformed_train_file_path,
             self.data_transformation_config.transformed_test_file_path   
            )
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecuirtyException(e,sys) 
