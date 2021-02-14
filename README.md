# Capstone Project Azure Machine Learning Engineer

This section contains short introduction to the project.

The goal of the project was to deploy and interact with web service endpoint of the best model as a result of comparison between most successful models trained on Automated ML and HyperDrive tools from Azure ML. There are six phases of the project. The first one was to import the dataset we use for training. This dataset (external) was available on publicly accessible URI. As part of this phase we needed to set up the environment that we will be using for training models. Next two tasks were training models utilizing Automated ML and HyperDrive on the same dataset. For the purpose of simplicity, during comparison we will observe Accuracy of best models from both approaches. The next phase was to deploy the best model as a web service. The last phase of the Capstone project was to test deployed model endpoint and interact with model.

## Project Set Up and Installation
This section contains installation steps, and explanation how to set up this project in Azure ML.

The code accompanying this README.md can be run inside Jupyter Notebook on Azure ML. In order to run Notebook we must deploy compute instance (VM) that will host the Notebook environment. We may use the menu item **Compute** on the left hand side and then **New** (+) -> scroll down Virtual machine size list -> select **Standard_DS11_v2** VM type -> **Next** -> type unique **Compute name** -> set **Minimum number of node**s to 1 -> set **Maximum number of nodes** to higher number -> **Create**. After a while a compute instance will be created and its status "Running". Click on Jupyter link in Application URI column for newly created compute instance to start Jupyter Notebook environment. Click on Users link to navigate into folder structure where you may upload your files using the button Upload. The GitHub repository https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/ contains all files you should first download to your local computer or desktop of VM if you have access to it. Then you upload one two three files to your Users folder in Jupyter Notebook. Please have in mind that config.json file of your subscription needs to be uploaded to the same folder from where you will run code contained in notebooks. This file can be found at Change subscription menu item on top right corner and use the link Download config file will download config.json file to your local computer from where you upload it using the same upload button as for notebooks.
In attempt to simplify and automate as much tasks as possible, we could utilize the code to create compute cluster for model training. The following code snippet may be run to perform setup of folder structure, compute cluster and dataset.

## Dataset

### Overview
In this section we will explain about the data you are using and where you got it from.

The data used for training of the models is obtained from publicly UCI Machine Learning Repository. The dataset contains 1599 records of eleven red wine physicochemical properties and one output variable 'quality' as sensory data denoting perceived quality of wine according to human taste. Quality is scored from 0 to 10, latest denoting the highest quality. Classes are not balanced and there are more 'ordinary' wines than high or poor quality ones (P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis., Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.). The data can be used both for regression and classification machine learning tasks. The dataset can be obtained [here](https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv). 

### Task
In this section we will explain the task we are going to be solving with this dataset and the features will be using for it.

The task we are going to be solving with this dataset is training classification model to predict quality of unknown wine by its physicochemical properties. As starting point we will remove all missing data, as we have to be certain that we are using the clean dataset for training. There are eleven features we will be using for training:
1 - fixed acidity
2 - volatile acidity
3 - citric acid
4 - residual sugar
5 - chlorides
6 - free sulfur dioxide
7 - total sulfur dioxide
8 - density
9 - pH
10 - sulphates
11 - alcohol
All features are numeric, which makes data preparation part of project less demanding and we will not be focusing on it. After feeding training data to both tasks separately we will use accuracy of trained models to select better approach and deploy best model as web service.

### Access
This section explains how we are accessing the data in our workspace.

There are several methods for accessing the data. The one is creating and registering a dataset inside Azure ML Studio. In this way we may utilize the same dataset for various experiment runs configured in Azure ML interface or using Azure ML Python SDK. For the purpose of Azure ML Automatic ML experiment, we register the dataset by using menu item **Datasets** -> **Create dataset** (+) on Registered datasets blade -> **From web files** -> fill in Web URL -> fill in Name (dataset name field) -> Tabular (dataset type) -> **Next** -> Column headers -> select **Use headers from the first file** -> **Next** -> **Next** -> **Create**. Another way to access the data is directly from Python notebook using for example using `TabularDatasetFactory` class and performing necessary transformations and manipulation with training data, such as splitting it to training and test subsets. We will use both approaches in this project. In order to avoid setbacks while preparation of Automatic ML training, we will use simple code to verify if the dataset was already registered and using that registered dataset for training.

## Automated ML
In this section we will give an overview of the `automl` settings and configuration we used for this experiment.

