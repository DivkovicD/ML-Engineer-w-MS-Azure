from azureml.core.environment import Environment
from azureml.automl.core.shared import constants
best_run.download_file(constants.CONDA_ENV_FILE_PATH, 'myenv.yml')
myenv = Environment.from_conda_specification(name="myenv", file_path="myenv.yml")
