import json
import pickle
import numpy as np
import pandas as pd
import os
import joblib
from azureml.core.model import Model

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


def init():
    global model
    path = os.getenv('AZUREML_MODEL_DIR') 
    model_path = os.path.join(path, 'automl-wine-quality-model.pkl')
    model = joblib.load(model_path)


input_sample = pd.DataFrame(data=[{
            "fixed acidity": 7.4,
             "volatile acidity": 0.7,
             "citric acid": 0,
             "residual sugar": 1.9,
             "chlorides": 0.076,
             "free sulfur dioxide": 11,
             "total sulfur dioxide": 34,
             "density": 0.9978,
             "pH": 3.51,
             "sulphates": 0.56,
             "alcohol": 9.4
}])

# Integer type
output_sample = np.array([0])

@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))

def run(data):
    try:
        print("Input:")
        print(data.columns)
        print(type(data))
        result = model.predict(data)
        print("Output:")
        print(result)
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