AutoML training script selects optimal parameters and passes them to all legible algorithms for classification task, therefore enlarging chance to find the best combination of algorithm/model and parameters relevant for that model. For this project we have selected classification task with accuracy as primary metric, with limited time for training of all iterations set to 20 minutes and maximum of 5 concurrent iterations. There are almost sixty configurations and settings presently. For the purpose of this project we have used some of them.

Setting | Value | Explanation
--- | --- | --- 
experiment_timeout_minutes | 20 | Maximum amount of time in hours that all iterations combined can take before the experiment terminates.
max_concurrent_iterations | 5 | Represents the maximum number of iterations that would be executed in parallel.
primary_metric | accuracy | The metric that Automated Machine Learning will optimize for model selection.

Configuration | Value | Explanation
--- | --- | --- 
compute_target | compute_target | The Azure Machine Learning compute target to run the Automated Machine Learning experiment on.
task | "classification" | The type of task to run. Values can be 'classification', 'regression', or 'forecasting' depending on the type of automated ML problem to solve.
training_data | dataset | The training data to be used within the experiment. It should contain both training features and a label column.
label_column_name | "quality" |  The name of the label column.
path |  "./aml" | The full path to the Azure Machine Learning project folder.
enable_early_stopping | True | Whether to enable early termination if the score is not improving in the short term. 
featurization | 'auto' | Indicator for whether featurization step should be done automatically or not, or whether customized featurization should be used.
debug_log | "automl_errors.log" | The log file to write debug information to. If not specified, 'automl.log' is used.

More explanations can be found here. https://docs.microsoft.com/en-us/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig?view=azure-ml-py

### Results
This section explains the results we got with automated ML model, the parameters of the model and how could we have improved it.

The result of AutoML run was VotingEnsemble model which achieved accuracy of 0.70294. The result of this model is a combined performance of best performing models from AutoML experiment run. The ensemble was created from previous AutoML iterations with soft voting. The VotingEnsemble consists of ensembled_algorithms : ['XGBoostClassifier', 'KNN', 'LightGBM', 'XGBoostClassifier', 'XGBoostClassifier', 'LightGBM', 'LightGBM', 'XGBoostClassifier', 'LightGBM', 'SVM', 'ExtremeRandomTrees', 'LightGBM'], which are top 12 models rated by accuracy. The AutoML Voting Ensemble selected parameters read from azureml-logs:

- 'ensemble_iterations': 35, 27, 0, 50, 1, 39, 44, 45, 8, 7, 28, 31
- 'training_type': 'MeanCrossValidation'
- 'goal': 'accuracy_max'
- 'primary_metric': 'accuracy'

Other AutoML parameters were mostly default values. The detailed list of parameters can also be obtained from Raw JSON file located under "See all properties" of Details blade of the AutoML experiment. The closest best model to VotingEnsemble was XGBoostClassifier with StandardScalerWrapper which achieved accuracy of 0.67417.
By looking at metrics of VotingEnsemble model we may observe some area for improvements. Precision and recall chart indicates low precision model. Imbalanced classes were detected in our inputs, so we may give some effort into sampling of the data to even the class imbalance. Calibration curve indicates traces of over-fitting which we may correct by using more data as the simplest and best possible way to prevent over-fitting, and typically increases accuracy.

The next is a screenshots of the `RunDetails` widget followed by a screenshot of the best model trained with it's parameters.

![1](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/Screenshot%20of%20RunDetails%20widget%20showing%20the%20progress%20of%20training%20runs%20of%20different%20experiments%20v5.png)

Screenshot of RunDetails widget showing the progress of AutoML training runs of different experiments

![2](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/Screenshot%20of%20the%20best%20model%20(AutoML)%20with%20its%20run%20id.png)

Screenshot of the best model (AutoML) with its run id

## Hyperparameter Tuning

This section explains which model did we choose for this experiment and why. We will also give an overview of the types of parameters and their ranges used for the hyperparameter search.

Since we have decided to perform classification task on previous step, we may as well select one of classification algorithms for HyperDrive part of the project, in order to give both approaches the same conditions. Primary metric was accuracy, the same as for previous step with maximize goal.

