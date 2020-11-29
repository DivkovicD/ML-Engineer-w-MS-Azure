<!-- #region -->
#  Project 2 - Creating and Consuming an Azure Auto ML experiment

**Overview of the Project**

This project encompases most common steps in creating Azure Auto ML experiment and consuming it. Two approaches were used, the first showing how the whole process is performed using Azure ML Studio and the second was using Python Azure SDK. The first approach is regarded as low-code-no-code experience and the second is demonstrating how the same scenario can be accompliched through coding in Python SDK for Azure ML.

Ahother key point of the Project was to illustrate use of pipelines aspects, which is commonly known as Pipleine Automation. From efforts to automate pipelines we may conclude that machine learning operations can benefit greatly. Automation is important pillar of DevOps and it's principles and practices applied to machine learning and called MLOps for short.

For the purpose of training the model, public data set "Bank Marketing" was used. This dataset was provided as URI containing csv file with records of data colected during direct marketing phone campaigns of banking inistitution. We were required to use Auto ML feature of Azure ML. Auto ML is freeing machine learning professionals from task of sellecting the best performing model. Instead of focusing on selecting and tuning the model, which is most suitable to make predictions, machine learning professionals can focus on operationalizing and delivering result to end customer. Classification goal was to predict will or will not the client subscribe to term deposit, designated with variable 'y' and values 'yes'/'no'.

Some areas for future improvements may be to set triggers to retrain the model when another (improved) dataset is available. For this purpose we would be needing to create Azure Logic App, provide condition, interval/frequency and URI of HTTP endpoint of the published pipeline. Another area of improvement may be setting Application Insights monitoring for Metrics of endpoints and setting Alerts, for instance on Failed Requests at web server. We may use metrics for performance improvements measures and alerts may be utilized to inform IT system staff about problems with deployed service, while some situations may be remedied by Azure automation.


## Architectural Diagram
*TODO*: Provide an architectual diagram of the project and give an introduction of each step.

There are sevearal clearly distinguishable phases of the project:

- Authentication, to use Azure ML resources,
- Creating Automated ML Experiment, with result of generating Auto ML model,
- Deploying the best model created during Auto ML Experimetn Run,
- Enabling logging to be used for monitoring, performance improvements and debugging
- Consuming deployed models' endpoints and utilizing Swagger tool, and
- Creating and publishing pipeline.

![Architectural Diagram of the Project](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/Project%202%20Arhitectural%20Diagram.png)

## Key Steps
*TODO*: Write a short discription of the key steps. Remeber to include all the screencasts required to demonstrate key steps.

1. Creeate Service Principal and allow acces to workspace

This step accociates SP account with workspace. Since we are aiming to achieve automated continous integration and deployment we need to use service principal to authenticate the service without requiring user interaction.
Screen
Screen

2. Create and run Auto ML Experiment

This step will provide a model we will deploy and consume. There are some mandatory data to fill in the appropriate form, starting with naming the experiment, selecting or creating a dataset for training and designate compute cluster for training, either by using the existing one or creating a new one. In this case we will create the dataset from CSV file given its URI. Then we need to create Auto ML experiment.
Screen

We will deploy new compute cluster and select number of nodes stipulated by project instructions. Optionally, we need to set parameters for Auto ML experiment and finally submit an experiment to run. Checkbox for "Explain the best model" should be thicked and Concurrency adjusted to be one less than number of compute cluster. After the experiment finishes, we will have the best trained model.
Screen
Screen

3. Deploy the Best Model

After completion of this step we will be able to interact with model by HTTP API service. To test this we will besending data over POST requests to the endpoint.
Screen?

4. Enable Application Insights

This step will allow us to retrieve logs after best model deployment. We will do this by running a piece of Python code from terminal window in order to enable Application Insights for the model. After verification of active Application Insights marked as enabled in endpoint details tab, we observer logs displayed by script we used.
Screenshot
Screenshot

5. Using Swagger for Documentation

In order to interact and see explanations of HTTP request types consumed by API of deployed model, we will be using Swagger tool. Preparation for running Swagger requires to download swagger.json file of deployed model from Azure. After running script with Docker setup, we will be using Python script to start server. Then we pass the URI to the Swagger which will analyze the API description.
Screen
Screen?

6. Consuming Deployed Model Endpoints

Shortly the term consume has meaning of interaction with the trained model. Python script is used to make the interaction. The result of running the script is data.json file created in the same  directory.
Screenshot

7. The second part of the Project 2 - Create, Publish and Consume a Pipeline

For this part we will be using a Jupyter notebook containing Azure Python SDK code examples for setting data, environment, configuration and then creating, running, publishing and running from REST endpoint of Azure ML pipeline. In order to be able to open Jupyter notebook we need a compute instance to provide running environment for Python interpreter. Additionally, we need to provide config.json file containing information about Azure subscription we are using and we need to update all variables to match environment. By running all the notebook cells we will create the pipleine and schedule it's run. Results of the run may be observed by using `RunDetails` widget.
screen 13 to 19

"[Screenshot of pipeline section Azure ML studio, showing that the pipeline has been created](https://github.com/DivkovicD/ML-Engineer-w-MS-Azure/blob/master/Screenshots/13.%20Screenshot%20pipeline%20section%20of%20Azure%20ML%20studio%2C%20showing%20that%20the%20pipeline%20has%20been%20created.png)


*TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
<!-- #endregion -->
