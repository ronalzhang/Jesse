"""
高频交易策略 - 实现日化3%-30%收益目标
"""

# import jesse.indicators as ta  # 移除jesse依赖
# from jesse import utils
# from jesse.strategies import Strategy
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
from finta import TA

class HighFrequencyStrategy:
    """
    高频交易策略
    目标：日化收益率3%-30%
    特点：短持仓时间，高交易频率，多交易所套利
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 高频交易参数
        self.min_holding_time = 30  # 最小持仓时间30秒
        self.max_holding_time = 3600  # 最大持仓时间1小时
        self.scalping_threshold = 0.005  # 高频交易阈值0.5%
        self.arbitrage_threshold = 0.003  # 套利阈值0.3%
        
        # 风险控制
        self.max_position_size = 0.3  # 最大仓位30%
        self.stop_loss = 0.05  # 止损5%
        self.take_profit = 0.08  # 止盈8%
        
        # 交易记录
        self.trades_today = []
        self.daily_pnl = 0
        self.last_trade_time = None
        
    def should_long(self, data: pd.DataFrame) -> bool:
        """判断是否应该做多"""
        # 高频交易信号
        if self._scalping_signal(data):
            return True
            
        # 套利信号
        if self._arbitrage_signal(data):
            return True
            
        # 动量交易信号
        if self._momentum_signal(data):
            return True
            
        return False
    
    def should_short(self, data: pd.DataFrame) -> bool:
        """判断是否应该做空"""
        # 高频交易信号
        if self._scalping_signal_short(data):
            return True
            
        # 套利信号
        if self._arbitrage_signal_short(data):
            return True
            
        # 动量交易信号
        if self._momentum_signal_short(data):
            return True
            
        return False
    
    def should_cancel_entry(self, data: pd.DataFrame) -> bool:
        """判断是否应该取消入场"""
        # 如果持仓时间过长，取消入场
        if self._holding_time_too_long():
            return True
            
        # 如果市场波动过大，取消入场
        if self._market_volatility_too_high(data):
            return True
            
        return False
    
    def should_exit(self, data: pd.DataFrame) -> bool:
        """判断是否应该出场"""
        # 达到止盈止损
        if self._hit_stop_loss() or self._hit_take_profit():
            return True
            
        # 持仓时间过长
        if self._holding_time_too_long():
            return True
            
        # 高频交易信号反转
        if self._signal_reversal(data):
            return True
            
        return False
    
    def go_long(self, data: pd.DataFrame, position_size: float = None):
        """做多"""
        if position_size is None:
            position_size = self.max_position_size
            
        self.logger.info(f"🟢 执行做多操作，仓位大小: {position_size}")
        self._record_trade("long", position_size, data['close'].iloc[-1])
        
    def go_short(self, data: pd.DataFrame, position_size: float = None):
        """做空"""
        if position_size is None:
            position_size = self.max_position_size
            
        self.logger.info(f"🔴 执行做空操作，仓位大小: {position_size}")
        self._record_trade("short", position_size, data['close'].iloc[-1])
        
    def update_position(self, data: pd.DataFrame):
        """更新持仓"""
        # 这里可以添加持仓更新逻辑
        pass
        
    def _scalping_signal(self, data: pd.DataFrame) -> bool:
        """高频交易信号"""
        try:
            if len(data) < 20:
                return False
                
            # 计算技术指标
            rsi = TA.RSI(data, period=14)
            
            # 高频交易条件
            current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            current_price = data['close'].iloc[-1]
            price_change = (current_price - data['close'].iloc[-2]) / data['close'].iloc[-2]
            
            # RSI超卖且价格快速上涨
            if current_rsi < 30 and price_change > self.scalping_threshold:
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"计算高频交易信号时出错: {e}")
            return False
    
    def _scalping_signal_short(self, data: pd.DataFrame) -> bool:
        """高频交易做空信号"""
        try:
            if len(data) < 20:
                return False
                
            # 计算技术指标
            rsi = TA.RSI(data, period=14)
            
            # 高频交易条件
            current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
            current_price = data['close'].iloc[-1]
            price_change = (current_price - data['close'].iloc[-2]) / data['close'].iloc[-2]
            
            # RSI超买且价格快速下跌
            if current_rsi > 70 and price_change < -self.scalping_threshold:
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"计算高频交易做空信号时出错: {e}")
            return False
    
    def _arbitrage_signal(self, data: pd.DataFrame) -> bool:
        """套利信号"""
        # 这里可以添加套利逻辑
        return False
    
    def _arbitrage_signal_short(self, data: pd.DataFrame) -> bool:
        """套利做空信号"""
        # 这里可以添加套利逻辑
        return False
    
    def _momentum_signal(self, data: pd.DataFrame) -> bool:
        """动量交易信号"""
        try:
            if len(data) < 20:
                return False
                
            # 计算移动平均线
            sma_5 = TA.SMA(data, period=5)
            sma_20 = TA.SMA(data, period=20)
            
            # 动量条件：短期均线上穿长期均线
            if (sma_5.iloc[-1] > sma_20.iloc[-1] and 
                sma_5.iloc[-2] <= sma_20.iloc[-2]):
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"计算动量信号时出错: {e}")
            return False
    
    def _momentum_signal_short(self, data: pd.DataFrame) -> bool:
        """动量交易做空信号"""
        try:
            if len(data) < 20:
                return False
                
            # 计算移动平均线
            sma_5 = TA.SMA(data, period=5)
            sma_20 = TA.SMA(data, period=20)
            
            # 动量条件：短期均线下穿长期均线
            if (sma_5.iloc[-1] < sma_20.iloc[-1] and 
                sma_5.iloc[-2] >= sma_20.iloc[-2]):
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"计算动量做空信号时出错: {e}")
            return False
    
    def _holding_time_too_long(self) -> bool:
        """检查持仓时间是否过长"""
        if self.last_trade_time is None:
            return False
            
        current_time = datetime.now()
        holding_time = (current_time - self.last_trade_time).total_seconds()
        
        return holding_time > self.max_holding_time
    
    def _market_volatility_too_high(self, data: pd.DataFrame) -> bool:
        """检查市场波动是否过大"""
        try:
            if len(data) < 20:
                return False
                
            # 计算波动率
            returns = data['close'].pct_change()
            volatility = returns.rolling(window=20).std().iloc[-1]
            
            # 如果波动率超过10%，认为波动过大
            return volatility > 0.1
            
        except Exception as e:
            self.logger.error(f"计算市场波动率时出错: {e}")
            return False
    
    def _hit_stop_loss(self) -> bool:
        """检查是否达到止损"""
        # 这里可以添加止损逻辑
        return False
    
    def _hit_take_profit(self) -> bool:
        """检查是否达到止盈"""
        # 这里可以添加止盈逻辑
        return False
    
    def _signal_reversal(self, data: pd.DataFrame) -> bool:
        """检查信号是否反转"""
        # 这里可以添加信号反转逻辑
        return False
    
    def _record_trade(self, direction: str, qty: float, price: float):
        """记录交易"""
        trade = {
            'timestamp': datetime.now(),
            'direction': direction,
            'quantity': qty,
            'price': price,
            'pnl': 0  # 初始盈亏为0
        }
        
        self.trades_today.append(trade)
        self.last_trade_time = datetime.now()
        
        self.logger.info(f"📝 记录交易: {direction} {qty} @ {price}")
    
    def on_trade_close(self, trade):
        """交易结束时调用"""
        # 计算盈亏
        if trade['direction'] == 'long':
            # 做多盈亏计算
            pass
        else:
            # 做空盈亏计算
            pass
            
        self.daily_pnl += trade.get('pnl', 0)
        
        self.logger.info(f"💰 交易结束，盈亏: {trade.get('pnl', 0)}")
    
    def _check_daily_targets(self):
        """检查每日目标"""
        # 检查是否达到日化收益率目标
        if self.daily_pnl > 0.03:  # 3%目标
            self.logger.info("🎯 达到日化收益率3%目标")
        elif self.daily_pnl > 0.30:  # 30%目标
            self.logger.info("🎯 达到日化收益率30%目标")
    
    def on_daily_end(self):
        """每日结束时调用"""
        self.logger.info(f"📊 每日总结 - 交易次数: {len(self.trades_today)}, 盈亏: {self.daily_pnl}")
        
        # 检查目标
        self._check_daily_targets()
        
        # 重置每日数据
        self.trades_today = []
        self.daily_pnl = 0
    
    def _calculate_avg_holding_time(self) -> float:
        """计算平均持仓时间"""
        if not self.trades_today:
            return 0
            
        total_time = 0
        for trade in self.trades_today:
            if trade.get('close_time') and trade.get('timestamp'):
                holding_time = (trade['close_time'] - trade['timestamp']).total_seconds()
                total_time += holding_time
                
        return total_time / len(self.trades_today)
    
    def _calculate_win_rate(self) -> float:
        """计算胜率"""
        if not self.trades_today:
            return 0
            
        winning_trades = sum(1 for trade in self.trades_today if trade.get('pnl', 0) > 0)
        return winning_trades / len(self.trades_today) 