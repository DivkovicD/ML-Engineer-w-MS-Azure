# Reccomended approach
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python
#
import json
import numpy as np
import os
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
import pickle
from azureml.core.model import Model
import time

def init():
    global model


def init():
    # Print statement for appinsights custom traces:
    # Reccomended approach
    # https://docs.microsoft.com/en-us/azure/machine-learning/how-to-enable-app-insights
    print ("Model initialized" + time.strftime("%H:%M:%S"))
    global model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'automl-wine-quality-model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    try:
        #data = np.array(json.loads(data))
        #result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        #return result.tolist()
        print ("Request arrived time" + time.strftime("%H:%M:%S"))
        data = np.array(json.loads(raw_data)['data'])
        # make prediction
        y_hat = model.predict(data)
        # Log the input and output data to appinsights:
        # Reccomended approach
        # https://docs.microsoft.com/en-us/azure/machine-learning/how-to-enable-app-insights
        info = {
            "Input": raw_data,
            "Output": result.tolist()
            }
        print(json.dumps(info))
        return json.dumps(y_hat.tolist())

    except Exception as e:
        error = str(e)
        # Print statement for appinsights custom traces:
        # Reccomended approach
        # https://docs.microsoft.com/en-us/azure/machine-learning/how-to-enable-app-insights
        print (error + time.strftime("%H:%M:%S"))
        return error
