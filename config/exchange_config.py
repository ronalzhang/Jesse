"""
交易所配置文件
"""

import os
from typing import Dict, Any

class ExchangeConfig:
    """交易所配置类"""
    
    # 支持的交易所列表 - 高频交易专用
    SUPPORTED_EXCHANGES = [
        'binance', 'okx', 'bitget'
    ]
    
    # 交易所API配置 - 高频交易专用
    EXCHANGE_CONFIGS = {
        'binance': {
            'api_key': os.getenv('BINANCE_API_KEY', ''),
            'secret_key': os.getenv('BINANCE_SECRET_KEY', ''),
            'sandbox': os.getenv('BINANCE_SANDBOX', 'false').lower() == 'true',
            'rate_limit': 1200,  # 每分钟请求限制
            'timeout': 30
        },
        'okx': {
            'api_key': os.getenv('OKX_API_KEY', ''),
            'secret_key': os.getenv('OKX_SECRET_KEY', ''),
            'passphrase': os.getenv('OKX_PASSPHRASE', ''),
            'sandbox': os.getenv('OKX_SANDBOX', 'false').lower() == 'true',
            'rate_limit': 600,
            'timeout': 30
        },
        'bitget': {
            'api_key': os.getenv('BITGET_API_KEY', ''),
            'secret_key': os.getenv('BITGET_SECRET_KEY', ''),
            'passphrase': os.getenv('BITGET_PASSPHRASE', ''),
            'sandbox': os.getenv('BITGET_SANDBOX', 'false').lower() == 'true',
            'rate_limit': 600,
            'timeout': 30
        }
    }
    
    # 交易对配置 - 高频交易专用
    TRADING_PAIRS = {
        'binance': ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT'],
        'okx': ['BTC/USDT', 'ETH/USDT', 'OKB/USDT', 'SOL/USDT'],
        'bitget': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
    }
    
    # 时间框架配置 - 高频交易专用
    TIMEFRAMES = ['1m', '5m', '15m', '1h']
    
    # 高频交易时间框架
    HIGH_FREQ_TIMEFRAMES = ['1m', '5m', '15m']
    SCALPING_TIMEFRAMES = ['1m', '5m']
    ARBITRAGE_TIMEFRAMES = ['1m', '5m']
    
    @classmethod
    def get_exchange_config(cls, exchange: str) -> Dict[str, Any]:
        """获取指定交易所的配置"""
        if exchange not in cls.EXCHANGE_CONFIGS:
            raise ValueError(f"不支持的交易所: {exchange}")
        return cls.EXCHANGE_CONFIGS[exchange].copy()
    
    @classmethod
    def get_trading_pairs(cls, exchange: str) -> list:
        """获取指定交易所的交易对"""
        return cls.TRADING_PAIRS.get(exchange, [])
    
    @classmethod
    def get_supported_exchanges(cls) -> list:
        """获取支持的交易所列表"""
        return cls.SUPPORTED_EXCHANGES.copy()
    
    @classmethod
    def get_timeframes(cls) -> list:
        """获取支持的时间框架"""
        return cls.TIMEFRAMES.copy() 