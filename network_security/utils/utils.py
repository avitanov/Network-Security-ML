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


def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e,sys)

def save_object(file_path: str, obj: object):
    try:
        logging.info("Entered the save_object function")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Saved the object as pikl file")
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} doesnt exist!!")
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def load_numpy_array_data(file_path: str) -> np.ndarray:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)