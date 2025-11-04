"""
智能套利机会扫描器
自动扫描多交易所套利机会，无需手动选择
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd
from dataclasses import dataclass

@dataclass
class ArbitrageOpportunity:
    """套利机会数据类"""
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    spread_percent: float
    profit_potential: float
    volume_24h: float
    timestamp: datetime
    confidence: str  # 'high', 'medium', 'low'
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'buy_exchange': self.buy_exchange,
            'sell_exchange': self.sell_exchange,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'spread_percent': self.spread_percent,
            'profit_potential': self.profit_potential,
            'volume_24h': self.volume_24h,
            'timestamp': self.timestamp.isoformat(),
            'confidence': self.confidence
        }


class ArbitrageScanner:
    """智能套利扫描器"""
    
    def __init__(self, market_data_collector):
        """
        初始化套利扫描器
        
        Args:
            market_data_collector: 市场数据采集器实例
        """
        self.collector = market_data_collector
        
        # 扫描配置
        self.min_spread_percent = 0.5  # 最小价差百分比（考虑手续费）
        self.min_volume_24h = 100000  # 最小24h成交量（USD）
        self.scan_interval = 30  # 扫描间隔（秒）
        
        # 交易所手续费（maker/taker平均）
        self.exchange_fees = {
            'binance': 0.1,  # 0.1%
            'bitget': 0.1,
            'okx': 0.1
        }
        
        # 缓存
        self.opportunities_cache = []
        self.last_scan_time = 0
        
        # 统计
        self.total_scans = 0
        self.opportunities_found = 0
    
    def calculate_net_profit(self, spread_percent: float, 
                            buy_exchange: str, sell_exchange: str) -> float:
        """
        计算净利润（扣除手续费）
        
        Args:
            spread_percent: 价差百分比
            buy_exchange: 买入交易所
            sell_exchange: 卖出交易所
            
        Returns:
            净利润百分比
        """
        buy_fee = self.exchange_fees.get(buy_exchange, 0.1)
        sell_fee = self.exchange_fees.get(sell_exchange, 0.1)
        total_fee = buy_fee + sell_fee
        
        return spread_percent - total_fee
    
    def assess_confidence(self, spread_percent: float, volume_24h: float) -> str:
        """
        评估套利机会的置信度
        
        Args:
            spread_percent: 价差百分比
            volume_24h: 24小时成交量
            
        Returns:
            置信度等级
        """
        # 高置信度：价差大且成交量高
        if spread_percent >= 1.0 and volume_24h >= 1000000:
            return 'high'
        # 中等置信度：价差中等或成交量中等
        elif spread_percent >= 0.7 or volume_24h >= 500000:
            return 'medium'
        # 低置信度
        else:
            return 'low'
    
    def scan_symbol(self, symbol: str, exchanges: List[str]) -> List[ArbitrageOpportunity]:
        """
        扫描单个交易对的套利机会
        
        Args:
            symbol: 交易对
            exchanges: 交易所列表
            
        Returns:
            套利机会列表
        """
        opportunities = []
        prices = {}
        
        # 获取所有交易所的价格
        for exchange in exchanges:
            try:
                ticker = self.collector.fetch_ticker(exchange, symbol)
                if ticker and ticker.get('last'):
                    prices[exchange] = {
                        'price': ticker['last'],
                        'volume': ticker.get('baseVolume', 0) * ticker['last']
                    }
            except Exception as e:
                continue
        
        # 如果少于2个交易所有数据，无法套利
        if len(prices) < 2:
            return opportunities
        
        # 寻找套利机会
        exchange_list = list(prices.keys())
        for i in range(len(exchange_list)):
            for j in range(i + 1, len(exchange_list)):
                ex1, ex2 = exchange_list[i], exchange_list[j]
                price1 = prices[ex1]['price']
                price2 = prices[ex2]['price']
                
                # 计算价差
                if price1 < price2:
                    buy_ex, sell_ex = ex1, ex2
                    buy_price, sell_price = price1, price2
                else:
                    buy_ex, sell_ex = ex2, ex1
                    buy_price, sell_price = price2, price1
                
                spread_percent = ((sell_price - buy_price) / buy_price) * 100
                
                # 计算净利润
                net_profit = self.calculate_net_profit(spread_percent, buy_ex, sell_ex)
                
                # 如果净利润大于最小阈值，记录机会
                if net_profit >= self.min_spread_percent:
                    avg_volume = (prices[buy_ex]['volume'] + prices[sell_ex]['volume']) / 2
                    
                    if avg_volume >= self.min_volume_24h:
                        confidence = self.assess_confidence(net_profit, avg_volume)
                        
                        opportunity = ArbitrageOpportunity(
                            symbol=symbol,
                            buy_exchange=buy_ex,
                            sell_exchange=sell_ex,
                            buy_price=buy_price,
                            sell_price=sell_price,
                            spread_percent=spread_percent,
                            profit_potential=net_profit,
                            volume_24h=avg_volume,
                            timestamp=datetime.now(),
                            confidence=confidence
                        )
                        opportunities.append(opportunity)
        
        return opportunities
    
    def scan_all_symbols(self, symbols: List[str], exchanges: List[str]) -> List[ArbitrageOpportunity]:
        """
        扫描所有交易对的套利机会
        
        Args:
            symbols: 交易对列表
            exchanges: 交易所列表
            
        Returns:
            所有套利机会列表
        """
        all_opportunities = []
        
        for symbol in symbols:
            opportunities = self.scan_symbol(symbol, exchanges)
            all_opportunities.extend(opportunities)
        
        # 按利润潜力排序
        all_opportunities.sort(key=lambda x: x.profit_potential, reverse=True)
        
        return all_opportunities
    
    def continuous_scan(self, symbols: List[str], exchanges: List[str], 
                       callback=None) -> List[ArbitrageOpportunity]:
        """
        持续扫描（带缓存）
        
        Args:
            symbols: 交易对列表
            exchanges: 交易所列表
            callback: 发现机会时的回调函数
            
        Returns:
            套利机会列表
        """
        current_time = time.time()
        
        # 检查是否需要重新扫描
        if current_time - self.last_scan_time < self.scan_interval:
            return self.opportunities_cache
        
        # 执行扫描
        opportunities = self.scan_all_symbols(symbols, exchanges)
        
        # 更新统计
        self.total_scans += 1
        self.opportunities_found += len(opportunities)
        
        # 更新缓存
        self.opportunities_cache = opportunities
        self.last_scan_time = current_time
        
        # 如果有回调函数，调用它
        if callback and opportunities:
            callback(opportunities)
        
        return opportunities
    
    def get_statistics(self) -> Dict:
        """获取扫描统计信息"""
        return {
            'total_scans': self.total_scans,
            'opportunities_found': self.opportunities_found,
            'avg_opportunities_per_scan': (
                self.opportunities_found / self.total_scans 
                if self.total_scans > 0 else 0
            ),
            'last_scan_time': datetime.fromtimestamp(self.last_scan_time).isoformat() 
                if self.last_scan_time > 0 else None,
            'cache_size': len(self.opportunities_cache)
        }
    
    def get_top_opportunities(self, limit: int = 10) -> List[Dict]:
        """
        获取最佳套利机会
        
        Args:
            limit: 返回数量限制
            
        Returns:
            套利机会列表（字典格式）
        """
        return [opp.to_dict() for opp in self.opportunities_cache[:limit]]
    
    def filter_by_confidence(self, confidence: str) -> List[ArbitrageOpportunity]:
        """
        按置信度筛选机会
        
        Args:
            confidence: 置信度等级 ('high', 'medium', 'low')
            
        Returns:
            筛选后的机会列表
        """
        return [opp for opp in self.opportunities_cache if opp.confidence == confidence]
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """导出为DataFrame"""
        if not self.opportunities_cache:
            return pd.DataFrame()
        
        data = [opp.to_dict() for opp in self.opportunities_cache]
        return pd.DataFrame(data)
