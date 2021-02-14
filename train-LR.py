from sklearn.linear_model import LogisticRegression
import argparse
import os
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
import pandas as pd
from azureml.core.run import Run
from azureml.data.dataset_factory import TabularDatasetFactory

# Create TabularDataset using TabularDatasetFactory
# Data is located at:
# web_uri = https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
# ds =TabularDatasetFactory.from_delimited_files(path=web_uri)
# Can be placed to azure datasets and taken from there for each round of training
# Try to load the dataset from the Workspace. Otherwise, create it from the file
#
found = False
key = "wine-quality"
description_text = "Wine Quality DataSet for Udacity Capstone Project"

import azureml.core
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.core.dataset import Dataset

# test this or line above if statement and un-comment what works best
run = Run.get_context()
# ws = run.experiment.workspace # for access to workspace without authentication
# test this and comment if necessary
ws = Workspace.from_config()

if key in ws.datasets.keys(): 
        found = True
        ds = ws.datasets[key] 

if not found:
        # Create AutoML Dataset and register it into Workspace
        web_uri = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
        ds = Dataset.Tabular.from_delimited_files(web_uri)        
        #Register Dataset in Workspace
        ds = dataset.register(workspace=ws,
                                   name=key,
                                   description=description_text)

df = ds.to_pandas_dataframe()
y = df.pop('quality')
x = df

# Split data into train and test sets.
#
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=321)

def main():
    # Add arguments to script
    parser = argparse.ArgumentParser()

    parser.add_argument('--C', type=float, default=1.0, help="Inverse of regularization strength. Smaller values cause stronger regularization")
    parser.add_argument('--max_iter', type=int, default=100, help="Maximum number of iterations to converge")

    args = parser.parse_args()
    
    key = "wine-quality"
    ds = ws.datasets[key]
    df = ds.to_pandas_dataframe()
    df.dropna(inplace=True)
    y = df.pop('quality')
    x = df
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=321)
    
    run.log("Regularization Strength:", np.float(args.C))
    run.log("Max iterations:", np.int(args.max_iter))

    model = LogisticRegression(C=args.C, max_iter=args.max_iter).fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    run.log("Accuracy", np.float(accuracy))
    
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(model, './outputs/lr-model.joblib')

if __name__ == '__main__':
    main()
