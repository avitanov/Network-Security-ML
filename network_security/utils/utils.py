import yaml
from network_security.exception.exception import CustomException
from network_security.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path:str)-> str:
    try:
        with open(file_path,"rb") as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path:str,content: object, replace: bool = False)-> str:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file_obj:
            yaml.dump(content,file_obj)
    except Exception as e:
        raise CustomException(e,sys)