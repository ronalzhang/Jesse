"""
多时间框架数据采集器
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

class MultiTimeframeCollector:
    """多时间框架数据采集器"""
    
    def __init__(self, base_collector):
        """
        初始化
        
        Args:
            base_collector: 基础市场数据采集器实例
        """
        self.base_collector = base_collector
        self.timeframes = ['1m', '3m', '5m', '15m', '1h', '4h', '1d']
        self.cache = {}
        
        # 缓存过期时间（秒）
        self.cache_expiry = {
            '1m': 60,
            '3m': 180,
            '5m': 300,
            '15m': 900,
            '1h': 3600,
            '4h': 14400,
            '1d': 86400
        }
        
        # 数据条数限制
        self.limits = {
            '1m': 100,
            '3m': 100,
            '5m': 100,
            '15m': 100,
            '1h': 100,
            '4h': 100,
            '1d': 100
        }
    
    def _get_cache_key(self, exchange: str, symbol: str, timeframe: str) -> str:
        """生成缓存键"""
        return f"{exchange}_{symbol}_{timeframe}"
    
    def _is_cache_valid(self, exchange: str, symbol: str, timeframe: str) -> bool:
        """检查缓存是否有效"""
        cache_key = self._get_cache_key(exchange, symbol, timeframe)
        
        if cache_key not in self.cache:
            return False
        
        cache_data = self.cache[cache_key]
        cache_time = cache_data.get('timestamp', 0)
        expiry_time = self.cache_expiry.get(timeframe, 300)
        
        return (time.time() - cache_time) < expiry_time
    
    def _get_from_cache(self, exchange: str, symbol: str, timeframe: str) -> Dict:
        """从缓存获取数据"""
        cache_key = self._get_cache_key(exchange, symbol, timeframe)
        return self.cache[cache_key]['data']
    
    def _fetch_and_cache(self, exchange: str, symbol: str, timeframe: str) -> Dict:
        """获取数据并缓存"""
        try:
            # 获取OHLCV数据
            limit = self.limits.get(timeframe, 100)
            df = self.base_collector.fetch_ohlcv(exchange, symbol, timeframe, limit)
            
            if df is None or len(df) < 50:
                return {}
            
            # 计算技术指标
            from utils.technical_indicators import TechnicalIndicators
            indicators = TechnicalIndicators.calculate_all_indicators(df)
            
            # 构建数据
            data = {
                'ohlcv': df.tail(10).to_dict('records'),  # 只保留最近10根用于展示
                'indicators': indicators,
                'data_points': len(df),
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat()
            }
            
            # 缓存数据
            cache_key = self._get_cache_key(exchange, symbol, timeframe)
            self.cache[cache_key] = {
                'data': data,
                'timestamp': time.time()
            }
            
            return data
            
        except Exception as e:
            print(f"获取 {exchange} {symbol} {timeframe} 数据失败: {e}")
            return {}
    
    def get_multi_timeframe_data(self, exchange: str, symbol: str, 
                                 timeframes: Optional[List[str]] = None) -> Dict:
        """
        获取多时间框架数据
        
        Args:
            exchange: 交易所名称
            symbol: 交易对
            timeframes: 时间框架列表，默认使用全部
            
        Returns:
            多时间框架数据字典
        """
        if timeframes is None:
            timeframes = self.timeframes
        
        result = {}
        
        for tf in timeframes:
            if tf not in self.timeframes:
                continue
            
            # 检查缓存
            if self._is_cache_valid(exchange, symbol, tf):
                result[tf] = self._get_from_cache(exchange, symbol, tf)
            else:
                result[tf] = self._fetch_and_cache(exchange, symbol, tf)
        
        return result
    
    def clear_cache(self, exchange: Optional[str] = None, 
                   symbol: Optional[str] = None):
        """清除缓存"""
        if exchange is None and symbol is None:
            self.cache.clear()
        else:
            keys_to_remove = []
            for key in self.cache.keys():
                if exchange and not key.startswith(exchange):
                    continue
                if symbol and symbol not in key:
                    continue
                keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.cache[key]
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        return {
            'total_cached': len(self.cache),
            'cache_keys': list(self.cache.keys()),
            'memory_usage': sum(len(str(v)) for v in self.cache.values())
        }
