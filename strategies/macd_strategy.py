"""
MACD策略
"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime
from .base_strategy import BaseStrategy

class MACDStrategy(BaseStrategy):
    """MACD策略"""
    
    def __init__(self, name: str = "MACD_Strategy", parameters: Dict[str, Any] = None):
        """
        初始化MACD策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        default_params = {
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9,
            'position_size': 0.1,
            'stop_loss': 0.05,
            'take_profit': 0.15
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(name, default_params)
    
    def generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易信号
        
        Args:
            market_data: 市场数据
            
        Returns:
            交易信号
        """
        try:
            prices = market_data.get('close', [])
            if len(prices) < self.parameters['slow_period'] + self.parameters['signal_period']:
                return self._create_no_signal("数据不足")
            
            # 计算MACD
            macd, signal, histogram = self._calculate_macd(prices)
            if macd is None or signal is None:
                return self._create_no_signal("无法计算MACD")
            
            # 生成信号
            signal_result = self._generate_macd_signal(macd, signal, histogram)
            return signal_result
            
        except Exception as e:
            self.logger.error(f"生成MACD信号时出错: {e}")
            return self._create_no_signal(f"错误: {str(e)}")
    
    def _calculate_macd(self, prices: List[float]) -> tuple:
        """
        计算MACD
        
        Args:
            prices: 价格列表
            
        Returns:
            (MACD线, 信号线, 柱状图)
        """
        if len(prices) < self.parameters['slow_period']:
            return None, None, None
        
        # 计算EMA
        fast_ema = self._calculate_ema(prices, self.parameters['fast_period'])
        slow_ema = self._calculate_ema(prices, self.parameters['slow_period'])
        
        if fast_ema is None or slow_ema is None:
            return None, None, None
        
        # 计算MACD线
        macd_line = fast_ema - slow_ema
        
        # 计算信号线
        signal_line = self._calculate_ema(macd_line, self.parameters['signal_period'])
        
        # 计算柱状图
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def _calculate_ema(self, data: List[float], period: int) -> List[float]:
        """
        计算指数移动平均线
        
        Args:
            data: 数据列表
            period: 周期
            
        Returns:
            EMA值列表
        """
        if len(data) < period:
            return None
        
        ema_values = []
        multiplier = 2 / (period + 1)
        
        # 第一个EMA使用简单移动平均
        ema = np.mean(data[:period])
        ema_values.append(ema)
        
        # 计算后续的EMA
        for i in range(period, len(data)):
            ema = (data[i] * multiplier) + (ema * (1 - multiplier))
            ema_values.append(ema)
        
        return ema_values
    
    def _generate_macd_signal(self, macd: List[float], signal: List[float], 
                             histogram: List[float]) -> Dict[str, Any]:
        """
        基于MACD生成信号
        
        Args:
            macd: MACD线
            signal: 信号线
            histogram: 柱状图
            
        Returns:
            交易信号
        """
        if len(macd) < 2 or len(signal) < 2:
            return self._create_no_signal("MACD数据不足")
        
        current_macd = macd[-1]
        prev_macd = macd[-2]
        current_signal = signal[-1]
        prev_signal = signal[-2]
        current_histogram = histogram[-1]
        prev_histogram = histogram[-2]
        
        # MACD金叉
        if prev_macd <= prev_signal and current_macd > current_signal:
            confidence = min(abs(current_macd - current_signal) / abs(current_signal), 0.9)
            return {
                'action': 'buy',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'macd_golden_cross',
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram
            }
        
        # MACD死叉
        elif prev_macd >= prev_signal and current_macd < current_signal:
            confidence = min(abs(current_macd - current_signal) / abs(current_signal), 0.9)
            return {
                'action': 'sell',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'macd_death_cross',
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram
            }
        
        # 柱状图反转信号
        elif prev_histogram < 0 and current_histogram > 0:
            confidence = min(abs(current_histogram), 0.8)
            return {
                'action': 'buy',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'histogram_bullish_divergence',
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram
            }
        
        elif prev_histogram > 0 and current_histogram < 0:
            confidence = min(abs(current_histogram), 0.8)
            return {
                'action': 'sell',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'histogram_bearish_divergence',
                'macd': current_macd,
                'signal': current_signal,
                'histogram': current_histogram
            }
        
        # 无信号
        else:
            return self._create_no_signal("无MACD信号")
    
    def _create_no_signal(self, reason: str) -> Dict[str, Any]:
        """创建无信号响应"""
        return {
            'action': 'hold',
            'confidence': 0.0,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        }
    
    def calculate_position_size(self, signal: Dict[str, Any], 
                              account_balance: float) -> float:
        """计算仓位大小"""
        if signal['action'] == 'hold':
            return 0.0
        
        base_position = self.parameters['position_size']
        confidence_factor = signal['confidence']
        
        position_size = base_position * confidence_factor * account_balance
        
        if signal['action'] == 'buy':
            max_position = account_balance * (1 - self.parameters['stop_loss'])
            position_size = min(position_size, max_position)
        elif signal['action'] == 'sell':
            max_position = account_balance * (1 + self.parameters['take_profit'])
            position_size = min(position_size, max_position)
        
        return max(0.0, position_size)
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """获取策略信息"""
        return {
            'name': self.name,
            'type': 'MACD',
            'parameters': self.parameters,
            'description': '基于MACD指标的交易策略',
            'is_active': self.is_active
        } 