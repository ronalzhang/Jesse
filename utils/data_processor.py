"""
数据处理工具
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
# import talib  # 替换为finta
from finta import TA
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
        添加技术指标
        
        Args:
            df: 数据框
            
        Returns:
            添加技术指标后的数据框
        """
        self.logger.info("📊 添加技术指标...")
        
        df_indicators = df.copy()
        
        # 确保有必要的列
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df_indicators.columns:
                self.logger.warning(f"缺少必要列: {col}")
                return df_indicators
        
        try:
            # 使用finta计算技术指标
            # 移动平均线
            df_indicators['sma_5'] = TA.SMA(df_indicators, 5)
            df_indicators['sma_20'] = TA.SMA(df_indicators, 20)
            df_indicators['ema_12'] = TA.EMA(df_indicators, 12)
            df_indicators['ema_26'] = TA.EMA(df_indicators, 26)
            
            # MACD
            macd_data = TA.MACD(df_indicators)
            if isinstance(macd_data, pd.DataFrame):
                df_indicators['macd'] = macd_data['MACD']
                df_indicators['macd_signal'] = macd_data['MACD_signal']
                df_indicators['macd_hist'] = macd_data['MACD_hist']
            else:
                # 如果返回的是Series，尝试分别计算
                df_indicators['macd'] = macd_data
            
            # RSI
            df_indicators['rsi'] = TA.RSI(df_indicators, 14)
            
            # 布林带
            bb_data = TA.BBANDS(df_indicators)
            if isinstance(bb_data, pd.DataFrame):
                df_indicators['bb_upper'] = bb_data['BB_UPPER']
                df_indicators['bb_middle'] = bb_data['BB_MIDDLE']
                df_indicators['bb_lower'] = bb_data['BB_LOWER']
            
            # 随机指标
            stoch_data = TA.STOCH(df_indicators)
            if isinstance(stoch_data, pd.DataFrame):
                df_indicators['stoch_k'] = stoch_data['STOCH_K']
                df_indicators['stoch_d'] = stoch_data['STOCH_D']
            
            # ATR (平均真实波幅)
            df_indicators['atr'] = TA.ATR(df_indicators, 14)
            
            # 成交量指标
            df_indicators['obv'] = TA.OBV(df_indicators)
            
        except Exception as e:
            self.logger.warning(f"计算技术指标时出错: {e}")
            # 如果finta计算失败，使用pandas原生方法作为备选
            self._add_fallback_indicators(df_indicators)
        
        # 价格变化率
        df_indicators['price_change'] = df_indicators['close'].pct_change()
        df_indicators['price_change_5'] = df_indicators['close'].pct_change(periods=5)
        
        # 波动率
        df_indicators['volatility'] = df_indicators['price_change'].rolling(window=20).std()
        
        self.logger.info("✅ 技术指标添加完成")
        return df_indicators
    
    def _add_fallback_indicators(self, df: pd.DataFrame) -> None:
        """添加备选技术指标（当finta失败时使用）"""
        try:
            # 简单的移动平均线
            df['sma_5'] = df['close'].rolling(window=5).mean()
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['ema_12'] = df['close'].ewm(span=12).mean()
            df['ema_26'] = df['close'].ewm(span=26).mean()
            
            # 简单的RSI计算
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # 简单的布林带
            df['bb_middle'] = df['close'].rolling(window=20).mean()
            bb_std = df['close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            self.logger.info("使用备选技术指标计算方法")
            
        except Exception as e:
            self.logger.error(f"备选技术指标计算也失败: {e}")
    
    def normalize_data(self, df: pd.DataFrame, method: str = 'minmax') -> Tuple[pd.DataFrame, Dict]:
        """
        数据标准化
        
        Args:
            df: 数据框
            method: 标准化方法 ('minmax', 'standard', 'robust')
            
        Returns:
            标准化后的数据框和缩放器信息
        """
        self.logger.info(f"📏 使用 {method} 方法进行数据标准化...")
        
        df_normalized = df.copy()
        scaler_info = {}
        
        # 选择缩放器
        if method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'standard':
            scaler = StandardScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError(f"不支持的标准化方法: {method}")
        
        # 标准化数值列
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        feature_columns = [col for col in numeric_columns if col != self.target_column]
        
        if len(feature_columns) > 0:
            # 拟合缩放器
            df_normalized[feature_columns] = scaler.fit_transform(df[feature_columns])
            
            # 保存缩放器信息
            scaler_info = {
                'method': method,
                'scaler': scaler,
                'feature_columns': feature_columns
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
        self.logger.info(f"🔄 创建长度为 {sequence_length} 的时间序列...")
        
        # 获取特征列
        feature_columns = [col for col in df.columns if col != self.target_column]
        
        if len(feature_columns) == 0:
            raise ValueError("没有找到特征列")
        
        X, y = [], []
        
        for i in range(sequence_length, len(df)):
            # 特征序列
            X.append(df[feature_columns].iloc[i-sequence_length:i].values)
            # 目标值
            y.append(df[self.target_column].iloc[i])
        
        X = np.array(X)
        y = np.array(y)
        
        self.logger.info(f"✅ 创建了 {len(X)} 个序列，特征形状: {X.shape}")
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
        
        # 首先分割出训练集
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=(1-train_split), shuffle=False
        )
        
        # 从剩余数据中分割验证集和测试集
        test_split = 1 - validation_split / (1 - train_split)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=test_split, shuffle=False
        )
        
        self.logger.info(f"✅ 数据集分割完成 - 训练: {len(X_train)}, 验证: {len(X_val)}, 测试: {len(X_test)}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def inverse_transform(self, data: np.ndarray, scaler_info: Dict) -> np.ndarray:
        """
        反向转换数据
        
        Args:
            data: 标准化后的数据
            scaler_info: 缩放器信息
            
        Returns:
            原始尺度的数据
        """
        if 'scaler' in scaler_info:
            scaler = scaler_info['scaler']
            return scaler.inverse_transform(data)
        return data 