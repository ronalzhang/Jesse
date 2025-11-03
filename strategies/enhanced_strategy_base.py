"""
增强版策略基类
支持多时间框架和丰富的技术指标
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from utils.logging_manager import LoggerMixin

class EnhancedStrategyBase(ABC, LoggerMixin):
    """增强版策略基类"""
    
    def __init__(self, name: str, parameters: Dict[str, Any] = None):
        """
        初始化策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        self.name = name
        self.parameters = parameters or {}
        self.is_active = True
        self.performance_metrics = {}
        
        # 多时间框架配置
        self.timeframes = self.parameters.get('timeframes', ['1h'])
        self.primary_timeframe = self.parameters.get('primary_timeframe', '1h')
        
        # 技术指标配置
        self.use_indicators = self.parameters.get('use_indicators', True)
        self.use_derivatives = self.parameters.get('use_derivatives', False)
    
    def extract_indicators(self, market_data: Dict[str, Any], 
                          timeframe: Optional[str] = None) -> Dict[str, float]:
        """
        从市场数据中提取技术指标
        
        Args:
            market_data: 市场数据
            timeframe: 时间框架（可选）
            
        Returns:
            技术指标字典
        """
        indicators = {}
        
        # 如果指定了时间框架，从timeframes中提取
        if timeframe and 'timeframes' in market_data:
            tf_data = market_data['timeframes'].get(timeframe, {})
            indicators = tf_data.get('indicators', {})
        # 否则使用基础指标
        elif 'indicators' in market_data:
            indicators = market_data['indicators']
        
        return indicators
    
    def extract_derivatives_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从市场数据中提取衍生品数据
        
        Args:
            market_data: 市场数据
            
        Returns:
            衍生品数据字典
        """
        return market_data.get('derivatives', {})
    
    def get_multi_timeframe_indicators(self, market_data: Dict[str, Any]) -> Dict[str, Dict]:
        """
        获取多时间框架的技术指标
        
        Args:
            market_data: 市场数据
            
        Returns:
            多时间框架指标字典
        """
        mtf_indicators = {}
        
        if 'timeframes' not in market_data:
            return mtf_indicators
        
        for tf in self.timeframes:
            if tf in market_data['timeframes']:
                mtf_indicators[tf] = market_data['timeframes'][tf].get('indicators', {})
        
        return mtf_indicators
    
    def check_trend_alignment(self, mtf_indicators: Dict[str, Dict]) -> str:
        """
        检查多时间框架趋势一致性
        
        Args:
            mtf_indicators: 多时间框架指标
            
        Returns:
            趋势方向 ('bullish', 'bearish', 'neutral')
        """
        trends = []
        
        for tf, indicators in mtf_indicators.items():
            if 'ema20' in indicators and 'current_price' in indicators:
                price = indicators['current_price']
                ema20 = indicators['ema20']
                
                if price > ema20:
                    trends.append('bullish')
                elif price < ema20:
                    trends.append('bearish')
                else:
                    trends.append('neutral')
        
        if not trends:
            return 'neutral'
        
        # 如果所有时间框架趋势一致
        if all(t == 'bullish' for t in trends):
            return 'bullish'
        elif all(t == 'bearish' for t in trends):
            return 'bearish'
        else:
            return 'neutral'
    
    def calculate_signal_strength(self, indicators: Dict[str, float]) -> float:
        """
        计算信号强度（0-1）
        
        Args:
            indicators: 技术指标
            
        Returns:
            信号强度
        """
        strength = 0.5  # 基础强度
        
        # RSI贡献
        if 'rsi14' in indicators:
            rsi = indicators['rsi14']
            if rsi < 30:  # 超卖
                strength += 0.2
            elif rsi > 70:  # 超买
                strength -= 0.2
        
        # MACD贡献
        if 'macd' in indicators and 'macd_signal' in indicators:
            macd = indicators['macd']
            signal = indicators['macd_signal']
            if macd > signal:  # 金叉
                strength += 0.15
            else:  # 死叉
                strength -= 0.15
        
        # 成交量贡献
        if 'volume_ratio' in indicators:
            vol_ratio = indicators['volume_ratio']
            if vol_ratio > 1.5:  # 放量
                strength += 0.15
        
        return max(0, min(1, strength))
    
    @abstractmethod
    def generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易信号（子类必须实现）
        
        Args:
            market_data: 增强版市场数据
            
        Returns:
            交易信号
        """
        pass
    
    @abstractmethod
    def calculate_position_size(self, signal: Dict[str, Any], 
                              account_balance: float) -> float:
        """
        计算仓位大小（子类必须实现）
        
        Args:
            signal: 交易信号
            account_balance: 账户余额
            
        Returns:
            仓位大小
        """
        pass
    
    def update_performance(self, trade_result: Dict[str, Any]):
        """
        更新策略性能指标
        
        Args:
            trade_result: 交易结果
        """
        if 'total_return' in trade_result:
            self.performance_metrics['total_return'] = trade_result['total_return']
        if 'sharpe_ratio' in trade_result:
            self.performance_metrics['sharpe_ratio'] = trade_result['sharpe_ratio']
        if 'win_rate' in trade_result:
            self.performance_metrics['win_rate'] = trade_result['win_rate']
