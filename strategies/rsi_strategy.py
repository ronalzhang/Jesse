"""
RSI策略
"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime
from .base_strategy import BaseStrategy

class RSIStrategy(BaseStrategy):
    """RSI策略"""
    
    def __init__(self, name: str = "RSI_Strategy", parameters: Dict[str, Any] = None):
        """
        初始化RSI策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        default_params = {
            'period': 14,
            'oversold_threshold': 30,
            'overbought_threshold': 70,
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
            if len(prices) < self.parameters['period'] + 1:
                return self._create_no_signal("数据不足")
            
            # 计算RSI
            rsi = self._calculate_rsi(prices, self.parameters['period'])
            if rsi is None:
                return self._create_no_signal("无法计算RSI")
            
            current_rsi = rsi[-1]
            prev_rsi = rsi[-2] if len(rsi) > 1 else current_rsi
            
            # 生成信号
            signal = self._generate_rsi_signal(current_rsi, prev_rsi)
            return signal
            
        except Exception as e:
            self.logger.error(f"生成RSI信号时出错: {e}")
            return self._create_no_signal(f"错误: {str(e)}")
    
    def _calculate_rsi(self, prices: List[float], period: int) -> List[float]:
        """
        计算RSI
        
        Args:
            prices: 价格列表
            period: RSI周期
            
        Returns:
            RSI值列表
        """
        if len(prices) < period + 1:
            return None
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        rsi_values = []
        for i in range(period, len(prices)):
            avg_gain = np.mean(gains[i-period:i])
            avg_loss = np.mean(losses[i-period:i])
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            rsi_values.append(rsi)
        
        return rsi_values
    
    def _generate_rsi_signal(self, current_rsi: float, prev_rsi: float) -> Dict[str, Any]:
        """
        基于RSI生成信号
        
        Args:
            current_rsi: 当前RSI值
            prev_rsi: 前一个RSI值
            
        Returns:
            交易信号
        """
        oversold = self.parameters['oversold_threshold']
        overbought = self.parameters['overbought_threshold']
        
        # 超卖信号（买入）
        if current_rsi < oversold and prev_rsi >= oversold:
            confidence = min((oversold - current_rsi) / oversold, 0.9)
            return {
                'action': 'buy',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'oversold',
                'rsi': current_rsi
            }
        
        # 超买信号（卖出）
        elif current_rsi > overbought and prev_rsi <= overbought:
            confidence = min((current_rsi - overbought) / (100 - overbought), 0.9)
            return {
                'action': 'sell',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'overbought',
                'rsi': current_rsi
            }
        
        # 无信号
        else:
            return self._create_no_signal("RSI在正常范围内")
    
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
            'type': 'RSI',
            'parameters': self.parameters,
            'description': '基于相对强弱指数(RSI)的交易策略',
            'is_active': self.is_active
        } 