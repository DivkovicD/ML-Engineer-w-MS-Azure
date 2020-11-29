<!-- #region -->
#  Project 2 - Creating and Consuming an Azure Auto ML experiment

**Overview of the Project**

This project encompasses most common steps in creating Azure Auto ML experiment and consuming it. Two approaches were used, the first showing how the whole process is performed using Azure ML Studio and the second was using Python Azure SDK. The first approach is regarded as low-code-no-code experience and the second is demonstrating how the same scenario can be accomplished through coding in Python SDK for Azure ML.

Another key point of the Project was to illustrate use of pipelines aspects, which is commonly known as Pipeline Automation. From efforts to automate pipelines we may conclude that machine learning operations can benefit greatly. Automation is important pillar of DevOps and its principles and practices applied to machine learning and called MLOps for short.

For the purpose of training the model, public data set "Bank Marketing" was used. This dataset was provided as URI containing csv file with records of data collected during direct marketing phone campaigns of banking institution. We were required to use Auto ML feature of Azure ML. Auto ML is freeing machine learning professionals from task of selecting the best performing model. Instead of focusing on selecting and tuning the model, which is most suitable to make predictions, machine learning professionals can focus on operationalizing and delivering result to end customer. Classification goal was to predict will or will not the client subscribe to term deposit, designated with variable 'y' and values 'yes'/'no'.


*Some areas for future improvements may be to set triggers to retrain the model when another (improved) dataset is available. For this purpose we would be needing to create Azure Logic App, provide condition, interval/frequency and URI of HTTP endpoint of the published pipeline. Another area of improvement may be setting Application Insights monitoring for Metrics of endpoints and setting Alerts, for instance on Failed Requests at web server. We may use metrics for performance improvements measures and alerts may be utilized to inform IT system staff about problems with deployed service, while some situations may be remedied by Azure automation.*


## Architectural Diagram
*TODO*: Provide an architectual diagram of the project and give an introduction of each step.

There are several clearly distinguishable phases of the project:

- Authentication, to use Azure ML resources,
- Creating Automated ML Experiment, with result of generating Auto ML model,
- Deploying the best model created during Auto ML Experiment Run,
- Enabling logging to be used for monitoring, performance improvements and debugging
- Consuming deployed models' endpoints and utilizing Swagger tool, and
- Creating and publishing pipeline.

![Architectural Diagram of the Project](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/Project%202%20Arhitectural%20Diagram.png)

## Key Steps
In this section a short description of the key steps may be found. We have included all relevant and required screenshots in order to demonstrate key steps.

1. Create Service Principal and allow access to workspace

This step was optional and therefore details and illustrations may be found in "Standout suggestions" section of this README.md file.

2. Create and run Auto ML Experiment

This step will provide a model we will deploy and consume. There are some mandatory data to fill in the appropriate form, starting with naming the experiment, selecting or creating a dataset for training and designate compute cluster for training, either by using the existing one or creating a new one. In this case we will create the dataset from CSV file given its URI. Then we need to create Auto ML experiment.

![Screenshot of "Registered Datasets" in ML Studio showing that Bankmarketing dataset is available](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/1.%20screenshot%20of%20-Registered%20Datasets-%20in%20ML%20Studio%20showing%20that%20Bankmarketing%20dataset%20available.png)
Screenshot of "Registered Datasets" in ML Studio showing that Bankmarketing dataset is available


We will deploy new compute cluster and select number of nodes stipulated by project instructions. Optionally, we need to set parameters for Auto ML experiment and finally submit an experiment to run. Checkbox for "Explain the best model" should be ticked and Concurrency adjusted to be one less than number of compute cluster. After the experiment finishes, we will have the best trained model.

![Screenshot showing that the experiment is displayed as completed](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/2.%20Screenshot%20showing%20that%20the%20experiment%20is%20displayed%20as%20completed%E2%80%8B.png)
Screenshot showing that the Experiment is displayed as completed


![Screenshot of the best model after the experiment completes](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/3.%20Screenshot%20of%20the%20best%20model%20after%20the%20experiment%20completes.png)
Screenshot of the best model after the Experiment completes


3. Deploy the Best Model

After completion of this step we will be able to interact with model by HTTP API service. To test this we will be sending data over POST requests to the endpoint.

![Deploy the model with Authentication using Azure Container Instance (ACI)](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/4.%20Deploy%20the%20model%20with%20Authentication%20using%20Azure%20Container%20Instance%20(ACI)%E2%80%8B.png)
Deploy the model with Authentication using Azure Container Instance (ACI)


4. Enable Application Insights

This step will allow us to retrieve logs after best model deployment. We will do this by running a piece of Python code from terminal window in order to enable Application Insights for the model. After verification of active Application Insights marked as enabled in endpoint details tab, we observer logs displayed by script we used.

![Screenshot showing that Application Insights is enabled in the Details tab of the endpoint](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/8.%20Screenshot%20showing%20that%20Application%20Insights%20is%20enabled%20in%20the%20Details%20tab%20of%20the%20endpoint%E2%80%8B.png)
Screenshot showing that Application Insights is enabled in the Details tab of the endpoint


![Screenshot showing logs by running the provided logs.py script](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/9.%20Screenshot%20showing%20logs%20by%20running%20the%20provided%20logs.py%20script.png)
Screenshot showing logs by running the provided logs.py script


5. Using Swagger for Documentation

In order to interact and see explanations of HTTP request types consumed by API of deployed model, we will be using Swagger tool. Preparation for running Swagger requires to download swagger.json file of deployed model from Azure. After running script with Docker setup, we will be using Python script to start server. Then we pass the URI to the Swagger which will analyze the API description.

