import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Download S&P 500 data from Yahoo Finance
sp500_data = yf.download('^GSPC', start='2010-01-01', end='2022-01-01')

# Preprocess the data
sp500_data['Returns'] = sp500_data['Close'].pct_change()  # Calculate daily returns
sp500_data.dropna(inplace=True)  # Drop rows with missing values

# Define features and target variable
features = ['Open', 'High', 'Low', 'Close', 'Volume']  # Example features
X = sp500_data[features]
y = sp500_data['Returns']

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
