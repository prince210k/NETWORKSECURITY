from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger
import sys 
import yaml
import dill 
import numpy as np 
import pickle 
import os 


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        NetworkSecuirtyException(e,sys)
        
def write_yaml_file(file_path: str,content: object, replace: bool = False)->None:
    try:
        if(replace):
            if os.path.exists(file_path):
                os.remove(file_path) 
        os.makedirs(os.path.dirname(file_path),exist_ok=True) 
        with open(file_path,'w') as f:
            yaml.dump(content,f) 
    except Exception as e:
        raise NetworkSecuirtyException(e,sys)
    
def save_numpy_array_data(file_path: str , array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecuirtyException(e,sys) 
                
                
def save_object(file_path: str, object: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(object,file_obj)
    except Exception as e:
        raise NetworkSecuirtyException(e,sys) 