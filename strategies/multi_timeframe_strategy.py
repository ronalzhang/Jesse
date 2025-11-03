"""
多时间框架趋势策略
利用多时间框架和技术指标进行交易决策
"""

from typing import Dict, Any
from strategies.enhanced_strategy_base import EnhancedStrategyBase

class MultiTimeframeStrategy(EnhancedStrategyBase):
    """多时间框架趋势策略"""
    
    def __init__(self, name: str = "MultiTimeframe", parameters: Dict[str, Any] = None):
        """初始化策略"""
        default_params = {
            'timeframes': ['15m', '1h', '4h'],
            'primary_timeframe': '1h',
            'use_indicators': True,
            'use_derivatives': True,
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            'min_signal_strength': 0.6,
            'position_size_pct': 0.02  # 2%仓位
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(name, default_params)
    
    def generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易信号
        
        Args:
            market_data: 增强版市场数据
            
        Returns:
            交易信号
        """
        signal = {
            'action': 'hold',
            'strength': 0.5,
            'reason': [],
            'indicators_used': []
        }
        
        # 获取主时间框架指标
        primary_indicators = self.extract_indicators(market_data, self.primary_timeframe)
        
        if not primary_indicators:
            signal['reason'].append('缺少主时间框架数据')
            return signal
        
        # 获取多时间框架指标
        mtf_indicators = self.get_multi_timeframe_indicators(market_data)
        
        # 检查趋势一致性
        trend = self.check_trend_alignment(mtf_indicators)
        signal['trend'] = trend
        
        # 计算信号强度
        strength = self.calculate_signal_strength(primary_indicators)
        signal['strength'] = strength
        
        # 决策逻辑
        current_price = primary_indicators.get('current_price', 0)
        rsi14 = primary_indicators.get('rsi14', 50)
        macd = primary_indicators.get('macd', 0)
        macd_signal = primary_indicators.get('macd_signal', 0)
        
        # 做多条件
        if (trend == 'bullish' and 
            rsi14 < self.parameters['rsi_oversold'] and 
            macd > macd_signal and
            strength >= self.parameters['min_signal_strength']):
            
            signal['action'] = 'buy'
            signal['reason'].append(f'多时间框架看涨趋势')
            signal['reason'].append(f'RSI超卖: {rsi14:.2f}')
            signal['reason'].append(f'MACD金叉')
            signal['indicators_used'] = ['trend', 'rsi14', 'macd']
        
        # 做空条件
        elif (trend == 'bearish' and 
              rsi14 > self.parameters['rsi_overbought'] and 
              macd < macd_signal and
              strength >= self.parameters['min_signal_strength']):
            
            signal['action'] = 'sell'
            signal['reason'].append(f'多时间框架看跌趋势')
            signal['reason'].append(f'RSI超买: {rsi14:.2f}')
            signal['reason'].append(f'MACD死叉')
            signal['indicators_used'] = ['trend', 'rsi14', 'macd']
        
        # 添加衍生品数据分析
        if self.use_derivatives:
            derivatives = self.extract_derivatives_data(market_data)
            
            if 'funding_metrics' in derivatives:
                fm = derivatives['funding_metrics']
                sentiment = fm.get('sentiment', 'neutral')
                
                # 资金费率确认信号
                if signal['action'] == 'buy' and sentiment == 'bullish':
                    signal['strength'] += 0.1
                    signal['reason'].append(f'资金费率确认看涨')
                elif signal['action'] == 'sell' and sentiment == 'bearish':
                    signal['strength'] += 0.1
                    signal['reason'].append(f'资金费率确认看跌')
        
        signal['strength'] = min(1.0, signal['strength'])
        
        return signal
    
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
            return 0
        
        # 基础仓位
        base_size = account_balance * self.parameters['position_size_pct']
        
        # 根据信号强度调整
        strength = signal.get('strength', 0.5)
        adjusted_size = base_size * strength
        
        return adjusted_size
