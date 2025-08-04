"""
基础策略类
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from utils.logging_manager import LoggerMixin

class BaseStrategy(ABC, LoggerMixin):
    """基础策略类"""
    
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
        
    @abstractmethod
    def generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易信号
        
        Args:
            market_data: 市场数据
            
        Returns:
            交易信号
        """
        pass
    
    @abstractmethod
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
        pass
    
    def update_parameters(self, new_parameters: Dict[str, Any]) -> None:
        """
        更新策略参数
        
        Args:
            new_parameters: 新参数
        """
        self.parameters.update(new_parameters)
        self.logger.info(f"策略 {self.name} 参数已更新")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        获取策略参数
        
        Returns:
            策略参数
        """
        return self.parameters.copy()
    
    def activate(self) -> None:
        """激活策略"""
        self.is_active = True
        self.logger.info(f"策略 {self.name} 已激活")
    
    def deactivate(self) -> None:
        """停用策略"""
        self.is_active = False
        self.logger.info(f"策略 {self.name} 已停用")
    
    def update_performance(self, metrics: Dict[str, Any]) -> None:
        """
        更新性能指标
        
        Args:
            metrics: 性能指标
        """
        self.performance_metrics.update(metrics)
    
    def get_performance(self) -> Dict[str, Any]:
        """
        获取性能指标
        
        Returns:
            性能指标
        """
        return self.performance_metrics.copy()
    
    def validate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        验证交易信号
        
        Args:
            signal: 交易信号
            
        Returns:
            信号是否有效
        """
        required_keys = ['action', 'confidence', 'timestamp']
        return all(key in signal for key in required_keys)
    
    def calculate_risk_metrics(self, returns: List[float]) -> Dict[str, float]:
        """
        计算风险指标
        
        Args:
            returns: 收益率列表
            
        Returns:
            风险指标
        """
        if not returns:
            return {
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'volatility': 0.0,
                'total_return': 0.0
            }
        
        import numpy as np
        from utils.helpers import calculate_sharpe_ratio, calculate_max_drawdown, calculate_volatility
        
        returns_array = np.array(returns)
        total_return = np.prod(1 + returns_array) - 1
        
        return {
            'sharpe_ratio': calculate_sharpe_ratio(returns),
            'max_drawdown': calculate_max_drawdown(returns),
            'volatility': calculate_volatility(returns),
            'total_return': total_return
        }
    
    def __str__(self) -> str:
        return f"{self.name} (Active: {self.is_active})"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>" 