Hyperparameter tuning is used to automate the process of training several models with different parameters to find the best model. There are three configurations required by project: estimator, hyperparameter sampler and policy. Estimator provides information on what script will be used to perform training and on what compute target. Hyperparameter sampler provides a search domain (space) from which parameters for training script will be selected and fed to training script. Hyperparameter tuning is performed by generating random combinations of parameters. There are two hyperparameters spaces "C" and "max_iter". Hyperparameter "C" denominates inverse of regularization strength, smaller values specify stronger regularization. The Logistic Regression model is fitted with training data and scored with test data. Early termination policy (bandit) is preventing long runs on experiment.

### Results
This section will describe the results we achieved with model, what were the parameters of the model and How we could have improved it.

The Logistic Regression model trained with HyperDrive achieved accuracy of 0.58787 with hyperparameters C = 10.0 and max_iter = 50. This is 10% worse compered to AutoML VotingEnsemble accuracy. For given experiment three fixed values were chosen for C parameter space (10.0, 1.0, 0.1). Hyperparameter "max_iter" denominates maximum number of iterations of the optimization algorithm, and three values were offered in this space (50, 100, 200). Logistic Regression classification algorithm accepts two parameters parsed from parameters passed by estimator, selected randomly to achieve convergence faster. 

For further experiments the dataset should be enriched with more cases belonging to high and low quality wine. Another area of improvement is modification of hyperparameter space for C to offer stronger regularization. This can be done by moving space to smaller values (0.001, 0.01, 0.1, 1.0). Perhaps one more thing is making difference in max_iter by increasing the upper limit of pace to 1000 iterations (100, 500, 1000).

The next is a  screenshot of the `RunDetails` widget followed by a screenshot of the best model trained with it's parameters.

![3](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/screenshot%20of%20the%20RunDetails%20HyperParameter%20widget%20that%20shows%20the%20progress%20of%20the%20training%20runs%20of%20the%20different%20experiments%20v3.png)

Screenshot of the RunDetails HyperDrive widget that shows the progress of the training runs of the different experiments

![4](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/Screenshot%20of%20the%20best%20model%20with%20its%20run%20id%20and%20the%20different%20hyperparameters%20that%20were%20tuned.png)

Screenshot of the best model with its run id and the different hyperparameters that were tuned

## Model Deployment
In this section we will give an overview of the deployed model and instructions on how to query the endpoint with a sample input.

We may conclude that Azure Auto ML produced VotingEnsemble model by comparing selected metrics, and this is going to be model selected for deployment.

When we deploy the ML model, Azure ML basically creates REST API endpoint and therefore we are accessing the model as a web service. We are sending the data to the endpoint and receiving prediction from the model. We may deploy locally, to ACI, AKS or FPGA. In order to do this we need to know URI of the web service and the type of data used by the model. There are several usual ways to deploy a model: Azure CLI, Azure Portal and Python code. Tasks we need to perform usually are to register the model, create an inference config, prepare entry script, choose compute target and deploy the model as a web service.

After a while web service is started and this is an indication that model is deployed. Making note of `scoring_uri` will enable us to send a request to the web service deployed in order to test it. Interaction with web service may be performed with curl command.

An important aspect of monitoring an endpoint of deployed model is observing the service logs. Last but not least we will delete the service and compute target in order to reduce costs.

## Screen Recording
Please use the following [link](https://www.dailymotion.com/video/x7zba4q) to a screencast of entire process of working machine learning application on Microsoft Azure ML walkthrough . The Capstone Project is about operationalizing machine learning and we will cover the following areas:

- Observe a working model
- Short Demo of the deployed  model
- Brief Demo of a sample request sent to the endpoint and its response

## Standout Suggestions
This section contains information about standout suggestions that I have attempted.

By enabling logging in deployed web app, we may log useful data about the requests being sent to the webapp. For the purpose of conceptual demonstration we will log inference time, the time at which the request arrived, input and output during inference, and the time any errors occur. The scoring file used by web service `score-w-appinsig.py` contains code in order to perform logging in the deployed web app. We will collect data using Azure Application Insights, a feature of [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/overview). This is a service for developers and DevOps professionals used to monitor live applications. It detects performance anomalies, help diagnosing issues and understand what users actually do with application. It's designed to continuously improve performance and usability of deployed applications.

The following is a screenshot of the logs and metrics collected:

![Screenshot App Insights](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/Screenshot%20App%20Insights.png)

![Endpoint logs](https://github.com/DivkovicD/python-repo/blob/master/capstone-4-submission-final-14022021/Screenshots/Endpoint%20logs.png)
