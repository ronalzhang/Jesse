"""
布林带策略
"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime
from .base_strategy import BaseStrategy

class BollingerStrategy(BaseStrategy):
    """布林带策略"""
    
    def __init__(self, name: str = "Bollinger_Strategy", parameters: Dict[str, Any] = None):
        """
        初始化布林带策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        default_params = {
            'period': 20,
            'std_dev': 2,
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
            if len(prices) < self.parameters['period']:
                return self._create_no_signal("数据不足")
            
            # 计算布林带
            upper, middle, lower = self._calculate_bollinger_bands(prices)
            if upper is None or middle is None or lower is None:
                return self._create_no_signal("无法计算布林带")
            
            current_price = prices[-1]
            current_upper = upper[-1]
            current_middle = middle[-1]
            current_lower = lower[-1]
            
            # 生成信号
            signal = self._generate_bollinger_signal(
                current_price, current_upper, current_middle, current_lower
            )
            return signal
            
        except Exception as e:
            self.logger.error(f"生成布林带信号时出错: {e}")
            return self._create_no_signal(f"错误: {str(e)}")
    
    def _calculate_bollinger_bands(self, prices: List[float]) -> tuple:
        """
        计算布林带
        
        Args:
            prices: 价格列表
            
        Returns:
            (上轨, 中轨, 下轨)
        """
        if len(prices) < self.parameters['period']:
            return None, None, None
        
        period = self.parameters['period']
        std_dev = self.parameters['std_dev']
        
        upper_bands = []
        middle_bands = []
        lower_bands = []
        
        for i in range(period - 1, len(prices)):
            window = prices[i - period + 1:i + 1]
            sma = np.mean(window)
            std = np.std(window)
            
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            
            upper_bands.append(upper)
            middle_bands.append(sma)
            lower_bands.append(lower)
        
        return upper_bands, middle_bands, lower_bands
    
    def _generate_bollinger_signal(self, price: float, upper: float, 
                                  middle: float, lower: float) -> Dict[str, Any]:
        """
        基于布林带生成信号
        
        Args:
            price: 当前价格
            upper: 上轨
            middle: 中轨
            lower: 下轨
            
        Returns:
            交易信号
        """
        # 价格触及下轨（买入信号）
        if price <= lower:
            confidence = min((lower - price) / lower, 0.9)
            return {
                'action': 'buy',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'price_at_lower_band',
                'price': price,
                'upper': upper,
                'middle': middle,
                'lower': lower
            }
        
        # 价格触及上轨（卖出信号）
        elif price >= upper:
            confidence = min((price - upper) / upper, 0.9)
            return {
                'action': 'sell',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'price_at_upper_band',
                'price': price,
                'upper': upper,
                'middle': middle,
                'lower': lower
            }
        
        # 价格回归中轨
        elif abs(price - middle) / middle < 0.01:  # 1%以内
            if price > middle:
                return {
                    'action': 'sell',
                    'confidence': 0.6,
                    'timestamp': datetime.now().isoformat(),
                    'reason': 'price_at_middle_band',
                    'price': price,
                    'upper': upper,
                    'middle': middle,
                    'lower': lower
                }
            else:
                return {
                    'action': 'buy',
                    'confidence': 0.6,
                    'timestamp': datetime.now().isoformat(),
                    'reason': 'price_at_middle_band',
                    'price': price,
                    'upper': upper,
                    'middle': middle,
                    'lower': lower
                }
        
        # 无信号
        else:
            return self._create_no_signal("价格在布林带中间区域")
    
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
            'type': 'Bollinger_Bands',
            'parameters': self.parameters,
            'description': '基于布林带的交易策略',
            'is_active': self.is_active
        } 