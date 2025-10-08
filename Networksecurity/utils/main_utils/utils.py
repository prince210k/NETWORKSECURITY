from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
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
        NetworkSecurityException(e,sys)
        
def write_yaml_file(file_path: str,content: object, replace: bool = False)->None:
    try:
        if(replace):
            if os.path.exists(file_path):
                os.remove(file_path) 
        os.makedirs(os.path.dirname(file_path),exist_ok=True) 
        with open(file_path,'w') as f:
            yaml.dump(content,f) 
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path: str , array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    
def load_numpy_array(file_path: str) -> np.array:
    try:
        with open(file_path,'rb') as obj:
            return np.load(obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path: str, object: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(object,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) 

def load_object(file_path: str,):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file :{file_path} is invalid")
        else:
            with open(file_path,'rb') as file_obj:
                print(file_obj)
                return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        best_score = float('-inf')
        best_model = None

        for name in models.keys():
            model = models[name]
            param = params.get(name, {})

            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)

            report[name] = test_model_score

            if test_model_score > best_score:
                best_score = test_model_score
                best_model = model  # Best fitted model with best params

        return report, best_model 

    except Exception as e:
        raise NetworkSecurityException(e, sys)
