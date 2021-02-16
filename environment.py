# This code saves training environment
# Environment file 'environment.yml' is uploaded to GitHub for future trainings
#
from azureml.core.environment import Environment
from azureml.automl.core.shared import constants
best_run.download_file(constants.CONDA_ENV_FILE_PATH, 'environment.yml')
environment = Environment.from_conda_specification(name="environment", file_path="environment.yml")
