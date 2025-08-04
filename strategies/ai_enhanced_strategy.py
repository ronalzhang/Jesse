"""
AI增强策略
"""

import numpy as np
from typing import Dict, List, Any
from datetime import datetime
from .base_strategy import BaseStrategy
from .ma_crossover_strategy import MACrossoverStrategy
from .rsi_strategy import RSIStrategy
from .macd_strategy import MACDStrategy
from .bollinger_strategy import BollingerStrategy

class AIEnhancedStrategy(BaseStrategy):
    """AI增强策略"""
    
    def __init__(self, name: str = "AI_Enhanced_Strategy", parameters: Dict[str, Any] = None):
        """
        初始化AI增强策略
        
        Args:
            name: 策略名称
            parameters: 策略参数
        """
        default_params = {
            'position_size': 0.1,
            'stop_loss': 0.05,
            'take_profit': 0.15,
            'ai_confidence_threshold': 0.7,
            'ensemble_weights': {
                'ma_crossover': 0.25,
                'rsi': 0.25,
                'macd': 0.25,
                'bollinger': 0.25
            }
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(name, default_params)
        
        # 初始化子策略
        self.sub_strategies = {
            'ma_crossover': MACrossoverStrategy(),
            'rsi': RSIStrategy(),
            'macd': MACDStrategy(),
            'bollinger': BollingerStrategy()
        }
    
    def generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成AI增强的交易信号
        
        Args:
            market_data: 市场数据
            
        Returns:
            交易信号
        """
        try:
            # 获取各个子策略的信号
            sub_signals = {}
            for name, strategy in self.sub_strategies.items():
                if strategy.is_active:
                    signal = strategy.generate_signals(market_data)
                    sub_signals[name] = signal
            
            if not sub_signals:
                return self._create_no_signal("没有活跃的子策略")
            
            # 结合AI分析
            ai_analysis = market_data.get('ai_analysis', {})
            
            # 生成综合信号
            combined_signal = self._combine_signals(sub_signals, ai_analysis)
            
            return combined_signal
            
        except Exception as e:
            self.logger.error(f"生成AI增强信号时出错: {e}")
            return self._create_no_signal(f"错误: {str(e)}")
    
    def _combine_signals(self, sub_signals: Dict[str, Dict], 
                         ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        结合多个策略的信号和AI分析
        
        Args:
            sub_signals: 子策略信号
            ai_analysis: AI分析结果
            
        Returns:
            综合信号
        """
        # 计算加权信号
        weighted_action = 0.0
        total_confidence = 0.0
        total_weight = 0.0
        
        action_scores = {'buy': 1, 'sell': -1, 'hold': 0}
        
        for strategy_name, signal in sub_signals.items():
            weight = self.parameters['ensemble_weights'].get(strategy_name, 0.25)
            action_score = action_scores.get(signal['action'], 0)
            confidence = signal.get('confidence', 0.0)
            
            weighted_action += action_score * confidence * weight
            total_confidence += confidence * weight
            total_weight += weight
        
        # 应用AI增强
        ai_enhancement = self._apply_ai_enhancement(ai_analysis)
        
        # 确定最终动作
        if total_weight > 0:
            avg_weighted_action = weighted_action / total_weight
            avg_confidence = total_confidence / total_weight
            
            # 结合AI增强
            final_confidence = min(avg_confidence * ai_enhancement, 0.95)
            
            if final_confidence >= self.parameters['ai_confidence_threshold']:
                if avg_weighted_action > 0.3:
                    action = 'buy'
                elif avg_weighted_action < -0.3:
                    action = 'sell'
                else:
                    action = 'hold'
            else:
                action = 'hold'
        else:
            action = 'hold'
            final_confidence = 0.0
        
        return {
            'action': action,
            'confidence': final_confidence,
            'timestamp': datetime.now().isoformat(),
            'reason': 'ai_enhanced_ensemble',
            'sub_signals': sub_signals,
            'ai_enhancement': ai_enhancement,
            'weighted_action': weighted_action if total_weight > 0 else 0.0
        }
    
    def _apply_ai_enhancement(self, ai_analysis: Dict[str, Any]) -> float:
        """
        应用AI增强
        
        Args:
            ai_analysis: AI分析结果
            
        Returns:
            AI增强系数
        """
        if not ai_analysis:
            return 1.0
        
        enhancement = 1.0
        
        # 情感分析增强
        sentiment = ai_analysis.get('sentiment', {})
        if sentiment:
            sentiment_score = sentiment.get('score', 0.0)
            enhancement *= (1.0 + sentiment_score * 0.2)
        
        # 技术分析增强
        technical = ai_analysis.get('technical', {})
        if technical:
            technical_score = technical.get('score', 0.0)
            enhancement *= (1.0 + technical_score * 0.15)
        
        # 预测增强
        predictions = ai_analysis.get('predictions', {})
        if predictions:
            prediction_confidence = predictions.get('confidence', 0.5)
            enhancement *= (1.0 + prediction_confidence * 0.1)
        
        # 趋势分析增强
        trends = ai_analysis.get('trends', {})
        if trends:
            trend_strength = trends.get('strength', 0.0)
            enhancement *= (1.0 + trend_strength * 0.1)
        
        return max(0.5, min(2.0, enhancement))  # 限制在0.5-2.0之间
    
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
        ai_enhancement = signal.get('ai_enhancement', 1.0)
        
        # 应用AI增强的仓位计算
        position_size = base_position * confidence_factor * ai_enhancement * account_balance
        
        if signal['action'] == 'buy':
            max_position = account_balance * (1 - self.parameters['stop_loss'])
            position_size = min(position_size, max_position)
        elif signal['action'] == 'sell':
            max_position = account_balance * (1 + self.parameters['take_profit'])
            position_size = min(position_size, max_position)
        
        return max(0.0, position_size)
    
    def update_sub_strategy_parameters(self, strategy_name: str, 
                                     parameters: Dict[str, Any]) -> None:
        """
        更新子策略参数
        
        Args:
            strategy_name: 策略名称
            parameters: 新参数
        """
        if strategy_name in self.sub_strategies:
            self.sub_strategies[strategy_name].update_parameters(parameters)
            self.logger.info(f"子策略 {strategy_name} 参数已更新")
    
    def get_sub_strategies_info(self) -> Dict[str, Any]:
        """
        获取子策略信息
        
        Returns:
            子策略信息
        """
        info = {}
        for name, strategy in self.sub_strategies.items():
            info[name] = {
                'name': strategy.name,
                'type': strategy.__class__.__name__,
                'is_active': strategy.is_active,
                'parameters': strategy.get_parameters(),
                'performance': strategy.get_performance()
            }
        return info
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """获取策略信息"""
        return {
            'name': self.name,
            'type': 'AI_Enhanced_Ensemble',
            'parameters': self.parameters,
            'description': '结合多个传统策略和AI分析的增强策略',
            'is_active': self.is_active,
            'sub_strategies': self.get_sub_strategies_info()
        } 