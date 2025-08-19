"""
市场数据收集器
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

from utils.logging_manager import LoggerMixin
from config.exchange_config import ExchangeConfig

class MarketDataCollector(LoggerMixin):
    """市场数据收集器"""
    
    def __init__(self):
        """初始化市场数据收集器"""
        self.exchanges = {}
        self.rate_limits = {}
        self.last_request_time = {}
        
    def initialize_exchange(self, exchange_name: str) -> bool:
        """
        初始化交易所连接
        
        Args:
            exchange_name: 交易所名称
            
        Returns:
            是否初始化成功
        """
        try:
            if exchange_name not in ExchangeConfig.SUPPORTED_EXCHANGES:
                self.logger.error(f"❌ 不支持的交易所: {exchange_name}")
                return False
            
            # 获取交易所配置
            config = ExchangeConfig.get_exchange_config(exchange_name)
            
            # 创建交易所实例
            exchange_class = getattr(ccxt, exchange_name)
            exchange = exchange_class({
                'apiKey': config['api_key'],
                'secret': config['secret_key'],
                'password': config.get('passphrase', ''),
                'sandbox': config['sandbox'],
                'enableRateLimit': True,
                'timeout': config['timeout'] * 1000
            })
            
            self.exchanges[exchange_name] = exchange
            self.rate_limits[exchange_name] = config['rate_limit']
            self.last_request_time[exchange_name] = 0
            
            self.logger.info(f"✅ 交易所 {exchange_name} 初始化成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 初始化交易所 {exchange_name} 失败: {e}")
            return False
    
    def _respect_rate_limit(self, exchange_name: str):
        """遵守速率限制"""
        if exchange_name in self.rate_limits:
            rate_limit = self.rate_limits[exchange_name]
            min_interval = 60.0 / rate_limit  # 每分钟请求数转换为间隔
            
            current_time = time.time()
            time_since_last = current_time - self.last_request_time.get(exchange_name, 0)
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time[exchange_name] = time.time()
    
    def fetch_ohlcv(self, exchange_name: str, symbol: str, 
                    timeframe: str = '1h', limit: int = 1000) -> Optional[pd.DataFrame]:
        """
        获取OHLCV数据
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            timeframe: 时间框架
            limit: 数据条数限制
            
        Returns:
            OHLCV数据
        """
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            # 遵守速率限制
            self._respect_rate_limit(exchange_name)
            
            exchange = self.exchanges[exchange_name]
            
            # 获取OHLCV数据
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            if not ohlcv:
                self.logger.warning(f"⚠️ 未获取到 {exchange_name} {symbol} 的数据")
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            self.logger.info(f"✅ 获取了 {len(df)} 条 {exchange_name} {symbol} 数据")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} {symbol} 数据失败: {e}")
            return None
    
    def fetch_ticker(self, exchange_name: str, symbol: str) -> Optional[Dict[str, Any]]:
        """
        获取当前价格信息
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            
        Returns:
            价格信息
        """
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            # 遵守速率限制
            self._respect_rate_limit(exchange_name)
            
            exchange = self.exchanges[exchange_name]
            ticker = exchange.fetch_ticker(symbol)
            
            return {
                'symbol': symbol,
                'exchange': exchange_name,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['baseVolume'],
                'timestamp': datetime.now().isoformat()
            }

        except ccxt.AuthenticationError as e:
            self.logger.error(f"❌ {exchange_name} 认证失败 (API Key可能无效或权限不足): {e}")
            return None
        except ccxt.NetworkError as e:
            self.logger.error(f"❌ {exchange_name} 网络错误: {e}")
            return None
        except ccxt.ExchangeError as e:
            self.logger.error(f"❌ {exchange_name} 交易所错误 (可能是交易对不支持): {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} {symbol} 价格信息时发生未知错误: {e}")
            return None
    
    def fetch_order_book(self, exchange_name: str, symbol: str, 
                        limit: int = 20) -> Optional[Dict[str, Any]]:
        """
        获取订单簿
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            limit: 深度限制
            
        Returns:
            订单簿数据
        """
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            # 遵守速率限制
            self._respect_rate_limit(exchange_name)
            
            exchange = self.exchanges[exchange_name]
            order_book = exchange.fetch_order_book(symbol, limit)
            
            return {
                'symbol': symbol,
                'exchange': exchange_name,
                'bids': order_book['bids'],
                'asks': order_book['asks'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} {symbol} 订单簿失败: {e}")
            return None
    
    def fetch_recent_trades(self, exchange_name: str, symbol: str, 
                           limit: int = 100) -> Optional[List[Dict[str, Any]]]:
        """
        获取最近交易
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            limit: 交易数量限制
            
        Returns:
            最近交易列表
        """
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            # 遵守速率限制
            self._respect_rate_limit(exchange_name)
            
            exchange = self.exchanges[exchange_name]
            trades = exchange.fetch_trades(symbol, limit=limit)
            
            formatted_trades = []
            for trade in trades:
                formatted_trades.append({
                    'id': trade['id'],
                    'timestamp': datetime.fromtimestamp(trade['timestamp'] / 1000).isoformat(),
                    'price': trade['price'],
                    'amount': trade['amount'],
                    'side': trade['side'],
                    'cost': trade['cost']
                })
            
            return formatted_trades
            
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} {symbol} 最近交易失败: {e}")
            return None
    
    def get_market_data(self, exchange_name: str, symbol: str, 
                       timeframe: str = '1h', days: int = 30) -> Optional[Dict[str, Any]]:
        """
        获取完整的市场数据
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            timeframe: 时间框架
            days: 天数
            
        Returns:
            市场数据
        """
        try:
            # 获取OHLCV数据
            ohlcv_data = self.fetch_ohlcv(exchange_name, symbol, timeframe)
            if ohlcv_data is None:
                return None
            
            # 获取当前价格信息
            ticker_data = self.fetch_ticker(exchange_name, symbol)
            
            # 获取订单簿
            order_book_data = self.fetch_order_book(exchange_name, symbol)
            
            # 获取最近交易
            trades_data = self.fetch_recent_trades(exchange_name, symbol)
            
            market_data = {
                'exchange': exchange_name,
                'symbol': symbol,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'ohlcv': ohlcv_data.to_dict('records') if ohlcv_data is not None else [],
                'ticker': ticker_data,
                'order_book': order_book_data,
                'recent_trades': trades_data
            }
            
            self.logger.info(f"✅ 获取了 {exchange_name} {symbol} 的完整市场数据")
            return market_data
            
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} {symbol} 市场数据失败: {e}")
            return None
    
    def get_exchange_info(self, exchange_name: str) -> Optional[Dict[str, Any]]:
        """
        获取交易所信息
        
        Args:
            exchange_name: 交易所名称
            
        Returns:
            交易所信息
        """
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            exchange = self.exchanges[exchange_name]
            markets = exchange.load_markets()
            
            return {
                'exchange': exchange_name,
                'markets': list(markets.keys()),
                'supported_symbols': ExchangeConfig.get_trading_pairs(exchange_name),
                'timeframes': ExchangeConfig.get_timeframes()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取 {exchange_name} 交易所信息失败: {e}")
            return None
    
    def cleanup(self):
        """清理资源"""
        for exchange_name, exchange in self.exchanges.items():
            try:
                exchange.close()
                self.logger.info(f"✅ 关闭 {exchange_name} 连接")
            except Exception as e:
                self.logger.warning(f"⚠️ 关闭 {exchange_name} 连接时出错: {e}")
        
        self.exchanges.clear()
        self.rate_limits.clear()
        self.last_request_time.clear() 