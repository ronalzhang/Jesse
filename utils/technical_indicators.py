"""技术指标计算模块"""
import pandas as pd
import numpy as np
from typing import Dict

class TechnicalIndicators:
    @staticmethod
    def calculate_ema(data: pd.Series, period: int) -> pd.Series:
        return data.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2.0):
        middle = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14):
        hl = high - low
        hc = np.abs(high - close.shift())
        lc = np.abs(low - close.shift())
        tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    @staticmethod
    def calculate_all_indicators(df: pd.DataFrame) -> Dict:
        if len(df) < 50:
            return {}
        indicators = {}
        try:
            indicators['current_price'] = float(df['close'].iloc[-1])
            indicators['ema20'] = float(TechnicalIndicators.calculate_ema(df['close'], 20).iloc[-1])
            if len(df) >= 50:
                indicators['ema50'] = float(TechnicalIndicators.calculate_ema(df['close'], 50).iloc[-1])
            macd, signal, hist = TechnicalIndicators.calculate_macd(df['close'])
            indicators['macd'] = float(macd.iloc[-1])
            indicators['macd_signal'] = float(signal.iloc[-1])
            indicators['rsi7'] = float(TechnicalIndicators.calculate_rsi(df['close'], 7).iloc[-1])
            indicators['rsi14'] = float(TechnicalIndicators.calculate_rsi(df['close'], 14).iloc[-1])
            upper, middle, lower = TechnicalIndicators.calculate_bollinger_bands(df['close'])
            indicators['bb_upper'] = float(upper.iloc[-1])
            indicators['bb_middle'] = float(middle.iloc[-1])
            indicators['bb_lower'] = float(lower.iloc[-1])
            indicators['atr14'] = float(TechnicalIndicators.calculate_atr(df['high'], df['low'], df['close'], 14).iloc[-1])
            indicators['volume'] = float(df['volume'].iloc[-1])
            indicators['volume_avg'] = float(df['volume'].rolling(window=20).mean().iloc[-1])
        except Exception as e:
            print(f"计算指标错误: {e}")
        return indicators
