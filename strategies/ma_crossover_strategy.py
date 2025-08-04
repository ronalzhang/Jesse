"""
移动平均线交叉策略
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
from .base_strategy import BaseStrategy

class MACrossoverStrategy(BaseStrategy):
    """移动平均线交叉策略"""
    
    def __init__(self, name: str = "MA_Crossover", parameters: Dict[str, Any] = None):
        """
        初始化移动平均线交叉策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        default_params = {
            'short_window': 5,
            'long_window': 20,
            'position_size': 0.1,  # 仓位比例
            'stop_loss': 0.05,     # 止损比例
            'take_profit': 0.15    # 止盈比例
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
            # 获取价格数据
            prices = market_data.get('close', [])
            if len(prices) < self.parameters['long_window']:
                return self._create_no_signal("数据不足")
            
            # 计算移动平均线
            short_ma = self._calculate_ma(prices, self.parameters['short_window'])
            long_ma = self._calculate_ma(prices, self.parameters['long_window'])
            
            if short_ma is None or long_ma is None:
                return self._create_no_signal("无法计算移动平均线")
            
            # 获取当前和前一个值
            current_short = short_ma[-1]
            current_long = long_ma[-1]
            prev_short = short_ma[-2] if len(short_ma) > 1 else current_short
            prev_long = long_ma[-2] if len(long_ma) > 1 else current_long
            
            # 判断交叉信号
            signal = self._detect_crossover(
                current_short, current_long, prev_short, prev_long
            )
            
            return signal
            
        except Exception as e:
            self.logger.error(f"生成信号时出错: {e}")
            return self._create_no_signal(f"错误: {str(e)}")
    
    def _calculate_ma(self, prices: List[float], window: int) -> List[float]:
        """
        计算移动平均线
        
        Args:
            prices: 价格列表
            window: 窗口大小
            
        Returns:
            移动平均线列表
        """
        if len(prices) < window:
            return None
        
        ma_values = []
        for i in range(window - 1, len(prices)):
            ma = np.mean(prices[i - window + 1:i + 1])
            ma_values.append(ma)
        
        return ma_values
    
    def _detect_crossover(self, current_short: float, current_long: float,
                         prev_short: float, prev_long: float) -> Dict[str, Any]:
        """
        检测交叉信号
        
        Args:
            current_short: 当前短期MA
            current_long: 当前长期MA
            prev_short: 前一个短期MA
            prev_long: 前一个长期MA
            
        Returns:
            交易信号
        """
        # 金叉：短期MA从下方穿越长期MA
        if prev_short <= prev_long and current_short > current_long:
            confidence = min(abs(current_short - current_long) / current_long, 0.9)
            return {
                'action': 'buy',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'golden_cross',
                'short_ma': current_short,
                'long_ma': current_long
            }
        
        # 死叉：短期MA从上方穿越长期MA
        elif prev_short >= prev_long and current_short < current_long:
            confidence = min(abs(current_short - current_long) / current_long, 0.9)
            return {
                'action': 'sell',
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'reason': 'death_cross',
                'short_ma': current_short,
                'long_ma': current_long
            }
        
        # 无信号
        else:
            return self._create_no_signal("无交叉信号")
    
    def _create_no_signal(self, reason: str) -> Dict[str, Any]:
        """
        创建无信号响应
        
        Args:
            reason: 无信号原因
            
        Returns:
            无信号响应
        """
        return {
            'action': 'hold',
            'confidence': 0.0,
            'timestamp': datetime.now().isoformat(),
            'reason': reason
        }
    
    def calculate_position_size(self, signal: Dict[str, Any], 
                              account_balance: float) -> float:
        """
        计算仓位大小
        
        Args:
            signal: 交易信号
            account_balance: 账户余额
            
        Returns:
            仓位大小
        """
        if signal['action'] == 'hold':
            return 0.0
        
        # 基于信号置信度调整仓位
        base_position = self.parameters['position_size']
        confidence_factor = signal['confidence']
        
        # 计算最终仓位
        position_size = base_position * confidence_factor * account_balance
        
        # 应用止损和止盈限制
        if signal['action'] == 'buy':
            max_position = account_balance * (1 - self.parameters['stop_loss'])
            position_size = min(position_size, max_position)
        elif signal['action'] == 'sell':
            max_position = account_balance * (1 + self.parameters['take_profit'])
            position_size = min(position_size, max_position)
        
        return max(0.0, position_size)
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """
        获取策略信息
        
        Returns:
            策略信息
        """
        return {
            'name': self.name,
            'type': 'MA_Crossover',
            'parameters': self.parameters,
            'description': '基于短期和长期移动平均线交叉的交易策略',
            'is_active': self.is_active
        } 