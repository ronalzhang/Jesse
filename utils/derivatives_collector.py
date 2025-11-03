"""
衍生品数据采集器
支持获取Open Interest和Funding Rate
"""

import ccxt
import numpy as np
from datetime import datetime
from typing import Dict, Optional, List

class DerivativesDataCollector:
    """衍生品数据采集器"""
    
    def __init__(self, base_collector):
        """
        初始化
        
        Args:
            base_collector: 基础市场数据采集器实例
        """
        self.base_collector = base_collector
        self.cache = {}

    def _convert_to_futures_symbol(self, symbol: str, exchange_name: str) -> str:
        """
        将现货symbol转换为期货symbol
        
        Args:
            symbol: 现货交易对
            exchange_name: 交易所名称
            
        Returns:
            期货交易对symbol
        """
        # 如果已经是期货格式，直接返回
        if ':' in symbol:
            return symbol
        
        # 不同交易所的期货格式
        if exchange_name == 'binance':
            # Binance: BTC/USDT -> BTC/USDT:USDT
            if '/USDT' in symbol:
                return symbol + ':USDT'
        elif exchange_name == 'okx':
            # OKX: BTC/USDT -> BTC/USDT:USDT (永续合约)
            if '/USDT' in symbol:
                base = symbol.split('/')[0]
                return base + '-USDT-SWAP'
        elif exchange_name == 'bitget':
            # Bitget: BTC/USDT -> BTC/USDT:USDT
            if '/USDT' in symbol:
                return symbol + ':USDT'
        
        return symbol
        self.cache_expiry = {
            'open_interest': 300,  # 5分钟
            'funding_rate': 3600   # 1小时
        }
    
    def get_open_interest(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """
        获取持仓量数据
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            
        Returns:
            持仓量数据
        """
        try:
            if exchange_name not in self.base_collector.exchanges:
                if not self.base_collector.initialize_exchange(exchange_name):
                    return None
            
            exchange = self.base_collector.exchanges[exchange_name]
            
            # 检查交易所是否支持持仓量查询
            if not hasattr(exchange, 'fetch_open_interest'):
                return None
            
            # 转换为期货symbol
            futures_symbol = self._convert_to_futures_symbol(symbol, exchange_name)
            
            # 获取持仓量
            try:
                oi_data = exchange.fetch_open_interest(futures_symbol)
            except:
                # 如果期货symbol失败，尝试原始symbol
                oi_data = exchange.fetch_open_interest(symbol)
            
            if not oi_data:
                return None
            
            # 安全获取数值
            oi_amount = oi_data.get('openInterestAmount') or oi_data.get('openInterest') or 0
            oi_value = oi_data.get('openInterestValue') or 0
            
            return {
                'current': float(oi_amount) if oi_amount else 0,
                'value': float(oi_value) if oi_value else 0,
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'futures_symbol': futures_symbol,
                'exchange': exchange_name
            }
            
        except Exception as e:
            print(f"获取 {exchange_name} {symbol} 持仓量失败: {e}")
            return None
    

    def get_open_interest_history(self, exchange_name: str, symbol: str, 
                                  timeframe: str = '1h', limit: int = 24) -> Optional[List[Dict]]:
        """
        获取历史持仓量数据
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            timeframe: 时间框架
            limit: 数据条数
            
        Returns:
            历史持仓量列表
        """
        try:
            if exchange_name not in self.base_collector.exchanges:
                if not self.base_collector.initialize_exchange(exchange_name):
                    return None
            
            exchange = self.base_collector.exchanges[exchange_name]
            
            # 检查是否支持历史持仓量
            if not hasattr(exchange, 'fetch_open_interest_history'):
                # 如果不支持，返回当前持仓量作为单点数据
                current_oi = self.get_open_interest(exchange_name, symbol)
                if current_oi:
                    return [current_oi]
                return None
            
            # 转换为期货symbol
            futures_symbol = self._convert_to_futures_symbol(symbol, exchange_name)
            
            # 获取历史持仓量
            try:
                history = exchange.fetch_open_interest_history(futures_symbol, timeframe, limit=limit)
            except:
                history = exchange.fetch_open_interest_history(symbol, timeframe, limit=limit)
            
            if not history:
                return None
            
            return [
                {
                    'value': float(item.get('openInterestAmount', 0) or item.get('openInterest', 0)),
                    'timestamp': item.get('timestamp'),
                    'datetime': item.get('datetime')
                }
                for item in history
            ]
            
        except Exception as e:
            print(f"获取 {exchange_name} {symbol} 历史持仓量失败: {e}")
            return None
    def get_funding_rate(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """
        获取资金费率
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            
        Returns:
            资金费率数据
        """
        try:
            if exchange_name not in self.base_collector.exchanges:
                if not self.base_collector.initialize_exchange(exchange_name):
                    return None
            
            exchange = self.base_collector.exchanges[exchange_name]
            
            # 检查交易所是否支持资金费率查询
            if not hasattr(exchange, 'fetch_funding_rate'):
                return None
            
            # 获取资金费率
            # 转换为期货symbol
            futures_symbol = self._convert_to_futures_symbol(symbol, exchange_name)
            
            try:
                funding_data = exchange.fetch_funding_rate(futures_symbol)
            except:
                # 如果期货合约失败，尝试原始symbol
                try:
                    funding_data = exchange.fetch_funding_rate(symbol)
                except:
                    return None
            
            if not funding_data:
                return None
            
            return {
                'current': float(funding_data.get('fundingRate', 0)),
                'next_funding_time': funding_data.get('fundingTimestamp'),
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'exchange': exchange_name
            }
            
        except Exception as e:
            print(f"获取 {exchange_name} {symbol} 资金费率失败: {e}")
            return None
    
    def get_funding_rate_history(self, exchange_name: str, symbol: str, 
                                 limit: int = 24) -> Optional[List[Dict]]:
        """
        获取历史资金费率
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            limit: 数据条数
            
        Returns:
            历史资金费率列表
        """
        try:
            if exchange_name not in self.base_collector.exchanges:
                if not self.base_collector.initialize_exchange(exchange_name):
                    return None
            
            exchange = self.base_collector.exchanges[exchange_name]
            
            # 检查交易所是否支持历史资金费率查询
            if not hasattr(exchange, 'fetch_funding_rate_history'):
                return None
            
            # 获取历史资金费率
            history = exchange.fetch_funding_rate_history(symbol, limit=limit)
            
            if not history:
                return None
            
            return [
                {
                    'rate': float(item.get('fundingRate', 0)),
                    'timestamp': item.get('timestamp'),
                    'datetime': item.get('datetime')
                }
                for item in history
            ]
            
        except Exception as e:
            print(f"获取 {exchange_name} {symbol} 历史资金费率失败: {e}")
            return None
    
    def calculate_oi_metrics(self, oi_current: float, 
                            oi_history: Optional[List[float]] = None) -> Dict:
        """
        计算持仓量指标
        
        Args:
            oi_current: 当前持仓量
            oi_history: 历史持仓量列表
            
        Returns:
            持仓量指标
        """
        metrics = {
            'current': oi_current
        }
        
        if oi_history and len(oi_history) > 0:
            metrics['average'] = float(np.mean(oi_history))
            metrics['change_24h'] = float((oi_current - oi_history[0]) / oi_history[0] * 100) if oi_history[0] != 0 else 0
            metrics['max_24h'] = float(np.max(oi_history))
            metrics['min_24h'] = float(np.min(oi_history))
            metrics['std_24h'] = float(np.std(oi_history))
            
            # 计算趋势（线性回归斜率）
            if len(oi_history) >= 3:
                x = np.arange(len(oi_history))
                slope = np.polyfit(x, oi_history, 1)[0]
                metrics['trend'] = 'increasing' if slope > 0 else 'decreasing'
                metrics['trend_strength'] = float(abs(slope))
        
        return metrics
    
    def calculate_funding_metrics(self, funding_history: List[Dict]) -> Dict:
        """
        计算资金费率指标
        
        Args:
            funding_history: 历史资金费率列表
            
        Returns:
            资金费率指标
        """
        if not funding_history:
            return {}
        
        rates = [item['rate'] for item in funding_history]
        
        metrics = {
            'current': rates[-1] if rates else 0,
            'average_8h': float(np.mean(rates[-3:])) if len(rates) >= 3 else (rates[-1] if rates else 0),
            'average_24h': float(np.mean(rates)),
            'max_24h': float(np.max(rates)),
            'min_24h': float(np.min(rates)),
            'std_24h': float(np.std(rates))
        }
        
        # 计算市场情绪
        current_rate = rates[-1] if rates else 0
        if current_rate > 0.0001:
            metrics['sentiment'] = 'bullish'  # 多头情绪
        elif current_rate < -0.0001:
            metrics['sentiment'] = 'bearish'  # 空头情绪
        else:
            metrics['sentiment'] = 'neutral'  # 中性
        
        # 计算费率趋势
        if len(rates) >= 3:
            recent_avg = np.mean(rates[-3:])
            older_avg = np.mean(rates[:3])
            if recent_avg > older_avg * 1.1:
                metrics['trend'] = 'increasing'
            elif recent_avg < older_avg * 0.9:
                metrics['trend'] = 'decreasing'
            else:
                metrics['trend'] = 'stable'
        
        return metrics
    
    def get_comprehensive_derivatives_data(self, exchange_name: str, 
                                          symbol: str) -> Dict:
        """
        获取完整的衍生品数据
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
            
        Returns:
            完整的衍生品数据
        """
        result = {}
        
        # 获取当前持仓量
        oi_data = self.get_open_interest(exchange_name, symbol)
        if oi_data:
            result['open_interest'] = oi_data
            
            # 获取历史持仓量并计算指标
            oi_history = self.get_open_interest_history(exchange_name, symbol, '1h', 24)
            if oi_history:
                oi_values = [item['value'] for item in oi_history if item.get('value')]
                if oi_values:
                    oi_metrics = self.calculate_oi_metrics(oi_data['current'], oi_values)
                    result['oi_metrics'] = oi_metrics
        
        # 获取当前资金费率
        funding_data = self.get_funding_rate(exchange_name, symbol)
        if funding_data:
            result['funding_rate'] = funding_data
        
        # 获取历史资金费率并计算指标
        funding_history = self.get_funding_rate_history(exchange_name, symbol, 24)
        if funding_history:
            result['funding_history'] = funding_history
            funding_metrics = self.calculate_funding_metrics(funding_history)
            result['funding_metrics'] = funding_metrics
        
        return result
