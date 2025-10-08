import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logger
from Networksecurity.pipeline.training_pipeline import TrainingPipeline
from Networksecurity.consants.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME

from Networksecurity.utils.main_utils.utils import load_object
from Networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,UploadFile,Request,File
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run 
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca) 

database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],           # Allow all origins (not secure for production!)
    allow_credentials = True,        # Allow cookies, auth headers
    allow_methods = ['*'],           # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers = ["*"]            # Allow any headers (like Authorization, Content-Type)
)

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is successfull")
    except Exception as e:
        return NetworkSecurityException(e,sys)
    
templates = Jinja2Templates(directory="./templates")

@app.post('/predict')
async def predict_route(request: Request,file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        print("CSV loaded successfully")
        
        preprocessor = load_object(file_path='final_model/preprocessor.pkl')
        final_model = load_object(file_path='final_model/model.pkl')
        print("Models loaded successfully")
        
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_label'] = y_pred
        df.to_csv("prediction_output/prediction.csv")
        
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table_html": table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

if __name__=='__main__':
    app_run(app,host='localhost',port=8000)