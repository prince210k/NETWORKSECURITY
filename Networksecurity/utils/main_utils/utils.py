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
    