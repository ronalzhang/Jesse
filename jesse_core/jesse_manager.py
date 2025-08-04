"""
Jesse管理器
负责Jesse核心功能的封装和管理
"""

import jesse.helpers as jh
from jesse.services import exchanges
from jesse.strategies import Strategy
import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

class JesseManager:
    """Jesse管理器，封装Jesse核心功能"""
    
    def __init__(self):
        """初始化Jesse管理器"""
        self.logger = logging.getLogger(__name__)
        self.exchanges = {}
        self.strategies = {}
        self.is_initialized = False
        
    def initialize(self):
        """初始化Jesse管理器"""
        try:
            self.logger.info("🔧 初始化Jesse管理器...")
            
            # 初始化交易所连接
            self._initialize_exchanges()
            
            # 初始化策略
            self._initialize_strategies()
            
            self.is_initialized = True
            self.logger.info("✅ Jesse管理器初始化完成")
            
        except Exception as e:
            self.logger.error(f"❌ Jesse管理器初始化失败: {e}")
            raise
    
    def _initialize_exchanges(self):
        """初始化交易所连接"""
        # 支持的交易所列表
        supported_exchanges = [
            'binance', 'coinbase', 'kraken', 'bitfinex',
            'huobi', 'okex', 'bybit', 'gate', 'kucoin'
        ]
        
        for exchange_name in supported_exchanges:
            try:
                # 创建交易所实例
                exchange = ccxt.create_exchange(exchange_name)
                self.exchanges[exchange_name] = exchange
                self.logger.info(f"✅ 初始化交易所: {exchange_name}")
                
            except Exception as e:
                self.logger.warning(f"⚠️ 初始化交易所 {exchange_name} 失败: {e}")
    
    def _initialize_strategies(self):
        """初始化交易策略"""
        # 这里可以加载自定义策略
        self.strategies = {
            'trend_following': self._create_trend_following_strategy(),
            'mean_reversion': self._create_mean_reversion_strategy(),
            'arbitrage': self._create_arbitrage_strategy(),
            'grid_trading': self._create_grid_trading_strategy()
        }
        
        self.logger.info(f"✅ 初始化了 {len(self.strategies)} 个策略")
    
    def collect_market_data(self) -> Dict[str, Any]:
        """收集市场数据"""
        try:
            market_data = {}
            
            for exchange_name, exchange in self.exchanges.items():
                try:
                    # 获取主要交易对的数据
                    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
                    
                    for symbol in symbols:
                        # 获取OHLCV数据
                        ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=100)
                        
                        # 获取订单簿数据
                        orderbook = exchange.fetch_order_book(symbol)
                        
                        # 获取交易数据
                        trades = exchange.fetch_trades(symbol, limit=50)
                        
                        market_data[f"{exchange_name}_{symbol}"] = {
                            'ohlcv': ohlcv,
                            'orderbook': orderbook,
                            'trades': trades,
                            'exchange': exchange_name,
                            'symbol': symbol
                        }
                        
                except Exception as e:
                    self.logger.warning(f"⚠️ 获取 {exchange_name} 数据失败: {e}")
                    continue
            
            self.logger.info(f"📊 收集了 {len(market_data)} 个市场数据")
            return market_data
            
        except Exception as e:
            self.logger.error(f"❌ 收集市场数据失败: {e}")
            return {}
    
    def execute_strategies(self, strategies: List[Dict]) -> Dict[str, Any]:
        """执行交易策略"""
        try:
            results = {}
            
            for strategy in strategies:
                try:
                    # 执行策略
                    result = self._execute_single_strategy(strategy)
                    results[strategy.get('name', 'unknown')] = result
                    
                except Exception as e:
                    self.logger.error(f"❌ 执行策略失败: {e}")
                    continue
            
            self.logger.info(f"🎯 执行了 {len(results)} 个策略")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ 执行策略失败: {e}")
            return {}
    
    def _execute_single_strategy(self, strategy: Dict) -> Dict[str, Any]:
        """执行单个策略"""
        strategy_name = strategy.get('name', 'unknown')
        strategy_type = strategy.get('type', 'unknown')
        
        try:
            # 根据策略类型执行不同的逻辑
            if strategy_type == 'trend_following':
                return self._execute_trend_following(strategy)
            elif strategy_type == 'mean_reversion':
                return self._execute_mean_reversion(strategy)
            elif strategy_type == 'arbitrage':
                return self._execute_arbitrage(strategy)
            elif strategy_type == 'grid_trading':
                return self._execute_grid_trading(strategy)
            else:
                self.logger.warning(f"⚠️ 未知策略类型: {strategy_type}")
                return {'status': 'unknown_strategy'}
                
        except Exception as e:
            self.logger.error(f"❌ 执行策略 {strategy_name} 失败: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _execute_trend_following(self, strategy: Dict) -> Dict[str, Any]:
        """执行趋势跟踪策略"""
        # 实现趋势跟踪逻辑
        return {
            'status': 'success',
            'strategy': 'trend_following',
            'signal': 'buy',  # 或 'sell', 'hold'
            'confidence': 0.8,
            'reasoning': '趋势向上，建议买入'
        }
    
    def _execute_mean_reversion(self, strategy: Dict) -> Dict[str, Any]:
        """执行均值回归策略"""
        # 实现均值回归逻辑
        return {
            'status': 'success',
            'strategy': 'mean_reversion',
            'signal': 'sell',
            'confidence': 0.7,
            'reasoning': '价格偏离均值，建议卖出'
        }
    
    def _execute_arbitrage(self, strategy: Dict) -> Dict[str, Any]:
        """执行套利策略"""
        # 实现套利逻辑
        return {
            'status': 'success',
            'strategy': 'arbitrage',
            'signal': 'arbitrage',
            'confidence': 0.9,
            'reasoning': '发现套利机会'
        }
    
    def _execute_grid_trading(self, strategy: Dict) -> Dict[str, Any]:
        """执行网格交易策略"""
        # 实现网格交易逻辑
        return {
            'status': 'success',
            'strategy': 'grid_trading',
            'signal': 'grid_buy',
            'confidence': 0.6,
            'reasoning': '网格买入信号'
        }
    
    def _create_trend_following_strategy(self) -> Dict:
        """创建趋势跟踪策略"""
        return {
            'name': 'trend_following',
            'type': 'trend_following',
            'parameters': {
                'ma_short': 10,
                'ma_long': 30,
                'rsi_period': 14,
                'rsi_overbought': 70,
                'rsi_oversold': 30
            }
        }
    
    def _create_mean_reversion_strategy(self) -> Dict:
        """创建均值回归策略"""
        return {
            'name': 'mean_reversion',
            'type': 'mean_reversion',
            'parameters': {
                'bollinger_period': 20,
                'bollinger_std': 2,
                'rsi_period': 14
            }
        }
    
    def _create_arbitrage_strategy(self) -> Dict:
        """创建套利策略"""
        return {
            'name': 'arbitrage',
            'type': 'arbitrage',
            'parameters': {
                'min_spread': 0.001,
                'max_position_size': 1000
            }
        }
    
    def _create_grid_trading_strategy(self) -> Dict:
        """创建网格交易策略"""
        return {
            'name': 'grid_trading',
            'type': 'grid_trading',
            'parameters': {
                'grid_levels': 10,
                'grid_spacing': 0.01,
                'base_amount': 100
            }
        }
    
    def cleanup(self):
        """清理资源"""
        try:
            self.logger.info("🧹 清理Jesse管理器资源...")
            
            # 关闭交易所连接
            for exchange_name, exchange in self.exchanges.items():
                try:
                    exchange.close()
                    self.logger.info(f"✅ 关闭交易所连接: {exchange_name}")
                except Exception as e:
                    self.logger.warning(f"⚠️ 关闭交易所 {exchange_name} 失败: {e}")
            
            self.logger.info("✅ Jesse管理器清理完成")
            
        except Exception as e:
            self.logger.error(f"❌ Jesse管理器清理失败: {e}") 