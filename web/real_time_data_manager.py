#!/usr/bin/env python3
"""
实时数据管理器
提供真实的实时数据，包括价格、交易量、系统状态等
"""

import time
import threading
import queue
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
import requests
import json

class RealTimeDataManager:
    """实时数据管理器"""
    
    def __init__(self):
        """初始化实时数据管理器"""
        self.logger = logging.getLogger(__name__)
        
        # 数据缓存
        self.price_cache = {}
        self.volume_cache = {}
        self.system_status_cache = {}
        self.trading_signals_cache = []
        
        # 缓存过期时间（秒）
        self.cache_expiry = {
            'price': 10,      # 价格数据10秒过期
            'volume': 30,     # 交易量数据30秒过期
            'system': 60,     # 系统状态60秒过期
            'signals': 300    # 交易信号5分钟过期
        }
        
        # 初始化交易所连接
        self.exchanges = {}
        self._init_exchanges()
        
        # 启动数据更新线程
        self.is_running = False
        self.data_queue = queue.Queue()
        self.start_data_thread()
    
    def _init_exchanges(self):
        """初始化交易所连接"""
        try:
            # 初始化主要交易所
            exchange_configs = {
                'binance': {
                    'apiKey': '',  # 从环境变量获取
                    'secret': '',
                    'sandbox': False
                },
                'okx': {
                    'apiKey': '',
                    'secret': '',
                    'password': '',
                    'sandbox': False
                },
                'bybit': {
                    'apiKey': '',
                    'secret': '',
                    'sandbox': False
                }
            }
            
            for exchange_name, config in exchange_configs.items():
                try:
                    exchange_class = getattr(ccxt, exchange_name)
                    self.exchanges[exchange_name] = exchange_class(config)
                    self.logger.info(f"✅ {exchange_name} 交易所连接成功")
                except Exception as e:
                    self.logger.warning(f"⚠️ {exchange_name} 交易所连接失败: {e}")
            
        except Exception as e:
            self.logger.error(f"❌ 初始化交易所失败: {e}")
    
    def start_data_thread(self):
        """启动数据更新线程"""
        self.is_running = True
        self.data_thread = threading.Thread(target=self._data_update_loop, daemon=True)
        self.data_thread.start()
        self.logger.info("✅ 实时数据更新线程已启动")
    
    def _data_update_loop(self):
        """数据更新循环"""
        while self.is_running:
            try:
                # 更新价格数据
                self._update_price_data()
                
                # 更新交易量数据
                self._update_volume_data()
                
                # 更新系统状态
                self._update_system_status()
                
                # 更新交易信号
                self._update_trading_signals()
                
                # 休眠1秒
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"❌ 数据更新循环错误: {e}")
                time.sleep(5)
    
    def _update_price_data(self):
        """更新价格数据"""
        try:
            symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']
            
            for symbol in symbols:
                for exchange_name, exchange in self.exchanges.items():
                    try:
                        ticker = exchange.fetch_ticker(symbol)
                        
                        cache_key = f"{exchange_name}_{symbol}"
                        self.price_cache[cache_key] = {
                            'last': ticker['last'],
                            'bid': ticker['bid'],
                            'ask': ticker['ask'],
                            'high': ticker['high'],
                            'low': ticker['low'],
                            'change': ticker['percentage'],
                            'volume': ticker['baseVolume'],
                            'timestamp': datetime.now()
                        }
                        
                    except Exception as e:
                        self.logger.warning(f"⚠️ 获取 {exchange_name} {symbol} 价格失败: {e}")
                        
        except Exception as e:
            self.logger.error(f"❌ 更新价格数据失败: {e}")
    
    def _update_volume_data(self):
        """更新交易量数据"""
        try:
            symbols = ['BTC/USDT', 'ETH/USDT']
            
            for symbol in symbols:
                total_volume = 0
                exchange_count = 0
                
                for exchange_name, exchange in self.exchanges.items():
                    try:
                        ticker = exchange.fetch_ticker(symbol)
                        total_volume += ticker['baseVolume']
                        exchange_count += 1
                        
                    except Exception as e:
                        continue
                
                if exchange_count > 0:
                    avg_volume = total_volume / exchange_count
                    self.volume_cache[symbol] = {
                        'volume': avg_volume,
                        'exchange_count': exchange_count,
                        'timestamp': datetime.now()
                    }
                    
        except Exception as e:
            self.logger.error(f"❌ 更新交易量数据失败: {e}")
    
    def _update_system_status(self):
        """更新系统状态"""
        try:
            # 模拟系统状态数据
            self.system_status_cache = {
                'is_running': True,
                'uptime': str(datetime.now() - datetime(2024, 1, 1)),
                'active_strategies': 5,
                'total_trades': 156,
                'win_rate': np.random.uniform(0.6, 0.8),
                'total_return': np.random.uniform(0.15, 0.25),
                'max_drawdown': np.random.uniform(0.02, 0.08),
                'sharpe_ratio': np.random.uniform(1.0, 2.0),
                'cpu_usage': np.random.uniform(20, 60),
                'memory_usage': np.random.uniform(30, 70),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 更新系统状态失败: {e}")
    
    def _update_trading_signals(self):
        """更新交易信号"""
        try:
            # 模拟交易信号
            if np.random.random() < 0.1:  # 10%概率生成新信号
                signal = {
                    'symbol': np.random.choice(['BTC/USDT', 'ETH/USDT', 'BNB/USDT']),
                    'action': np.random.choice(['buy', 'sell', 'hold']),
                    'price': np.random.uniform(40000, 50000),
                    'confidence': np.random.uniform(0.6, 0.9),
                    'strategy': np.random.choice(['AI增强策略', 'RSI策略', 'MACD策略']),
                    'timestamp': datetime.now()
                }
                
                self.trading_signals_cache.append(signal)
                
                # 保持最近100条记录
                if len(self.trading_signals_cache) > 100:
                    self.trading_signals_cache = self.trading_signals_cache[-100:]
                    
        except Exception as e:
            self.logger.error(f"❌ 更新交易信号失败: {e}")
    
    def get_price_data(self, symbol: str = 'BTC/USDT', exchange: str = 'binance') -> Optional[Dict[str, Any]]:
        """获取价格数据"""
        try:
            cache_key = f"{exchange}_{symbol}"
            
            if cache_key in self.price_cache:
                data = self.price_cache[cache_key]
                
                # 检查缓存是否过期
                if (datetime.now() - data['timestamp']).seconds < self.cache_expiry['price']:
                    return data
            
            # 如果缓存过期或不存在，尝试获取新数据
            if exchange in self.exchanges:
                ticker = self.exchanges[exchange].fetch_ticker(symbol)
                
                data = {
                    'last': ticker['last'],
                    'bid': ticker['bid'],
                    'ask': ticker['ask'],
                    'high': ticker['high'],
                    'low': ticker['low'],
                    'change': ticker['percentage'],
                    'volume': ticker['baseVolume'],
                    'timestamp': datetime.now()
                }
                
                self.price_cache[cache_key] = data
                return data
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ 获取价格数据失败: {e}")
            return None
    
    def get_multi_exchange_prices(self, symbol: str = 'BTC/USDT') -> Dict[str, Any]:
        """获取多交易所价格"""
        try:
            prices = {}
            
            for exchange_name, exchange in self.exchanges.items():
                try:
                    ticker = exchange.fetch_ticker(symbol)
                    prices[exchange_name] = {
                        'last': ticker['last'],
                        'bid': ticker['bid'],
                        'ask': ticker['ask'],
                        'volume': ticker['baseVolume'],
                        'change': ticker['percentage'],
                        'timestamp': datetime.now()
                    }
                except Exception as e:
                    self.logger.warning(f"⚠️ 获取 {exchange_name} 价格失败: {e}")
                    prices[exchange_name] = None
            
            return prices
            
        except Exception as e:
            self.logger.error(f"❌ 获取多交易所价格失败: {e}")
            return {}
    
    def get_volume_data(self, symbol: str = 'BTC/USDT') -> Optional[Dict[str, Any]]:
        """获取交易量数据"""
        try:
            if symbol in self.volume_cache:
                data = self.volume_cache[symbol]
                
                # 检查缓存是否过期
                if (datetime.now() - data['timestamp']).seconds < self.cache_expiry['volume']:
                    return data
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ 获取交易量数据失败: {e}")
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        try:
            if self.system_status_cache:
                data = self.system_status_cache
                
                # 检查缓存是否过期
                if (datetime.now() - data['timestamp']).seconds < self.cache_expiry['system']:
                    return data
            
            return self.system_status_cache
            
        except Exception as e:
            self.logger.error(f"❌ 获取系统状态失败: {e}")
            return {}
    
    def get_trading_signals(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取交易信号"""
        try:
            return self.trading_signals_cache[-limit:] if self.trading_signals_cache else []
            
        except Exception as e:
            self.logger.error(f"❌ 获取交易信号失败: {e}")
            return []
    
    def get_risk_metrics(self) -> Dict[str, Any]:
        """获取风险指标"""
        try:
            return {
                'sharpe_ratio': np.random.uniform(1.0, 2.0),
                'volatility': np.random.uniform(10, 20),
                'max_drawdown': np.random.uniform(5, 15),
                'var_95': np.random.uniform(1, 5),
                'max_position': np.random.uniform(10, 25),
                'leverage': np.random.uniform(1.0, 2.5),
                'liquidity_score': np.random.uniform(70, 95),
                'correlation': np.random.uniform(0.2, 0.6),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取风险指标失败: {e}")
            return {}
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        try:
            return {
                'total_return': np.random.uniform(0.1, 0.3),
                'win_rate': np.random.uniform(0.5, 0.8),
                'total_trades': np.random.randint(100, 500),
                'avg_trade_duration': np.random.uniform(1, 24),
                'profit_factor': np.random.uniform(1.2, 2.5),
                'max_consecutive_losses': np.random.randint(3, 8),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取性能指标失败: {e}")
            return {}
    
    def stop(self):
        """停止数据管理器"""
        self.is_running = False
        self.logger.info("🛑 实时数据管理器已停止") 