"""
策略数据适配器
将增强版市场数据适配给策略使用
"""

from typing import Dict, Any, List, Optional
from data.market_data_collector import MarketDataCollector

class StrategyDataAdapter:
    """策略数据适配器"""
    
    def __init__(self, collector: Optional[MarketDataCollector] = None):
        """
        初始化适配器
        
        Args:
            collector: 市场数据采集器实例
        """
        self.collector = collector or MarketDataCollector()
    
    def get_strategy_data(self, exchange: str, symbol: str,
                         timeframes: Optional[List[str]] = None,
                         include_derivatives: bool = True) -> Dict[str, Any]:
        """
        获取策略所需的完整数据
        
        Args:
            exchange: 交易所名称
            symbol: 交易对
            timeframes: 时间框架列表
            include_derivatives: 是否包含衍生品数据
            
        Returns:
            策略数据
        """
        # 获取增强版市场数据
        market_data = self.collector.get_enhanced_market_data(
            exchange, symbol,
            include_multi_timeframe=True,
            include_derivatives=include_derivatives,
            timeframes=timeframes
        )
        
        if not market_data:
            return {}
        
        # 添加便捷访问字段
        strategy_data = market_data.copy()
        
        # 添加当前价格（从ticker或indicators）
        if 'ticker' in market_data and market_data['ticker']:
            strategy_data['current_price'] = market_data['ticker'].get('last', 0)
        elif 'indicators' in market_data:
            strategy_data['current_price'] = market_data['indicators'].get('current_price', 0)
        
        # 添加主要指标快捷访问
        if 'indicators' in market_data:
            strategy_data['primary_indicators'] = market_data['indicators']
        
        return strategy_data
    
    def get_batch_strategy_data(self, pairs: List[tuple],
                               timeframes: Optional[List[str]] = None,
                               include_derivatives: bool = True) -> Dict[str, Dict]:
        """
        批量获取多个交易对的策略数据
        
        Args:
            pairs: 交易对列表 [(exchange, symbol), ...]
            timeframes: 时间框架列表
            include_derivatives: 是否包含衍生品数据
            
        Returns:
            策略数据字典 {f"{exchange}_{symbol}": data}
        """
        batch_data = {}
        
        for exchange, symbol in pairs:
            key = f"{exchange}_{symbol}"
            data = self.get_strategy_data(
                exchange, symbol, timeframes, include_derivatives
            )
            if data:
                batch_data[key] = data
        
        return batch_data
    
    def extract_features_for_ml(self, market_data: Dict[str, Any],
                                timeframes: Optional[List[str]] = None) -> List[float]:
        """
        从市场数据中提取机器学习特征
        
        Args:
            market_data: 市场数据
            timeframes: 要提取的时间框架
            
        Returns:
            特征向量
        """
        features = []
        
        # 提取基础指标
        if 'indicators' in market_data:
            ind = market_data['indicators']
            features.extend([
                ind.get('ema20', 0),
                ind.get('rsi14', 50),
                ind.get('macd', 0),
                ind.get('atr14', 0),
                ind.get('volume_ratio', 1)
            ])
        
        # 提取多时间框架指标
        if timeframes and 'timeframes' in market_data:
            for tf in timeframes:
                if tf in market_data['timeframes']:
                    tf_ind = market_data['timeframes'][tf].get('indicators', {})
                    features.extend([
                        tf_ind.get('ema20', 0),
                        tf_ind.get('rsi14', 50),
                        tf_ind.get('macd', 0)
                    ])
        
        # 提取衍生品数据
        if 'derivatives' in market_data:
            deriv = market_data['derivatives']
            
            if 'funding_metrics' in deriv:
                fm = deriv['funding_metrics']
                features.append(fm.get('current', 0))
                features.append(fm.get('average_24h', 0))
            
            if 'oi_metrics' in deriv:
                oi = deriv['oi_metrics']
                features.append(oi.get('change_24h', 0))
        
        return features
