"""
数据库配置文件
"""

import os
from typing import Dict, Any

class DatabaseConfig:
    """数据库配置类"""
    
    # Redis配置
    REDIS_CONFIG = {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', 6379)),
        'db': int(os.getenv('REDIS_DB', 0)),
        'password': os.getenv('REDIS_PASSWORD', None),
        'decode_responses': True
    }
    
    # MongoDB配置
    MONGODB_CONFIG = {
        'host': os.getenv('MONGODB_HOST', 'localhost'),
        'port': int(os.getenv('MONGODB_PORT', 27017)),
        'database': os.getenv('MONGODB_DATABASE', 'jesse_plus'),
        'username': os.getenv('MONGODB_USERNAME', None),
        'password': os.getenv('MONGODB_PASSWORD', None)
    }
    
    # 数据库集合名称
    COLLECTIONS = {
        'market_data': 'market_data',
        'trading_signals': 'trading_signals',
        'ai_models': 'ai_models',
        'strategies': 'strategies',
        'performance': 'performance',
        'logs': 'logs'
    }
    
    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """获取Redis配置"""
        return cls.REDIS_CONFIG.copy()
    
    @classmethod
    def get_mongodb_config(cls) -> Dict[str, Any]:
        """获取MongoDB配置"""
        return cls.MONGODB_CONFIG.copy()
    
    @classmethod
    def get_collections(cls) -> Dict[str, str]:
        """获取集合配置"""
        return cls.COLLECTIONS.copy() 