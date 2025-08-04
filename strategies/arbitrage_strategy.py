#!/usr/bin/env python3
"""
跨交易所套利策略
基于多交易所价格差异的套利策略
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import time

from utils.logging_manager import LoggerMixin
from data.multi_exchange_price_collector import get_price_collector

class ArbitrageStrategy(LoggerMixin):
    """跨交易所套利策略"""
    
    def __init__(self):
        """初始化套利策略"""
        self.price_collector = get_price_collector()
        self.min_spread_threshold = 0.001  # 最小价差阈值 0.1%
        self.max_position_size = 0.1  # 最大仓位 10%
        self.transaction_fee = 0.001  # 交易手续费 0.1%
        self.slippage = 0.0005  # 滑点 0.05%
        
        # 套利机会记录
        self.arbitrage_opportunities = []
        self.executed_trades = []
        
    def initialize(self):
        """初始化策略"""
        try:
            self.logger.info("🔧 初始化跨交易所套利策略...")
            
            # 初始化价格收集器
            if not self.price_collector.initialize_exchanges():
                self.logger.error("❌ 初始化交易所连接失败")
                return False
            
            self.logger.info("✅ 跨交易所套利策略初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 初始化套利策略失败: {e}")
            return False
    
    def scan_arbitrage_opportunities(self, symbols: List[str] = None) -> List[Dict[str, Any]]:
        """扫描套利机会"""
        try:
            if symbols is None:
                symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
            
            opportunities = []
            
            for symbol in symbols:
                # 获取多交易所价格
                prices_data = self.price_collector.fetch_all_prices(symbol)
                
                if not prices_data['prices'] or len(prices_data['prices']) < 2:
                    continue
                
                # 分析价格差异
                symbol_opportunities = self._analyze_price_differences(symbol, prices_data['prices'])
                opportunities.extend(symbol_opportunities)
            
            # 按收益排序
            opportunities.sort(key=lambda x: x['expected_profit_percentage'], reverse=True)
            
            self.logger.info(f"🔍 发现 {len(opportunities)} 个套利机会")
            return opportunities
            
        except Exception as e:
            self.logger.error(f"❌ 扫描套利机会失败: {e}")
            return []
    
    def _analyze_price_differences(self, symbol: str, prices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析价格差异"""
        opportunities = []
        
        # 找到最高买价和最低卖价
        valid_prices = [p for p in prices if p['bid'] and p['ask']]
        
        if len(valid_prices) < 2:
            return opportunities
        
        # 计算所有交易所对之间的价差
        for i, buy_exchange in enumerate(valid_prices):
            for j, sell_exchange in enumerate(valid_prices):
                if i == j:
                    continue
                
                buy_price = buy_exchange['bid']
                sell_price = sell_exchange['ask']
                
                if buy_price >= sell_price:
                    continue
                
                # 计算价差
                spread = sell_price - buy_price
                spread_percentage = (spread / buy_price) * 100
                
                # 计算净收益（扣除手续费和滑点）
                total_fees = (buy_price + sell_price) * (self.transaction_fee + self.slippage)
                net_profit = spread - total_fees
                net_profit_percentage = (net_profit / buy_price) * 100
                
                # 检查是否满足最小价差要求
                if net_profit_percentage > self.min_spread_threshold * 100:
                    opportunity = {
                        'symbol': symbol,
                        'buy_exchange': buy_exchange['exchange'],
                        'sell_exchange': sell_exchange['exchange'],
                        'buy_price': buy_price,
                        'sell_price': sell_price,
                        'spread': spread,
                        'spread_percentage': spread_percentage,
                        'net_profit': net_profit,
                        'net_profit_percentage': net_profit_percentage,
                        'total_fees': total_fees,
                        'timestamp': datetime.now().isoformat(),
                        'risk_score': self._calculate_risk_score(buy_exchange, sell_exchange)
                    }
                    opportunities.append(opportunity)
        
        return opportunities
    
    def _calculate_risk_score(self, buy_exchange: Dict, sell_exchange: Dict) -> float:
        """计算风险评分"""
        risk_score = 0.0
        
        # 基于交易量的风险评分
        buy_volume = buy_exchange.get('volume', 0)
        sell_volume = sell_exchange.get('volume', 0)
        
        if buy_volume < 1000 or sell_volume < 1000:
            risk_score += 0.3
        
        # 基于价差的风险评分
        spread = sell_exchange['ask'] - buy_exchange['bid']
        if spread > 100:  # 价差过大可能表示流动性问题
            risk_score += 0.2
        
        # 基于交易所的风险评分
        major_exchanges = ['binance', 'okx', 'bybit']
        if buy_exchange['exchange'] not in major_exchanges:
            risk_score += 0.1
        if sell_exchange['exchange'] not in major_exchanges:
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def execute_arbitrage(self, opportunity: Dict[str, Any], position_size: float = None) -> bool:
        """执行套利交易"""
        try:
            if position_size is None:
                position_size = self.max_position_size
            
            # 检查风险评分
            if opportunity['risk_score'] > 0.5:
                self.logger.warning(f"⚠️ 风险评分过高: {opportunity['risk_score']}")
                return False
            
            # 模拟执行交易
            trade_result = {
                'opportunity_id': len(self.executed_trades) + 1,
                'symbol': opportunity['symbol'],
                'buy_exchange': opportunity['buy_exchange'],
                'sell_exchange': opportunity['sell_exchange'],
                'buy_price': opportunity['buy_price'],
                'sell_price': opportunity['sell_price'],
                'position_size': position_size,
                'expected_profit': opportunity['net_profit'] * position_size,
                'execution_time': datetime.now().isoformat(),
                'status': 'executed'
            }
            
            self.executed_trades.append(trade_result)
            
            self.logger.info(f"✅ 执行套利交易: {opportunity['symbol']} "
                           f"从 {opportunity['buy_exchange']} 到 {opportunity['sell_exchange']} "
                           f"预期收益: {trade_result['expected_profit']:.2f} USDT")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 执行套利交易失败: {e}")
            return False
    
    def get_arbitrage_summary(self) -> Dict[str, Any]:
        """获取套利策略摘要"""
        if not self.executed_trades:
            return {
                'total_trades': 0,
                'total_profit': 0,
                'success_rate': 0,
                'avg_profit_per_trade': 0
            }
        
        total_trades = len(self.executed_trades)
        total_profit = sum(trade['expected_profit'] for trade in self.executed_trades)
        avg_profit = total_profit / total_trades if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'total_profit': total_profit,
            'success_rate': 1.0,  # 模拟100%成功率
            'avg_profit_per_trade': avg_profit,
            'recent_trades': self.executed_trades[-10:]  # 最近10笔交易
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        summary = self.get_arbitrage_summary()
        
        # 计算年化收益率（假设每天执行10笔交易）
        daily_trades = 10
        annual_trades = daily_trades * 365
        annual_profit = summary['avg_profit_per_trade'] * annual_trades
        
        return {
            'daily_trades': daily_trades,
            'annual_trades': annual_trades,
            'annual_profit': annual_profit,
            'roi_percentage': (annual_profit / 10000) * 100,  # 假设本金1万USDT
            'risk_adjusted_return': annual_profit * (1 - summary.get('success_rate', 0.9))
        }
    
    def update_parameters(self, min_spread: float = None, max_position: float = None,
                         transaction_fee: float = None, slippage: float = None):
        """更新策略参数"""
        if min_spread is not None:
            self.min_spread_threshold = min_spread
        if max_position is not None:
            self.max_position_size = max_position
        if transaction_fee is not None:
            self.transaction_fee = transaction_fee
        if slippage is not None:
            self.slippage = slippage
        
        self.logger.info(f"✅ 套利策略参数已更新: "
                        f"最小价差={self.min_spread_threshold}, "
                        f"最大仓位={self.max_position_size}, "
                        f"手续费={self.transaction_fee}, "
                        f"滑点={self.slippage}")
    
    def cleanup(self):
        """清理资源"""
        try:
            self.price_collector.cleanup()
            self.logger.info("✅ 套利策略清理完成")
            
        except Exception as e:
            self.logger.error(f"❌ 清理失败: {e}")

# 全局实例
arbitrage_strategy = ArbitrageStrategy()

def get_arbitrage_strategy() -> ArbitrageStrategy:
    """获取套利策略实例"""
    return arbitrage_strategy 