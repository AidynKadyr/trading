# Trading Project

## Overview

This project is developed as part of a Machine Learning Engineer position and aims to create a pipeline for developing a trading model for Foreign Exchange (FX). The pipeline involves a series of steps, starting with the execution of `start.py`.

## Execution Flow

1. **Data Collection:**
   - The `start.py` script initiates the data collection process. It creates a dataset by concatenating macroeconomic data, technical indicators, and the latest available FX data from Interactive Brokers.

2. **Interactive Brokers API:**
   - The project utilizes the TWS platform to interact with Interactive Brokers API. This allows the retrieval of ticker information and the ability to place Buy/Sell orders at a paper trading account.

3. **Data Preprocessing:**
   - After creating the dataset, data preprocessing is performed to clean and format the data appropriately for model training.

4. **Feature Engineering:**
   - The pipeline includes a feature engineering step, where additional features are created or modified to enhance the model's predictive capabilities.

5. **Model Training (XGBoost):**
   - An XGBoost model is employed for training. The model is fitted using the preprocessed and engineered data.

6. **Trading Strategy:**
   - The trading strategy involves determining the order type by comparing the forecast value with the previous day's closing price.

## Usage

To run the pipeline, execute the following command:

```bash
python start.py
