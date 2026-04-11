# Options Momentum Strategy

## Core Logic
"Buy high, sell higher." Utilizes extreme momentum to capture nonlinear Gamma explosion in OTM options.

## Entry Signals
*   **RSI (14):** 60-70 (Strong momentum, not yet exhausted).
*   **Price Action:** Trading above 20-day SMA.
*   **MACD:** Positive histogram, crossover confirmed.
*   **Action:** Buy OTM Call (approx 5% out of the money, DTE ~30 days).

## Exit & Risk Management
1. **Initial Stop Loss:** Strict exit if price closes below the 20-day SMA.
2. **Trailing Stop:** Once profitable, trail stop behind the 10-day SMA or MACD histogram flip.
3. **Extreme Take Profit:** If RSI > 75 and price pierces the 3rd Standard Deviation Upper Bollinger Band, scale out 50% immediately to capture Vega/Gamma premium before reversion.
