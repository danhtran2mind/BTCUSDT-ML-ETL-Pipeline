import os
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
from sklearn.metrics import (
    mean_squared_error, 
    mean_absolute_error, 
    mean_absolute_percentage_error
)
from typing import Dict, Tuple
from datetime import datetime
import tensorflow as tf
import sys
import ast

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from components.utils.file_utils import load_extract_config, get_parquet_file_names
from components.model.model_utils import build_model_from_config
from components.model.data_utils import create_data_loader

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def model_evaluate(model, scaler: MinMaxScaler, ds: tf.data.Dataset) -> Tuple[float, float, float]:
    """Evaluate a model on a dataset and return RMSE, MAE, MAPE.

    Args:
        model: Trained Keras model.
        scaler (MinMaxScaler): Scaler used for data normalization.
        ds (tf.data.Dataset): Dataset to evaluate on.

    Returns:
        Tuple[float, float, float]: RMSE, MAE, MAPE metrics.
    """
    # Collect true labels
    y_true = []
    for _, y in ds:
        y_true.append(y.numpy())
    y_true = np.concatenate(y_true)

    # Predict entire dataset efficiently
    y_pred = model.predict(ds, verbose=0)

    # Inverse transform to original scale
    y_true_orig = scaler.inverse_transform(y_true)
    y_pred_orig = scaler.inverse_transform(y_pred)

    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))
    mae = mean_absolute_error(y_true_orig, y_pred_orig)
    mape = mean_absolute_percentage_error(y_true_orig, y_pred_orig)

    return rmse, mae, mape


