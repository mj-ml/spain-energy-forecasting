# Prediction of energy consumption in Spain

## Problem description

The goal of this project is to predict the energy consumption in Spain.

The project was based on the following dataset.

https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather

The project runs in docker compose, which contains mlflow server for experiment tracking and model registry and API
orchestrating everything (prefect).
The monitoring endpoint is able to calculate the metrics and retrain the models if required.
The predictions are returned using webserver (flask).

## ML details

The algorithm uses random forest taking into account the following features

- mean temperature in Spain on a given hour (-30 .. 30 C)
- day of year (1st of Jan = 1) (1..365)
- hour of day (1..24)
  it will produce an estimate of total country level load in MWh.

# Technical guide

## Cloud

The project is deployed using docker compose. All required components are already included.

In order to start the project run the following line:

```docker compose build```

and later

```docker compose up -d```

In the file

```python3 src/hit_api.py```

you will find all possible actions using the model

* check if the deployment is alive
* train the models
* predict.

For the first time please run the file as it is - so that the model can be initialised.

The only required library in your local machine is `requests` - please make sure you have it installed! :)

```python
import requests

"""
Example pipeline
"""
params = {"temp": 0, "hour": 1, "day": 150}

url = "http://localhost:9696/alive"
response = requests.post(url)
if response.status_code == 200:
    print("run test alive: all good")

url = 'http://localhost:9696/train'
response = requests.post(url)
if response.status_code == 200:
    print("train the models: all good")

url = "http://localhost:9696/predict"
response = requests.post(url, json=params)
if response.status_code == 200:
    resp = response.json()
    print(f"the predicted load is {resp['load']}")
```

## Experiment tracking and model registry

Running hit_api.py will:

- check if the deployment is ok
- will create an experiment and it will try a couple of ML models
- the best model according to our metrics (MAPE) will be stored in the registry and used in the process

## Workflow orchestration

The workflow is orchestrated in the API directly using Prefect. There is nothing to be done manually.

## Model deployment

The model is deployed as a webservice. (flask)
The API will call MLFlow, it will extract the best possible model, and it will run against the provided data.

## Model monitoring

There is model monitoring and if the MAPE (mean absolute percentage error, the most common metric is time series
forecasting) is too high, the API will re-run the model training.

```python
import requests

url = 'http://localhost:9696/monitoring'
response = requests.post(url)
if response.status_code == 200:
    print("train the models: all good")
```

## Reproducibility

Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies
are specified. :D

Linter and sonarcloud applied directly in PyCharm.

## Best practices

In the repo you can find

* [ ] There are unit tests
* [ ] There is an integration test
* [ ] Linter and/or code formatter are used
* [ ] There's a CI/CD pipeline (2 points)
