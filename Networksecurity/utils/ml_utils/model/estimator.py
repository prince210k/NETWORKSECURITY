from Networksecurity.consants.training_pipeline import TRAINED_MODEL_NAME,SAVED_MODEL_DIR
import os 
import sys 
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logger 

## Initialization of saved model, preprocessor and to directly do the prediction of new data points
class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor 
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat 
        except Exception as e:
            raise NetworkSecurityException(e,sys)