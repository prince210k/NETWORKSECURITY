from sklearn.metrics import f1_score,precision_score,recall_score
from Networksecurity.entity.artifacts_entity import ClassificationMetricArtifact
from Networksecurity.exception.exception import NetworkSecurityException
import sys 

def get_classification_report(y_true,y_pred)-> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_pred,y_true)
        model_precision = precision_score(y_pred,y_true)
        model_recall = recall_score(y_pred,y_true)
        return ClassificationMetricArtifact(model_f1_score,model_recall,model_precision)
    except Exception as e:
        raise NetworkSecurityException(e,sys)