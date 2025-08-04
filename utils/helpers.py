"""
辅助工具函数
"""

import os
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import numpy as np
import pandas as pd

def ensure_directory(path: str) -> None:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
    """
    Path(path).mkdir(parents=True, exist_ok=True)

def save_json(data: Dict, filepath: str) -> None:
    """
    保存JSON数据
    
    Args:
        data: 要保存的数据
        filepath: 文件路径
    """
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Dict:
    """
    加载JSON数据
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_pickle(data: Any, filepath: str) -> None:
    """
    保存pickle数据
    
    Args:
        data: 要保存的数据
        filepath: 文件路径
    """
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filepath: str) -> Any:
    """
    加载pickle数据
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def calculate_md5(data: str) -> str:
    """
    计算MD5哈希值
    
    Args:
        data: 要计算哈希的数据
        
    Returns:
        MD5哈希值
    """
    return hashlib.md5(data.encode()).hexdigest()

def format_timestamp(timestamp: Union[str, datetime]) -> str:
    """
    格式化时间戳
    
    Args:
        timestamp: 时间戳
        
    Returns:
        格式化的时间字符串
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def get_time_range(days: int = 30) -> tuple:
    """
    获取时间范围
    
    Args:
        days: 天数
        
    Returns:
        (开始时间, 结束时间)
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    return start_time, end_time

def calculate_returns(prices: List[float]) -> List[float]:
    """
    计算收益率
    
    Args:
        prices: 价格列表
        
    Returns:
        收益率列表
    """
    returns = []
    for i in range(1, len(prices)):
        returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    计算夏普比率
    
    Args:
        returns: 收益率列表
        risk_free_rate: 无风险利率
        
    Returns:
        夏普比率
    """
    if not returns:
        return 0.0
    
    returns_array = np.array(returns)
    excess_returns = returns_array - risk_free_rate / 252  # 日化无风险利率
    
    if np.std(excess_returns) == 0:
        return 0.0
    
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def calculate_max_drawdown(returns: List[float]) -> float:
    """
    计算最大回撤
    
    Args:
        returns: 收益率列表
        
    Returns:
        最大回撤
    """
    if not returns:
        return 0.0
    
    cumulative = np.cumprod(1 + np.array(returns))
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    return np.min(drawdown)

def calculate_volatility(returns: List[float]) -> float:
    """
    计算波动率
    
    Args:
        returns: 收益率列表
        
    Returns:
        年化波动率
    """
    if not returns:
        return 0.0
    
    return np.std(returns) * np.sqrt(252)

def normalize_data(data: np.ndarray, method: str = 'minmax') -> np.ndarray:
    """
    数据标准化
    
    Args:
        data: 数据数组
        method: 标准化方法
        
    Returns:
        标准化后的数据
    """
    if method == 'minmax':
        min_val = np.min(data)
        max_val = np.max(data)
        if max_val - min_val == 0:
            return np.zeros_like(data)
        return (data - min_val) / (max_val - min_val)
    elif method == 'zscore':
        mean_val = np.mean(data)
        std_val = np.std(data)
        if std_val == 0:
            return np.zeros_like(data)
        return (data - mean_val) / std_val
    else:
        raise ValueError(f"不支持的标准化方法: {method}")

def create_lagged_features(data: np.ndarray, lags: List[int]) -> np.ndarray:
    """
    创建滞后特征
    
    Args:
        data: 原始数据
        lags: 滞后期数列表
        
    Returns:
        包含滞后特征的数据
    """
    features = []
    for lag in lags:
        if lag > 0:
            lagged_data = np.roll(data, lag)
            lagged_data[:lag] = np.nan
            features.append(lagged_data)
    
    if features:
        return np.column_stack(features)
    return np.array([])

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算技术指标
    
    Args:
        df: 包含OHLCV数据的DataFrame
        
    Returns:
        添加技术指标的DataFrame
    """
    df_indicators = df.copy()
    
    # 移动平均线
    df_indicators['sma_5'] = df_indicators['close'].rolling(window=5).mean()
    df_indicators['sma_20'] = df_indicators['close'].rolling(window=20).mean()
    
    # 价格变化率
    df_indicators['price_change'] = df_indicators['close'].pct_change()
    df_indicators['price_change_5'] = df_indicators['close'].pct_change(periods=5)
    
    # 波动率
    df_indicators['volatility'] = df_indicators['price_change'].rolling(window=20).std()
    
    # RSI (简化版)
    delta = df_indicators['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df_indicators['rsi'] = 100 - (100 / (1 + rs))
    
    return df_indicators

def validate_config(config: Dict, required_keys: List[str]) -> bool:
    """
    验证配置字典
    
    Args:
        config: 配置字典
        required_keys: 必需的键列表
        
    Returns:
        是否有效
    """
    for key in required_keys:
        if key not in config or config[key] is None:
            return False
    return True

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    安全除法
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 默认值
        
    Returns:
        除法结果
    """
    if denominator == 0:
        return default
    return numerator / denominator

def format_number(number: float, decimals: int = 4) -> str:
    """
    格式化数字
    
    Args:
        number: 数字
        decimals: 小数位数
        
    Returns:
        格式化的字符串
    """
    return f"{number:.{decimals}f}"

def format_percentage(number: float, decimals: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        number: 数字
        decimals: 小数位数
        
    Returns:
        格式化的百分比字符串
    """
    return f"{number * 100:.{decimals}f}%" 