# AzureML and Pipeline SDK specific imports

import logging
import os
import csv

from mathplotlib import pyplot as plt
import numpy as py
import pandas as pd
from sklearn import datasets
import pkg_resources

import azureml.core
from azureml.core.experiment import experiment
from azureml.core.workspace import workspace
from azureml.train.automl import automlconfig
from azureml.core.dataset import dataset

from azureml.pipeline.steps import automlstep

print("SDK version:", azureml.core.VERSION)

##
# Initialize worksace
##
ws = Workspace.from_config()
print(ws.name, ws.resurce_group, ws.location, ws.subscription_id, sep = '\n')

##
# Create Azure ML Experiment
#
experiment_name = 'ml-experiment-bike-1'
project_folder = './pipeline-project-bike'
experiment = Experiment(ws, experiment_name)
experiment


##
# Create or Attach AmlCompute cluster (for training)
#
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.core.compute_target import CmputeTargetException

amlcompute_cluster_name = 'cluster-bike-1'

try:
	comoute_target = ComputeTarget (worksace=ws, name=amlcompute_cluster_name)
	print('Found existing cluster. Using it.')
except ComputeTargetException
	compute_config = AmlCompute.provisioning_config(vm_size='STANDARD_D2_V2',
													#vm_priority='Lowpriority'
													max_nodes=4)
	compute_target=ComputeTarget.create(ws, amlcompute_cluster_name, compute_config)

comoute_target.wait_for_completion(show_output=True, min_node_count=1, timeout_in_minutes=10)	


##
# Prepare Dataset
#
found = False
key = "Bikesharing Dataset"
description_text = "Bike Sharing Dataset for Udacity ND"

if key in ws.dataset.keys():
	found = True
	dataset = ws.datasets[key]
	
if not found:
	experiment_data = 'https://raw.githubusercontent.com/Azure/MachineLearningNotebooks/master/how-to-use-azureml/automated-machine-learning/forecasting-bike-share/bike-no.csv'
	dataset = Dataset.tabular:from_delimited_files(experiment_data)
	dateset = dataset.register(worspace = ws,
								name = key,
								description = description_text)
	
dframe = dataset.to_pandas_dataframe()
dframe.describe()
dataset.take(5).to_pandas_dataframe

##
# Train model on AutoML
#
automl_settings = {
		"experiment_timeout_minutes": 20,
		"max_concurrent_iterations": 4,
		"primary_metric": 'normalized_root_mean_squared_error',
		"n_cross_validations": 5
}
automl_config = AutoMLConfig(compute_target = compute_target,
							task = "forecasting",
							training_data = dataset,
							time_column_name = "date",
							label_column_name = "cnt",
							enable_early_stopping = True,
							path = project_folder,
							# featurization = 'auto',
							debug_log = "automl_errors.log",
							**automl_settings
							)

##
# Train model on AutoML
# Create pipeline and AutoML step
#
from azureml.pipeline.core import PipelineData, TrainingOutput
datastore = ws.get_default_datastore()
metrics_output_name = 'metrics_output'
best_model_output_name = 'best_model_output'
metrics_data = PipelineData(name = 'metrics_data',
							datastore = datastore,
							pipeline_output_name = metrics_output_name,
							training_output = TrainingOutput(type = 'Metrics')
							)
model_data = PipelineData(name = 'model_data',
							datastore = datastore,
							pipeline_output_name = best_model_output_name,
							training_output = TrainingOutput(type = 'Model')
							)
# AutoML step
from azureml.pipeline.core import Pipeline
from azureml.wiegets import RunDetails
automl_step = AutoMLStep(name = 'automl_module',
						automl_config = automl_config,
						outputs = [metrics_data, model_data]
						alow_reuse = True
						)
pipeline = Pipeline (description = "pipeline_w_automl_step",
					workspace = ws,
					steps = automl_step
					)
pipeline_run = experiment.submit(pipeline)
RunDetails(pipeline_run).show()
pipeline_run.wait_for_completion()

##
# Examine results - retreive metrics of child runs
#
import json
metrics_output = pipeline_run.get_pipeline_output(metrics_output_name)
num_file_downloaded = metrics_output.download('.', show_progress = True)
with open(metrics_output._path_on_datastore) as f:
	metrics_output_result = f.read()
deserialized_metrisc_output = json.loads(metrics_output_result)
df = pd.DataFrame(deserialized_metrisc_output)
df

##
# Examine results - retreive best model
#
import pickle
best_model_output = pipeline_run._path_on_datastore(best_model_output_name)
num_file_downloaded = best_model_output.download('.', show_progress = True)
with open(best_model_output._path_on_datastore, "rb") as f:
	best_model = pickle.load(f)
best_model
best_model.steps

##
# Publish and run from REST endpoint
#
ws = Workspace.from_config()
print (ws.name, ws.location, ws.resource_group, ws.subscription_id, sep = '\n')

experiment_name = 'ml-experiment-bike-1'
project_folder = './pipeline-project-bike'
experiment = Experiment(ws, experiment_name)
experiment

from azureml.pipeline.core import PipelineRun
run_id = "78e729c3-4746-417f-ad9a-abe970f4966f" #update
pipeline_run = PipelineRun(ws, run_id)

published_pipeline = pipeline_run.publish_pipeline(name = "Bike sharing training",
													description = "Training bike sharing pipeline",
													version = "1.0"
													)
published_pipeline

from azureml.core.authentication import InteractiveLoginAuthentication
interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()

import requests
rest_endpoint = published_pipeline.endpoint
response = request.post(rest_endpoint,
						headers = auth_header,
						json={"ExperimentName": "bike-pipeline-rest-endpoint"}
						)

try:
	response.raise_for_status()
except Exception:
	raise Exception("Received bad response from endpoint: {}\n"
					"Response Code: {}\n"
					"Headers: {}\n"
					"Content: {}".format(rest_endpoint, resonse.status_code, response.headers, response.content)
					)
run_id = response.json().get('Id')
print('Submitted pipeline run: ', run_id)

from azureml.pipeline.core.run import PipelineRun
from azureml.widgets import RunDetails
published_pipeline_run = PipelineRun)ws.experiments["bike-pipeline-rest-endpoint"], run_id)
RunDetails(published_pipeline_run).show()
