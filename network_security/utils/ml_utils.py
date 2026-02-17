import os,sys
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score,precision_score, r2_score,recall_score
from sklearn.model_selection import GridSearchCV

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        classification_metric= ClassificationMetricArtifact(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score,
            )
        return classification_metric
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}

        for i in range(len(list(models))):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]

            gs=GridSearchCV(model,param,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            y_test_pred=model.predict(X_test)
            test_model_score=r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]]=test_model_score

        return report
    except Exception as e:
        raise CustomException(e,sys)
