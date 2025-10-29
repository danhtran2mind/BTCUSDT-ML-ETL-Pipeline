# BTCUSDT-ML-ETL-Pipeline

[![GitHub Stars](https://img.shields.io/github/stars/danhtran2mind/BTCUSDT-ML-ETL-Pipeline?style=social&label=Repo%20Stars)](https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/stargazers)
![Badge](https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2Fdanhtran2mind%2FBTCUSDT-ML-ETL-Pipeline&label=Repo+Views&icon=github&color=%236f42c1&message=&style=social&tz=UTC)

[![pyspark](https://img.shields.io/badge/PySpark-blue.svg?logo=apachespark)](https://spark.apache.org/docs/latest/api/python/)
[![airflow](https://img.shields.io/badge/Airflow-blue.svg?logo=apacheairflow)](https://airflow.apache.org/)
[![minio](https://img.shields.io/badge/MinIO-blue.svg?logo=minio)](https://min.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A modern, scalable data engineering pipeline for processing BTC-USDT trading data using Apache Airflow, MinIO, and Apache Spark.

## Introduction

This project delivers a robust, cloud-native ETL pipeline for extracting, transforming, and loading BTC-USDT trading data, leveraging industry-leading tools for orchestration, storage, and distributed processing.

## Key Features

- **Workflow Orchestration**: Flexible Directed Acyclic Graphs (DAGs) in Apache Airflow to manage **BTC-USDT ETL** workflows.
- **Data Storage**: MinIO for efficient storage of raw and processed datasets.
- **Data Processing**: Apache Spark for high-performance, large-scale data transformations and analytics.
- **Machine Learning Forecasting**: Integrated ML pipeline with feature engineering, model training (e.g., LSTM), and price prediction for BTC-USDT.

## Technologies

- **MinIO**: Object storage for managing raw and processed data.
- **Apache Spark**: Distributed processing engine for scalable data transformations.
- **Apache Airflow**: Orchestrates and schedules ETL workflows for reliable execution.

## Notebooks
### 1. **Analyze historical BTC/USDT trading data with visualizations, statistical insights, and preprocessing steps for machine learning.**
Interactive notebook for exploratory data analysis (EDA) on Binance BTC/USDT perpetual futures data. Includes candlestick charts, volume analysis, volatility metrics, and feature engineering for ML models.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/explore_datasets.ipynb)
[![Open in SageMaker](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/explore_datasets.ipynb)
[![Open in Deepnote](https://deepnote.com/buttons/launch-in-deepnote-small.svg)](https://deepnote.com/launch?url=https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/explore_datasets.ipynb)
[![JupyterLab](https://img.shields.io/badge/Launch-JupyterLab-orange?logo=Jupyter)](https://mybinder.org/v2/gh/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/main?filepath=notebooks/explore_datasets.ipynb)
[![Open in Gradient](https://assets.paperspace.io/img/gradient-badge.svg)](https://console.paperspace.com/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/explore_datasets.ipynb)
[![Open in Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/main?filepath=notebooks/explore_datasets.ipynb)
[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/notebooks/welcome?src=https%3A%2F%2Fgithub.com%2Fdanhtran2mind%2FBTCUSDT-ML-ETL-Pipeline%2Fblob%2Fmain%2Fnotebooks%2Fexplore_datasets.ipynb)
[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?logo=github)](https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/explore_datasets.ipynb)


### 2. **From raw Binance futures data → ETL → Feature Engineering → Model Training & Evaluation**  
Run the **complete machine learning pipeline** in one notebook:  
- Fetch & clean BTC/USDT perpetual futures data  
- Build technical indicators & volatility features  
- Train/test split with time-series validation
- Train LSTM models for price direction prediction  
- Evaluate with precision, recall, and backtest-ready signals

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/full_workflow.ipynb)
[![Open in SageMaker](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/full_workflow.ipynb)
[![Open in Deepnote](https://deepnote.com/buttons/launch-in-deepnote-small.svg)](https://deepnote.com/launch?url=https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/full_workflow.ipynb)
[![JupyterLab](https://img.shields.io/badge/Launch-JupyterLab-orange?logo=Jupyter)](https://mybinder.org/v2/gh/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/main?filepath=notebooks/full_workflow.ipynb)
[![Open in Gradient](https://assets.paperspace.io/img/gradient-badge.svg)](https://console.paperspace.com/github/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/full_workflow.ipynb)
[![Open in Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/main?filepath=notebooks/full_workflow.ipynb)
[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/notebooks/welcome?src=https%3A%2F%2Fgithub.com%2Fdanhtran2mind%2FBTCUSDT-ML-ETL-Pipeline%2Fblob%2Fmain%2Fnotebooks%2Ffull_workflow.ipynb)
[![View on GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?logo=github)](https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline/blob/main/notebooks/full_workflow.ipynb)

## Quickstart Guide

Follow these steps to set up and run the **BTC-USDT ETL pipeline**.

### 1. Clone the Repository

```bash
git clone https://github.com/danhtran2mind/BTCUSDT-ML-ETL-Pipeline.git
cd BTCUSDT-ML-ETL-Pipeline
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up MinIO

#### Install MinIO

Execute the provided script to install MinIO:

```bash
python scripts/install_minio.py
```

For additional configuration options, refer to [MinIO Server Installation](docs/install_minio_server.md).

#### Configure MinIO Secrets

Create a `minio.env` file in the project root with the following:

```bash
MINIO_ROOT_USER=<your_username>
MINIO_ROOT_PASSWORD=<your_password>
MINIO_HOST=localhost:9192
MINIO_CONSOLE_ADDRESS=localhost:9193
```

Replace `<your_username>` and `<your_password>` with secure credentials of your choice.

#### Start MinIO Server

Set environment variables and launch the MinIO server:

```bash
export MINIO_ROOT_USER=<your_username>
export MINIO_ROOT_PASSWORD=<your_password>
# Start server with credentials
MINIO_ROOT_USER=$MINIO_ROOT_USER MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD \
./minio server ~/minio-data --address :9192 --console-address :9193 > logs/minio_server.log 2>&1 &
```

### 4. Set Up Apache Spark

#### Quick Setup

Run the provided script for a streamlined Spark installation:

```bash
python scripts/install_spark.py
```

For manual installation, follow the [Spark Installation Guide](docs/install_spark.md).

### 5. Set Up Apache Airflow

#### Install Airflow

Use the quick installation script:

```bash
python scripts/install_airflow.py
```

For detailed instructions, see the [Airflow Installation Guide](docs/install_airflow.md).

#### Configure Airflow Home

Set the Airflow home directory:

```bash
python scripts/installation_airflow.py
```

### 6. Access Airflow

Navigate to `http://localhost:8081` in your browser. Log in with the default credentials:
- Username: `admin`
- Password: `admin`

Use the Airflow UI to trigger and monitor **BTC-USDT ETL** workflows.

### 6. Export Data to CSV for Visualization

You can read more at [Export DuckDB to CSV](docs/visualize_data.md)

## Troubleshooting

- **MinIO Fails to Start**: Verify ports `9192` and `9193` are free. Review `logs/minio_server.log` for error details.
- **Airflow UI Unreachable**: Ensure the webserver is running and port `8081` is open. Check `logs/airflow.log` for issues.
- **Spark Issues**: Confirm `SPARK_HOME` and `PYSPARK_PYTHON` environment variables are correctly configured.