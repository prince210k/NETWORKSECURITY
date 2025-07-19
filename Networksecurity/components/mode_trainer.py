import os 
import sys 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from Networksecurity.exception.exception import NetworkSecuirtyException
from Networksecurity.logging.logger import logger
from Networksecurity.entity.config_entity import ModelTrainerConfig
from Networksecurity.entity.artifacts_entity import ModelTrainerArtifact,DataTransformationArtifact
from Networksecurity.utils.main_utils.utils import evaluate_model
from Networksecurity.utils.ml_utils.model.estimator import NetworkModel
from Networksecurity.utils.ml_utils.metric.classification_metric import get_classification_report
from Networksecurity.utils.main_utils.utils import save_object,load_numpy_array,load_object
import mlflow 
class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    def track_mlflow(self,best_model,train_report,test_report):
         
        mlflow.set_experiment("NetworkSecurity_Model_Training")

        with mlflow.start_run():
            mlflow.log_metric("train_f1", train_report.f1_score)
            mlflow.log_metric("train_recall", train_report.recall_score)
            mlflow.log_metric("train_precision", train_report.precision_score)

            mlflow.log_metric("test_f1", test_report.f1_score)
            mlflow.log_metric("test_recall", test_report.recall_score)
            mlflow.log_metric("test_precision", test_report.precision_score)

            mlflow.sklearn.log_model(best_model, "model")
            
            
    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            models = {
                "Random Forest" : RandomForestClassifier(verbose=1),
                'Decision Tree':DecisionTreeClassifier(),
                "AdaBoost": AdaBoostClassifier(),
                "Gradient Boost":GradientBoostingClassifier(verbose=1),
                "SVC" : SVC(verbose=1),
                "Logistic Regression" : LogisticRegression(verbose=1),
                "KNN classifier": KNeighborsClassifier()
            }
            
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boost":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
            
            model_report, best_model = evaluate_model(X_train, y_train, X_test, y_test, models, params)

            best_model_score = max(model_report.values())
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            logger.info(f"Best Model :{best_model_name}, Score : {best_model_score}")
            
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_report(y_train, y_train_pred)
            
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_report(y_test, y_test_pred)
            
            ## Track experiments with mlflow 
            self.track_mlflow(best_model,classification_train_metric,classification_test_metric)
            
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True) 
            
            Networkmodel = NetworkModel(preprocessor,best_model)
            save_object(self.model_trainer_config.trained_model_file_path,Networkmodel)
            
            ## Model Trainer Artifact 
            model_trainer_artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path,
            classification_train_metric,classification_test_metric)
             
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            ## Loading train array and test array
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)
            
            X_train,y_train,X_test,y_test = [
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            ]
            
            model = self.train_model(X_train,y_train,X_test,y_test)
            return model 
        except Exception as e:
            raise NetworkSecuirtyException(e,sys)