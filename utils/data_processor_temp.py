"""
数据处理工具 - 临时版本（无TA-Lib依赖）
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
# import talib  # 暂时注释掉
from utils.logging_manager import LoggerMixin

class DataProcessor(LoggerMixin):
    """数据处理类"""
    
    def __init__(self):
        """初始化数据处理器"""
        self.scalers = {}
        self.feature_columns = ['open', 'high', 'low', 'close', 'volume']
        self.target_column = 'close'
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据
        
        Args:
            df: 原始数据框
            
        Returns:
            清洗后的数据框
        """
        self.logger.info("🧹 开始数据清洗...")
        
        # 复制数据避免修改原始数据
        df_clean = df.copy()
        
        # 移除重复行
        df_clean = df_clean.drop_duplicates()
        
        # 处理缺失值
        df_clean = self._handle_missing_values(df_clean)
        
        # 移除异常值
        df_clean = self._remove_outliers(df_clean)
        
        # 确保数据类型正确
        df_clean = self._ensure_data_types(df_clean)
        
        self.logger.info(f"✅ 数据清洗完成，保留 {len(df_clean)} 行数据")
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理缺失值"""
        # 对于价格数据，使用前向填充
        price_columns = ['open', 'high', 'low', 'close']
        df[price_columns] = df[price_columns].fillna(method='ffill')
        
        # 对于成交量，使用0填充
        if 'volume' in df.columns:
            df['volume'] = df['volume'].fillna(0)
        
        # 移除仍有缺失值的行
        df = df.dropna()
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """移除异常值"""
        # 使用IQR方法移除异常值
        for col in self.feature_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # 移除异常值
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        return df
    
    def _ensure_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """确保数据类型正确"""
        # 确保数值列为float类型
        for col in self.feature_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 确保时间列为datetime类型
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加技术指标 - 使用pandas内置函数替代TA-Lib
        
        Args:
            df: 原始数据框
            
        Returns:
            添加技术指标后的数据框
        """
        self.logger.info("📊 添加技术指标...")
        
        # 复制数据避免修改原始数据
        df_indicators = df.copy()
        
        # 使用pandas内置函数计算技术指标
        # 移动平均线
        df_indicators['sma_5'] = df_indicators['close'].rolling(window=5).mean()
        df_indicators['sma_20'] = df_indicators['close'].rolling(window=20).mean()
        df_indicators['ema_12'] = df_indicators['close'].ewm(span=12).mean()
        df_indicators['ema_26'] = df_indicators['close'].ewm(span=26).mean()
        
        # MACD
        ema12 = df_indicators['close'].ewm(span=12).mean()
        ema26 = df_indicators['close'].ewm(span=26).mean()
        df_indicators['macd'] = ema12 - ema26
        df_indicators['macd_signal'] = df_indicators['macd'].ewm(span=9).mean()
        df_indicators['macd_hist'] = df_indicators['macd'] - df_indicators['macd_signal']
        
        # RSI
        delta = df_indicators['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df_indicators['rsi'] = 100 - (100 / (1 + rs))
        
        # 布林带
        sma20 = df_indicators['close'].rolling(window=20).mean()
        std20 = df_indicators['close'].rolling(window=20).std()
        df_indicators['bb_upper'] = sma20 + (std20 * 2)
        df_indicators['bb_middle'] = sma20
        df_indicators['bb_lower'] = sma20 - (std20 * 2)
        
        # 随机指标
        low_min = df_indicators['low'].rolling(window=14).min()
        high_max = df_indicators['high'].rolling(window=14).max()
        df_indicators['stoch_k'] = 100 * ((df_indicators['close'] - low_min) / (high_max - low_min))
        df_indicators['stoch_d'] = df_indicators['stoch_k'].rolling(window=3).mean()
        
        # ATR (平均真实波幅)
        high_low = df_indicators['high'] - df_indicators['low']
        high_close = np.abs(df_indicators['high'] - df_indicators['close'].shift())
        low_close = np.abs(df_indicators['low'] - df_indicators['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df_indicators['atr'] = true_range.rolling(window=14).mean()
        
        # OBV (能量潮)
        df_indicators['obv'] = (np.sign(df_indicators['close'].diff()) * df_indicators['volume']).fillna(0).cumsum()
        
        # 移除包含NaN的行
        df_indicators = df_indicators.dropna()
        
        self.logger.info(f"✅ 技术指标添加完成，保留 {len(df_indicators)} 行数据")
        return df_indicators
    
    def normalize_data(self, df: pd.DataFrame, method: str = 'minmax') -> Tuple[pd.DataFrame, Dict]:
        """
        数据标准化
        
        Args:
            df: 原始数据框
            method: 标准化方法 ('minmax', 'standard', 'robust')
            
        Returns:
            标准化后的数据框和标准化信息
        """
        self.logger.info(f"📏 数据标准化 (方法: {method})...")
        
        # 复制数据避免修改原始数据
        df_normalized = df.copy()
        
        # 选择要标准化的列
        columns_to_normalize = [col for col in self.feature_columns if col in df.columns]
        
        # 根据方法选择标准化器
        if method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'standard':
            scaler = StandardScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"不支持的标准化方法: {method}")
        
        # 标准化数据
        df_normalized[columns_to_normalize] = scaler.fit_transform(df_normalized[columns_to_normalize])
        
        # 保存标准化信息
        scaler_info = {
            'method': method,
            'scaler': scaler,
            'columns': columns_to_normalize
        }
        
        self.logger.info("✅ 数据标准化完成")
        return df_normalized, scaler_info
    
    def create_sequences(self, df: pd.DataFrame, sequence_length: int = 60) -> Tuple[np.ndarray, np.ndarray]:
        """
        创建时间序列数据
        
        Args:
            df: 数据框
            sequence_length: 序列长度
            
        Returns:
            X: 特征序列
            y: 目标序列
        """
        self.logger.info(f"🔄 创建时间序列数据 (序列长度: {sequence_length})...")
        
        # 选择特征列
        feature_columns = [col for col in self.feature_columns if col in df.columns]
        
        # 创建序列
        X, y = [], []
        for i in range(sequence_length, len(df)):
            X.append(df[feature_columns].iloc[i-sequence_length:i].values)
            y.append(df[self.target_column].iloc[i])
        
        X = np.array(X)
        y = np.array(y)
        
        self.logger.info(f"✅ 时间序列数据创建完成: X.shape={X.shape}, y.shape={y.shape}")
        return X, y
    
    def split_data(self, X: np.ndarray, y: np.ndarray, 
                   train_split: float = 0.7, 
                   validation_split: float = 0.15) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        分割数据集
        
        Args:
            X: 特征数据
            y: 目标数据
            train_split: 训练集比例
            validation_split: 验证集比例
            
        Returns:
            训练集、验证集、测试集
        """
        self.logger.info("✂️ 分割数据集...")
        
        # 计算分割点
        train_size = int(len(X) * train_split)
        val_size = int(len(X) * validation_split)
        
        # 分割数据
        X_train = X[:train_size]
        y_train = y[:train_size]
        
        X_val = X[train_size:train_size + val_size]
        y_val = y[train_size:train_size + val_size]
        
        X_test = X[train_size + val_size:]
        y_test = y[train_size + val_size:]
        
        self.logger.info(f"✅ 数据集分割完成:")
        self.logger.info(f"   训练集: {X_train.shape[0]} 样本")
        self.logger.info(f"   验证集: {X_val.shape[0]} 样本")
        self.logger.info(f"   测试集: {X_test.shape[0]} 样本")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def inverse_transform(self, data: np.ndarray, scaler_info: Dict) -> np.ndarray:
        """
        反向转换标准化数据
        
        Args:
            data: 标准化后的数据
            scaler_info: 标准化信息
            
        Returns:
            原始尺度的数据
        """
        return scaler_info['scaler'].inverse_transform(data) 