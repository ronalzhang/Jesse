#!/usr/bin/env python3
"""
多交易所实时币价收集器
用于跨交易所套利策略的实时价格数据收集
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import threading
import json
from pathlib import Path

from utils.logging_manager import LoggerMixin
from config.exchange_config import ExchangeConfig

class MultiExchangePriceCollector(LoggerMixin):
    """多交易所实时币价收集器"""
    
    def __init__(self):
        """初始化多交易所价格收集器"""
        self.exchanges = {}
        self.rate_limits = {}
        self.last_request_time = {}
        self.price_cache = {}
        self.arbitrage_opportunities = []
        
        # 主流币种列表
        self.main_coins = [
            'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT',
            'XRP/USDT', 'DOT/USDT', 'DOGE/USDT', 'AVAX/USDT', 'MATIC/USDT'
        ]
        
        # 支持的交易所
        self.supported_exchanges = [
            'binance', 'okx', 'bybit', 'gate', 'kucoin', 'mexc'
        ]
        
        # 数据存储目录
        self.data_dir = Path("data/prices")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 缓存过期时间（秒）
        self.cache_expiry = 30
        
    def initialize_exchanges(self) -> bool:
        """初始化所有交易所连接"""
        try:
            self.logger.info("🔧 初始化多交易所连接...")
            
            for exchange_name in self.supported_exchanges:
                if self.initialize_exchange(exchange_name):
                    self.logger.info(f"✅ {exchange_name} 初始化成功")
                else:
                    self.logger.warning(f"⚠️ {exchange_name} 初始化失败")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 初始化交易所失败: {e}")
            return False
    
    def initialize_exchange(self, exchange_name: str) -> bool:
        """初始化单个交易所连接"""
        try:
            if exchange_name not in ExchangeConfig.SUPPORTED_EXCHANGES:
                self.logger.error(f"❌ 不支持的交易所: {exchange_name}")
                return False
            
            # 获取交易所配置
            config = ExchangeConfig.get_exchange_config(exchange_name)
            
            # 创建交易所实例（使用公共API，无需密钥）
            exchange_class = getattr(ccxt, exchange_name)
            exchange = exchange_class({
                'enableRateLimit': True,
                'timeout': 10000,  # 10秒超时
                'sandbox': False
            })
            
            self.exchanges[exchange_name] = exchange
            self.rate_limits[exchange_name] = config.get('rate_limit', 600)
            self.last_request_time[exchange_name] = 0
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 初始化交易所 {exchange_name} 失败: {e}")
            return False
    
    def _respect_rate_limit(self, exchange_name: str):
        """遵守速率限制"""
        if exchange_name in self.rate_limits:
            rate_limit = self.rate_limits[exchange_name]
            min_interval = 60.0 / rate_limit
            
            current_time = time.time()
            time_since_last = current_time - self.last_request_time.get(exchange_name, 0)
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                time.sleep(sleep_time)
            
            self.last_request_time[exchange_name] = time.time()
    
    def fetch_single_price(self, exchange_name: str, symbol: str) -> Optional[Dict[str, Any]]:
        """获取单个交易所的价格"""
        try:
            if exchange_name not in self.exchanges:
                if not self.initialize_exchange(exchange_name):
                    return None
            
            # 遵守速率限制
            self._respect_rate_limit(exchange_name)
            
            exchange = self.exchanges[exchange_name]
            
            # 获取ticker数据
            ticker = exchange.fetch_ticker(symbol)
            
            price_data = {
                'exchange': exchange_name,
                'symbol': symbol,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'high': ticker['high'],
                'low': ticker['low'],
                'volume': ticker['baseVolume'],
                'timestamp': datetime.now().isoformat(),
                'spread': ticker['ask'] - ticker['bid'] if ticker['ask'] and ticker['bid'] else None
            }
            
            return price_data
            
        except Exception as e:
            self.logger.warning(f"⚠️ 获取 {exchange_name} {symbol} 价格失败: {e}")
            return None
    
    def fetch_all_prices(self, symbol: str = 'BTC/USDT') -> Dict[str, List[Dict[str, Any]]]:
        """获取所有交易所的价格"""
        prices = []
        
        for exchange_name in self.supported_exchanges:
            price_data = self.fetch_single_price(exchange_name, symbol)
            if price_data:
                prices.append(price_data)
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'prices': prices,
            'exchange_count': len(prices)
        }
    
    def fetch_multi_coin_prices(self, symbols: List[str] = None) -> Dict[str, Any]:
        """获取多个币种的所有交易所价格"""
        if symbols is None:
            symbols = self.main_coins
        
        all_prices = {}
        
        for symbol in symbols:
            symbol_prices = self.fetch_all_prices(symbol)
            all_prices[symbol] = symbol_prices
            
            # 避免请求过于频繁
            time.sleep(1)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'symbols': symbols,
            'data': all_prices
        }
    
    def calculate_arbitrage_opportunities(self, prices_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """计算套利机会"""
        opportunities = []
        
        for symbol, symbol_data in prices_data['data'].items():
            prices = symbol_data['prices']
            
            if len(prices) < 2:
                continue
            
            # 找到最高买价和最低卖价
            max_bid = max(prices, key=lambda x: x['bid'] if x['bid'] else 0)
            min_ask = min(prices, key=lambda x: x['ask'] if x['ask'] else float('inf'))
            
            if max_bid['exchange'] != min_ask['exchange'] and max_bid['bid'] and min_ask['ask']:
                spread = min_ask['ask'] - max_bid['bid']
                spread_percentage = (spread / max_bid['bid']) * 100
                
                if spread_percentage > 0.1:  # 0.1%以上的价差
                    opportunity = {
                        'symbol': symbol,
                        'buy_exchange': max_bid['exchange'],
                        'sell_exchange': min_ask['exchange'],
                        'buy_price': max_bid['bid'],
                        'sell_price': min_ask['ask'],
                        'spread': spread,
                        'spread_percentage': spread_percentage,
                        'timestamp': datetime.now().isoformat()
                    }
                    opportunities.append(opportunity)
        
        return opportunities
    
    def get_price_comparison_chart_data(self, symbol: str = 'BTC/USDT') -> Dict[str, Any]:
        """获取价格对比图表数据"""
        prices_data = self.fetch_all_prices(symbol)
        
        if not prices_data['prices']:
            return {}
        
        # 准备图表数据
        exchanges = []
        last_prices = []
        bid_prices = []
        ask_prices = []
        volumes = []
        
        for price in prices_data['prices']:
            exchanges.append(price['exchange'])
            last_prices.append(price['last'])
            bid_prices.append(price['bid'])
            ask_prices.append(price['ask'])
            volumes.append(price['volume'])
        
        return {
            'symbol': symbol,
            'exchanges': exchanges,
            'last_prices': last_prices,
            'bid_prices': bid_prices,
            'ask_prices': ask_prices,
            'volumes': volumes,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_arbitrage_summary(self) -> Dict[str, Any]:
        """获取套利机会摘要"""
        all_prices = self.fetch_multi_coin_prices()
        opportunities = self.calculate_arbitrage_opportunities(all_prices)
        
        # 按币种分组
        opportunities_by_symbol = {}
        for opp in opportunities:
            symbol = opp['symbol']
            if symbol not in opportunities_by_symbol:
                opportunities_by_symbol[symbol] = []
            opportunities_by_symbol[symbol].append(opp)
        
        # 计算统计信息
        total_opportunities = len(opportunities)
        avg_spread = np.mean([opp['spread_percentage'] for opp in opportunities]) if opportunities else 0
        max_spread = max([opp['spread_percentage'] for opp in opportunities]) if opportunities else 0
        
        return {
            'total_opportunities': total_opportunities,
            'average_spread': avg_spread,
            'max_spread': max_spread,
            'opportunities_by_symbol': opportunities_by_symbol,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_price_data(self, data: Dict[str, Any], filename: str = None):
        """保存价格数据到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prices_{timestamp}.json"
        
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"✅ 价格数据已保存到 {filepath}")
            
        except Exception as e:
            self.logger.error(f"❌ 保存价格数据失败: {e}")
    
    def load_price_data(self, filename: str) -> Dict[str, Any]:
        """从文件加载价格数据"""
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ 加载价格数据失败: {e}")
            return {}
    
    def get_latest_price_files(self, limit: int = 10) -> List[str]:
        """获取最新的价格数据文件"""
        try:
            files = list(self.data_dir.glob("prices_*.json"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return [f.name for f in files[:limit]]
            
        except Exception as e:
            self.logger.error(f"❌ 获取价格文件列表失败: {e}")
            return []
    
    def cleanup(self):
        """清理资源"""
        try:
            for exchange in self.exchanges.values():
                if hasattr(exchange, 'close'):
                    exchange.close()
            
            self.logger.info("✅ 多交易所价格收集器清理完成")
            
        except Exception as e:
            self.logger.error(f"❌ 清理失败: {e}")

# 全局实例
price_collector = MultiExchangePriceCollector()

def get_price_collector() -> MultiExchangePriceCollector:
    """获取价格收集器实例"""
    return price_collector 