![Screenshot showing that swagger runs on localhost showing the HTTP API methods and responses for the model](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/10.%20Screenshot%20showing%20that%20swagger%20runs%20on%20localhost%20showing%20the%20HTTP%20API%20methods%20and%20responses%20for%20the%20model%E2%80%8B.png)
Screenshot showing that swagger runs on localhost showing the HTTP API methods and responses for the model


![Screenshot showing that swagger runs on localhost showing the HTTP API methods and responses for the model](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/10b.%20Screenshot%20showing%20that%20swagger%20runs%20on%20localhost%20showing%20the%20HTTP%20API%20methods%20and%20responses%20for%20the%20model%E2%80%8B.png)
Screenshot showing that swagger runs on localhost showing the HTTP API methods and responses for the model


6. Consuming Deployed Model Endpoints

Shortly the term consume has meaning of interaction with the trained model. Python script is used to make the interaction. The result of running the script is data.json file created in the same  directory.

![Screenshot showing that theendpoint.py script runs against the API producing JSON output from the model](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/11.%20Screenshot%20showing%20that%20theendpoint.py%20script%20runs%20against%20the%20API%20producing%20JSON%20output%20from%20the%20model.png)
Screenshot showing that theendpoint.py script runs against the API producing JSON output from the model


7. The second part of the Project 2 - Create, Publish and Consume a Pipeline

For this part we will be using a Jupyter notebook containing Azure Python SDK code examples for setting data, environment, configuration and then creating, running, publishing and running from REST endpoint of Azure ML pipeline. In order to be able to open Jupyter notebook we need a compute instance to provide running environment for Python interpreter. Additionally, we need to provide config.json file containing information about Azure subscription we are using and we need to update all variables to match environment. By running all the notebook cells we will create the pipeline and schedule its run. Results of the run may be observed by using `RunDetails` widget.

![Screenshot of pipeline section Azure ML studio, showing that the pipeline has been created](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/13.%20Screenshot%20pipeline%20section%20of%20Azure%20ML%20studio%2C%20showing%20that%20the%20pipeline%20has%20been%20created.png)
Screenshot of pipeline section Azure ML Studio, showing that the pipeline has been created


![Screenshot of pipelines section in Azure ML Studio, showing the Pipeline Endpoint](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/14.%20Screenshot%20of%20pipelines%20section%20in%20Azure%20ML%20Studio%2C%20showing%20the%20Pipeline%20Endpoint.png)
Screenshot of pipelines section in Azure ML Studio, showing the Pipeline Endpoint


![Screenshot Bankmarketing dataset with the AutoML module](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/15.%20Screenshot%20Bankmarketing%20dataset%20with%20the%20AutoML%20module.png)
Screenshot of Bankmarketing dataset with the AutoML module


![Screenshot of -Published Pipeline overview-, showing a REST endpoint and a status of ACTIVE](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/16.%20Screenshot%20of%20-Published%20Pipeline%20overview-%2C%20showing%20a%20REST%20endpoint%20and%20a%20status%20of%20ACTIVE.png)
Screenshot of "Published Pipeline overview", showing a REST endpoint and a status of ACTIVE

![Screenshot Jupyter Notebook, showing that the -Use RunDetails Widget- shows the step runs](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/17.%20Screenshot%20Jupyter%20Notebook%2C%20showing%20that%20the%20-Use%20RunDetails%20Widget-%20shows%20the%20step%20runs.png)
Screenshot of Jupyter Notebook, showing that the "Use `RunDetails` Widget" shows the step runs


![Screenshot ML studio showing the scheduled run](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/18.%20Screenshot%20ML%20studio%20showing%20the%20scheduled%20run%E2%80%8B.png)
Screenshot of ML studio showing the scheduled run


![Best model trained w paramaters](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/20.%20Best%20model%20trained%20w%20paramaters.png)
Screenshot of best model trained showing parameters


## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:

## Standout Suggestions
In this section we provide information about any standout suggestions that were attempted.

This optional step associates Service Principal account with Azure ML Workspace. Since we are aiming to achieve automated continuous integration and deployment we need to use service principal to authenticate the service without requiring user interaction.

![Creating conditions for RBAC on Azure](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/w_authentication_3.png)
Creating conditions for RBAC on Azure

![Locating ObjectId of Service Principal](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/w_authentication_4.png)
Locating ObjectId of Service Principal

![Assigining role to Service Principal](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/w_authentication_6.png)
Assigning role to Service Principal

Another optional step is an illustration of using Apache Benchmark for load testing deployed model

![Screenshot showing that Apache Benchmark (ab) runs against the HTTP API using authentication keys to retrieve performance results I](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/12.%20Screenshot%20showing%20that%20Apache%20Benchmark%20(ab)%20runs%20against%20the%20HTTP%20API%20using%20authentication%20keys%20to%20retrieve%20performance%20results.png)
Screenshot showing that Apache Benchmark (ab) runs against the HTTP API using authentication keys to retrieve performance results

![Screenshot showing that Apache Benchmark (ab) runs against the HTTP API using authentication keys to retrieve performance results II](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/12a.%20Screenshot%20showing%20that%20Apache%20Benchmark%20(ab)%20runs%20against%20the%20HTTP%20API%20using%20authentication%20keys%20to%20retrieve%20performance%20results.png)
Screenshot showing that Apache Benchmark (ab) runs against the HTTP API using authentication keys to retrieve performance results

<!-- #endregion -->
