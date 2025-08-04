"""
AI模型配置文件
"""

import os
from typing import Dict, Any

class AIConfig:
    """AI配置类"""
    
    # LSTM模型配置
    LSTM_CONFIG = {
        'sequence_length': 60,
        'hidden_layers': [128, 64, 32],
        'dropout_rate': 0.2,
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 100,
        'validation_split': 0.2
    }
    
    # Transformer模型配置
    TRANSFORMER_CONFIG = {
        'd_model': 512,
        'n_heads': 8,
        'n_layers': 6,
        'd_ff': 2048,
        'dropout': 0.1,
        'max_sequence_length': 100,
        'learning_rate': 0.0001,
        'batch_size': 16,
        'epochs': 50
    }
    
    # GARCH模型配置
    GARCH_CONFIG = {
        'p': 1,
        'q': 1,
        'vol': 'GARCH',
        'dist': 'normal'
    }
    
    # 强化学习配置
    RL_CONFIG = {
        'algorithm': 'PPO',
        'learning_rate': 0.0003,
        'batch_size': 64,
        'n_steps': 2048,
        'gamma': 0.99,
        'gae_lambda': 0.95,
        'clip_range': 0.2,
        'ent_coef': 0.01,
        'vf_coef': 0.5,
        'max_grad_norm': 0.5
    }
    
    # 遗传算法配置
    GA_CONFIG = {
        'population_size': 100,
        'generations': 50,
        'mutation_rate': 0.1,
        'crossover_rate': 0.8,
        'elite_size': 10
    }
    
    # 情感分析配置
    SENTIMENT_CONFIG = {
        'model_name': 'vader',
        'threshold': 0.1,
        'window_size': 24,  # 小时
        'update_frequency': 3600  # 秒
    }
    
    # 模型存储路径
    MODEL_PATHS = {
        'lstm': 'models/lstm/',
        'transformer': 'models/transformer/',
        'garch': 'models/garch/',
        'rl': 'models/rl/',
        'sentiment': 'models/sentiment/'
    }
    
    # 数据预处理配置
    DATA_CONFIG = {
        'min_data_points': 1000,
        'train_split': 0.7,
        'validation_split': 0.15,
        'test_split': 0.15,
        'normalization': 'minmax',  # minmax, standard, robust
        'feature_columns': ['open', 'high', 'low', 'close', 'volume'],
        'target_column': 'close'
    }
    
    # 预测配置
    PREDICTION_CONFIG = {
        'horizon': 24,  # 预测未来24个时间点
        'confidence_level': 0.95,
        'ensemble_method': 'weighted_average',
        'update_frequency': 300  # 5分钟更新一次
    }
    
    @classmethod
    def get_lstm_config(cls) -> Dict[str, Any]:
        """获取LSTM模型配置"""
        return cls.LSTM_CONFIG.copy()
    
    @classmethod
    def get_transformer_config(cls) -> Dict[str, Any]:
        """获取Transformer模型配置"""
        return cls.TRANSFORMER_CONFIG.copy()
    
    @classmethod
    def get_garch_config(cls) -> Dict[str, Any]:
        """获取GARCH模型配置"""
        return cls.GARCH_CONFIG.copy()
    
    @classmethod
    def get_rl_config(cls) -> Dict[str, Any]:
        """获取强化学习配置"""
        return cls.RL_CONFIG.copy()
    
    @classmethod
    def get_ga_config(cls) -> Dict[str, Any]:
        """获取遗传算法配置"""
        return cls.GA_CONFIG.copy()
    
    @classmethod
    def get_sentiment_config(cls) -> Dict[str, Any]:
        """获取情感分析配置"""
        return cls.SENTIMENT_CONFIG.copy()
    
    @classmethod
    def get_model_paths(cls) -> Dict[str, str]:
        """获取模型存储路径"""
        return cls.MODEL_PATHS.copy()
    
    @classmethod
    def get_data_config(cls) -> Dict[str, Any]:
        """获取数据预处理配置"""
        return cls.DATA_CONFIG.copy()
    
    @classmethod
    def get_prediction_config(cls) -> Dict[str, Any]:
        """获取预测配置"""
        return cls.PREDICTION_CONFIG.copy() 