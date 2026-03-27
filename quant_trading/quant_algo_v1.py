import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings

# Suppress yfinance warnings for clean output
warnings.filterwarnings('ignore')

# 1. Configuration
TICKERS = ['NVDA', 'AMD', 'TSM', 'ARM', 'GOOGL', 'MSFT', 'SMH']
START_DATE = '2021-01-01'
# End date is today automatically by yfinance
TRAIN_TEST_SPLIT = 0.8 # Train on 80% of data, backtest on recent 20%

def add_indicators(df):
    """Calculate technical indicators for the ML model to learn from."""
    close = df['Close']
    
    # 1. Simple Moving Averages (Trend)
    df['SMA_20'] = close.rolling(window=20).mean()
    df['SMA_50'] = close.rolling(window=50).mean()
    
    # 2. RSI - Relative Strength Index (Momentum)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # 3. MACD (Trend Momentum)
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    df['MACD'] = macd
    df['MACD_Signal'] = macd.ewm(span=9, adjust=False).mean()
    
    # 4. Bollinger Bands (Volatility)
    bb_middle = close.rolling(window=20).mean()
    bb_std = close.rolling(window=20).std()
    df['BB_Middle'] = bb_middle
    df['BB_Upper'] = bb_middle + 2 * bb_std
    df['BB_Lower'] = bb_middle - 2 * bb_std
    
    # 5. Price Rate of Change
    df['ROC_5'] = close.pct_change(periods=5)
    
    # Drop rows with NaN values created by rolling windows
    df = df.dropna()
    return df

def prepare_data(df):
    """Define the Target (Y) and Features (X)"""
    close = df['Close']
    volume = df['Volume']
    
    # Target: 1 if tomorrow's Close is higher than today's Close, else 0
    target = np.where(close.shift(-1) > close, 1, 0)
    
    # Features to train on
    features_df = pd.DataFrame({
        'SMA_20': df['SMA_20'],
        'SMA_50': df['SMA_50'],
        'RSI_14': df['RSI_14'],
        'MACD': df['MACD'],
        'MACD_Signal': df['MACD_Signal'],
        'BB_Upper': df['BB_Upper'],
        'BB_Lower': df['BB_Lower'],
        'ROC_5': df['ROC_5'],
        'Volume': volume
    }, index=df.index)
    
    # We must drop the last row because we don't know "tomorrow's" price yet for training
    X = features_df[:-1]
    y = target[:-1]
    
    # The absolute latest day's data (used for predicting tomorrow)
    latest_data = features_df.iloc[-1:]
    latest_close = close.iloc[-1]
    
    return X, y, latest_data, latest_close, close

print("==========================================================")
print(" QUANT ALGORITHM v1.0: AI INFRASTRUCTURE & SEMICONDUCTORS")
print(" Model: Random Forest Classifier (Daily Timeframe)")
print("==========================================================")

total_hypothetical_profit = 0

for ticker in TICKERS:
    try:
        # Download Data
        data = yf.download(ticker, start=START_DATE, progress=False)
        if data.empty:
            continue
        
        # Flatten multi-index columns if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values('Price')
            
        # Feature Engineering
        df = add_indicators(data)
        X, y, latest_x, latest_price, full_df = prepare_data(df)
        
        # Train/Test Split
        split_idx = int(len(X) * TRAIN_TEST_SPLIT)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        test_dates = full_df.index[split_idx:-1]
        
        # Train the Machine Learning Model
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)
        
        # ----------------------------------------------------
        # BACKTESTING (回測)
        # ----------------------------------------------------
        predictions = model.predict(X_test)
        
        # Calculate Backtest Yield
        # If model predicts 1 (Up), we hold the stock for 1 day and get the daily return
        test_returns = full_df['Close'].pct_change().shift(-1)[split_idx:-1]
        strategy_returns = predictions * test_returns
        
        # Cumulative return (Compound growth)
        cumulative_strategy_return = (1 + strategy_returns).prod() - 1
        buy_and_hold_return = (1 + test_returns).prod() - 1
        
        # Evaluate model accuracy
        accuracy = accuracy_score(y_test, predictions)
        
        # ----------------------------------------------------
        # PREDICT TOMORROW
        # ----------------------------------------------------
        # Use the trained model on today's closing data to predict tomorrow
        prediction_prob = model.predict_proba(latest_x)[0]
        prob_up = prediction_prob[1] * 100
        
        signal = "BUY/CALL" if prob_up > 55 else "SELL/PUT" if prob_up < 45 else "HOLD"
        
        print(f"\n[{ticker}] Last Close: ${latest_price:.2f}")
        print(f"  -> Backtest Model Accuracy:  {accuracy*100:.1f}%")
        print(f"  -> Backtest Strategy Yield: {cumulative_strategy_return*100:>6.1f}% (vs Buy&Hold: {buy_and_hold_return*100:.1f}%)")
        print(f"  -> Prediction for Tomorrow: {prob_up:.1f}% probability of going UP.")
        print(f"  -> ACTION SIGNAL:           {signal}")
        
    except Exception as e:
        print(f"[{ticker}] Error: {str(e)}")

print("\n==========================================================")
print(" Note: The backtest assumes buying at today's close and")
print(" selling at tomorrow's close based on the model's signal.")
print("==========================================================")