def metric_and_predict_lstm_model(train_result: Dict) -> Dict:
    """Evaluate the trained LSTM model and predict the next price.

    Args:
        train_result (Dict): Training result dictionary from train_lstm_model task.
                            Can be dict or string (for Airflow XCom compatibility).

    Returns:
        Dict: Evaluation metrics and prediction metadata.
    """
    if not train_result:
        raise ValueError("No training result provided.")

    # Safely convert string (from Airflow) to dict; skip if already dict
    if isinstance(train_result, str):
        try:
            train_result = ast.literal_eval(train_result)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Failed to parse train_result string: {e}")
    elif not isinstance(train_result, dict):
        raise TypeError("train_result must be a dict or a string representation of a dict")

    # Load configs
    cfg = load_extract_config('model_config.yml')
    pipeline_cfg = load_extract_config('pipeline_config.yml')
    parquet_folder = pipeline_cfg['paths']['parquet_folder']
    os.makedirs(parquet_folder, exist_ok=True)

    model_cfg = cfg['model']
    data_cfg = cfg['data']
    out_cfg = cfg['output']
    dt_str = train_result['datetime']
    model_filename = train_result['model_filename']
    dataset_merge = train_result['dataset_merge']

    model_path = train_result['model_path']
    scaler_path = train_result['scaler_path']
    seq_length = data_cfg['seq_length']
    batch_size = cfg['evaluation'].get('eval_batch_size', 64)

    # Load scaler and model
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler not found: {scaler_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model weights not found: {model_path}")

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    model = build_model_from_config(seq_length, cfg)
    model.load_weights(model_path)

    # Get parquet files
    parquet_paths = [
        os.path.join(parquet_folder, fname)
        for fname in get_parquet_file_names()
        if os.path.exists(os.path.join(parquet_folder, fname))
    ]
    if not parquet_paths:
        raise ValueError("No parquet files found in directory.")

    # Create dataset
    dataset = create_data_loader(parquet_paths, scaler, seq_length, batch_size)

    # Calculate total sequences
    total_seqs = sum(
        max(0, len(pd.read_parquet(path, columns=['Close'])) - seq_length)
        for path in parquet_paths
    )
    if total_seqs == 0:
        raise ValueError("Not enough sequences for evaluation.")

    steps_total = (total_seqs + batch_size - 1) // batch_size
    steps_train = int(steps_total * data_cfg['train_ratio'])
    steps_val = int(steps_total * data_cfg['val_ratio'])
    steps_test = steps_total - steps_train - steps_val

    train_ds = dataset.take(steps_train)
    val_ds = dataset.skip(steps_train).take(steps_val)
    test_ds = dataset.skip(steps_train + steps_val)

    # Evaluate on all splits
    logger.info("Evaluate on training set")
    train_rmse, train_mae, train_mape = model_evaluate(model, scaler, train_ds)

    logger.info("Evaluate on validation set")
    val_rmse, val_mae, val_mape = model_evaluate(model, scaler, val_ds)
    
    logger.info("Evaluate on test set")
    test_rmse, test_mae, test_mape = model_evaluate(model, scaler, test_ds)

    # Save metrics to CSV
    metrics_path = os.path.join(out_cfg['metrics']['metrics_dir'], f"metrics_{dt_str}.csv")
    os.makedirs(out_cfg['metrics']['metrics_dir'], exist_ok=True)

    metrics_data = [
        [model_filename, dataset_merge, "Train", "RMSE", train_rmse],
        [model_filename, dataset_merge, "Train", "MAE", train_mae],
        [model_filename, dataset_merge, "Train", "MAPE", train_mape],
        [model_filename, dataset_merge, "Val", "RMSE", val_rmse],
        [model_filename, dataset_merge, "Val", "MAE", val_mae],
        [model_filename, dataset_merge, "Val", "MAPE", val_mape],
        [model_filename, dataset_merge, "Test", "RMSE", test_rmse],
        [model_filename, dataset_merge, "Test", "MAE", test_mae],
        [model_filename, dataset_merge, "Test", "MAPE", test_mape],
    ]

    metrics_df = pd.DataFrame(
        metrics_data,
        columns=['model_path', 'dataset_merge', 'Split', 'Metric', 'Value']
    )
    metrics_df.to_csv(metrics_path, index=False)

    # Predict next price using the last sequence
    last_chunk = None
    for path in reversed(parquet_paths):
        df = pd.read_parquet(path)
        if len(df) >= seq_length:
            last_chunk = df['Close'].values[-seq_length:].astype('float32').reshape(-1, 1)
            break

    if last_chunk is None:
        raise ValueError("Not enough recent data to make a prediction.")

    last_scaled = scaler.transform(last_chunk)
    next_scaled = model.predict(last_scaled.reshape(1, seq_length, 1), verbose=0)
    next_price = scaler.inverse_transform(next_scaled)[0][0]

    # Save prediction to text file
    pred_path = os.path.join(out_cfg['predictions']['pred_dir'], f"prediction_{dt_str}.txt")
    os.makedirs(os.path.dirname(pred_path), exist_ok=True)

    with open(pred_path, 'w') as f:
        f.write(f"Model Run: {dt_str}\n")
        f.write(f"Model File: {model_filename}\n")
        f.write(f"Dataset Merged: {dataset_merge}\n")
        f.write(f"Architecture: {model_cfg['architecture'].upper()}\n")
        f.write(f"Predicted Next Close: {next_price:.6f}\n")
        f.write(f"Based on last {seq_length} timesteps.\n\n")
        f.write("Evaluation Metrics:\n")
        f.write(f"  Train  -> RMSE: {train_rmse:8.6f} | MAE: {train_mae:8.6f} | MAPE: {train_mape:8.6f}\n")
        f.write(f"  Val    -> RMSE: {val_rmse:8.6f} | MAE: {val_mae:8.6f} | MAPE: {val_mape:8.6f}\n")
        f.write(f"  Test   -> RMSE: {test_rmse:8.6f} | MAE: {test_mae:8.6f} | MAPE: {test_mape:8.6f}\n")

    logger.info(f"Next price: {next_price:.4f} | Test RMSE: {test_rmse:.6f} | Dataset: {dataset_merge}")

    return {
        'metrics_path': metrics_path,
        'prediction_path': pred_path,
        'next_price': float(next_price)
    }


if __name__ == "__main__":
    logger.info("Running standalone evaluation test")

    run_dt = "2025-10-28-11-33-51-(+07)"  # CHANGE IF NEEDED

    cfg = load_extract_config('model_config.yml')
    out_cfg = cfg['output']

    mock_train_result = {
        "model_path": os.path.join(out_cfg["checkpoints"]["model_dir"], f"model_{run_dt}.h5"),
        "model_filename": f"model_{run_dt}.h5",
        "scaler_path": os.path.join(out_cfg["checkpoints"]["scaler_dir"], f"scaler_{run_dt}.pkl"),
        "datetime": run_dt,
        "dataset_merge": "BTCUSDT-1s-2025-08 + BTCUSDT-1s-2025-09"
    }

    # Verify files exist
    missing = []
    for key in ["model_path", "scaler_path"]:
        path = mock_train_result[key]
        if not os.path.exists(path):
            missing.append(path)

    if missing:
        logger.error("Missing files:\n" + "\n".join(missing))
        logger.error("Make sure you have run training with the same timestamp.")
        raise FileNotFoundError("Required model/scaler files not found.")

    # Run evaluation
    try:
        result = metric_and_predict_lstm_model(mock_train_result)
        logger.info("Evaluation completed successfully!")
        logger.info(f"Results: {result}")
    except Exception as e:
        logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
    finally:
        logger.info("Standalone evaluation run completed")