"""
高频交易策略 - 实现日化3%-30%收益目标
"""

import jesse.indicators as ta
from jesse import utils
from jesse.strategies import Strategy
import numpy as np
from datetime import datetime, timedelta
import logging

class HighFrequencyStrategy(Strategy):
    """
    高频交易策略
    目标：日化收益率3%-30%
    特点：短持仓时间，高交易频率，多交易所套利
    """
    
    def __init__(self):
        super().__init__()
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
        
    def should_long(self) -> bool:
        """判断是否应该做多"""
        # 高频交易信号
        if self._scalping_signal():
            return True
            
        # 套利信号
        if self._arbitrage_signal():
            return True
            
        # 动量交易信号
        if self._momentum_signal():
            return True
            
        return False
    
    def should_short(self) -> bool:
        """判断是否应该做空"""
        # 高频交易信号
        if self._scalping_signal_short():
            return True
            
        # 套利信号
        if self._arbitrage_signal_short():
            return True
            
        # 动量交易信号
        if self._momentum_signal_short():
            return True
            
        return False
    
    def should_cancel_entry(self) -> bool:
        """判断是否应该取消入场"""
        # 如果持仓时间过长，取消入场
        if self._holding_time_too_long():
            return True
            
        # 如果市场波动过大，取消入场
        if self._market_volatility_too_high():
            return True
            
        return False
    
    def should_exit(self) -> bool:
        """判断是否应该出场"""
        # 达到止盈止损
        if self._hit_stop_loss() or self._hit_take_profit():
            return True
            
        # 持仓时间过长
        if self._holding_time_too_long():
            return True
            
        # 高频交易信号反转
        if self._signal_reversal():
            return True
            
        return False
    
    def go_long(self):
        """做多"""
        # 计算仓位大小
        qty = utils.size_to_qty(self.capital * self.max_position_size, self.price, fee_rate=self.fee_rate)
        
        # 执行买入
        self.buy = qty, self.price
        
        # 记录交易
        self._record_trade('LONG', qty, self.price)
        
    def go_short(self):
        """做空"""
        # 计算仓位大小
        qty = utils.size_to_qty(self.capital * self.max_position_size, self.price, fee_rate=self.fee_rate)
        
        # 执行卖出
        self.sell = qty, self.price
        
        # 记录交易
        self._record_trade('SHORT', qty, self.price)
    
    def update_position(self):
        """更新持仓"""
        # 检查是否需要出场
        if self.should_exit():
            self.liquidate()
    
    def _scalping_signal(self) -> bool:
        """高频交易信号"""
        # 计算短期技术指标
        rsi = ta.rsi(self.candles, period=14)
        macd = ta.macd(self.candles)
        bb = ta.bollinger_bands(self.candles, period=20)
        
        # 高频交易条件
        price_change = (self.price - self.candles[-2]['close']) / self.candles[-2]['close']
        
        # RSI超卖 + MACD金叉 + 价格突破布林带下轨
        if (rsi[-1] < 30 and 
            macd['macd'][-1] > macd['macd'][-2] and 
            self.price > bb['lower'][-1] and
            abs(price_change) > self.scalping_threshold):
            return True
            
        return False
    
    def _scalping_signal_short(self) -> bool:
        """高频交易做空信号"""
        rsi = ta.rsi(self.candles, period=14)
        macd = ta.macd(self.candles)
        bb = ta.bollinger_bands(self.candles, period=20)
        
        price_change = (self.price - self.candles[-2]['close']) / self.candles[-2]['close']
        
        # RSI超买 + MACD死叉 + 价格跌破布林带上轨
        if (rsi[-1] > 70 and 
            macd['macd'][-1] < macd['macd'][-2] and 
            self.price < bb['upper'][-1] and
            abs(price_change) > self.scalping_threshold):
            return True
            
        return False
    
    def _arbitrage_signal(self) -> bool:
        """套利信号"""
        # 这里需要多交易所价格数据
        # 暂时使用单交易所的价差信号
        price_change = (self.price - self.candles[-2]['close']) / self.candles[-2]['close']
        
        if abs(price_change) > self.arbitrage_threshold:
            return True
            
        return False
    
    def _arbitrage_signal_short(self) -> bool:
        """套利做空信号"""
        price_change = (self.price - self.candles[-2]['close']) / self.candles[-2]['close']
        
        if abs(price_change) > self.arbitrage_threshold:
            return True
            
        return False
    
    def _momentum_signal(self) -> bool:
        """动量交易信号"""
        # 计算动量指标
        momentum = ta.momentum(self.candles, period=10)
        volume = ta.volume_sma(self.candles, period=20)
        
        # 动量向上 + 成交量放大
        if (momentum[-1] > momentum[-2] and 
            self.candles[-1]['volume'] > volume[-1] * 1.5):
            return True
            
        return False
    
    def _momentum_signal_short(self) -> bool:
        """动量做空信号"""
        momentum = ta.momentum(self.candles, period=10)
        volume = ta.volume_sma(self.candles, period=20)
        
        # 动量向下 + 成交量放大
        if (momentum[-1] < momentum[-2] and 
            self.candles[-1]['volume'] > volume[-1] * 1.5):
            return True
            
        return False
    
    def _holding_time_too_long(self) -> bool:
        """检查持仓时间是否过长"""
        if self.position.is_open:
            holding_time = (datetime.now() - self.position.opened_at).total_seconds()
            return holding_time > self.max_holding_time
        return False
    
    def _market_volatility_too_high(self) -> bool:
        """检查市场波动是否过大"""
        atr = ta.atr(self.candles, period=14)
        current_atr = atr[-1]
        avg_atr = np.mean(atr[-20:])
        
        return current_atr > avg_atr * 2
    
    def _hit_stop_loss(self) -> bool:
        """检查是否触发止损"""
        if self.position.is_open:
            if self.position.is_long:
                return self.price <= self.position.entry_price * (1 - self.stop_loss)
            else:
                return self.price >= self.position.entry_price * (1 + self.stop_loss)
        return False
    
    def _hit_take_profit(self) -> bool:
        """检查是否触发止盈"""
        if self.position.is_open:
            if self.position.is_long:
                return self.price >= self.position.entry_price * (1 + self.take_profit)
            else:
                return self.price <= self.position.entry_price * (1 - self.take_profit)
        return False
    
    def _signal_reversal(self) -> bool:
        """检查信号是否反转"""
        if not self.position.is_open:
            return False
            
        # 简单的信号反转检查
        rsi = ta.rsi(self.candles, period=14)
        
        if self.position.is_long:
            return rsi[-1] > 70  # 超买反转
        else:
            return rsi[-1] < 30  # 超卖反转
    
    def _record_trade(self, direction: str, qty: float, price: float):
        """记录交易"""
        trade = {
            'timestamp': datetime.now(),
            'direction': direction,
            'qty': qty,
            'price': price,
            'symbol': self.symbol,
            'exchange': self.exchange
        }
        self.trades_today.append(trade)
        self.last_trade_time = datetime.now()
        
        self.logger.info(f"高频交易: {direction} {qty} {self.symbol} @ {price}")
    
    def on_trade_close(self, trade):
        """交易结束时调用"""
        # 计算收益
        pnl = trade.pnl
        self.daily_pnl += pnl
        
        # 记录交易结果
        trade_record = {
            'timestamp': datetime.now(),
            'symbol': self.symbol,
            'exchange': self.exchange,
            'pnl': pnl,
            'holding_time': (trade.closed_at - trade.opened_at).total_seconds(),
            'entry_price': trade.entry_price,
            'exit_price': trade.exit_price,
            'qty': trade.qty
        }
        
        self.logger.info(f"交易结束: PnL={pnl:.4f}, 持仓时间={trade_record['holding_time']:.0f}秒")
        
        # 检查日收益目标
        self._check_daily_targets()
    
    def _check_daily_targets(self):
        """检查日收益目标"""
        daily_return = self.daily_pnl / self.capital
        
        if daily_return >= 0.03:  # 达到3%目标
            self.logger.info(f"🎯 达到日收益目标: {daily_return:.2%}")
        elif daily_return >= 0.30:  # 达到30%目标
            self.logger.info(f"🚀 达到高收益目标: {daily_return:.2%}")
        elif daily_return <= -0.15:  # 达到止损线
            self.logger.warning(f"⚠️ 达到日止损线: {daily_return:.2%}")
    
    def on_daily_end(self):
        """每日结束时调用"""
        # 计算日收益率
        daily_return = self.daily_pnl / self.capital
        
        # 记录日交易统计
        stats = {
            'date': datetime.now().date(),
            'total_trades': len(self.trades_today),
            'daily_pnl': self.daily_pnl,
            'daily_return': daily_return,
            'avg_holding_time': self._calculate_avg_holding_time(),
            'win_rate': self._calculate_win_rate()
        }
        
        self.logger.info(f"📊 日交易统计: {stats}")
        
        # 重置日交易记录
        self.trades_today = []
        self.daily_pnl = 0
    
    def _calculate_avg_holding_time(self) -> float:
        """计算平均持仓时间"""
        if not self.trades_today:
            return 0
        
        holding_times = []
        for trade in self.trades_today:
            if hasattr(trade, 'holding_time'):
                holding_times.append(trade['holding_time'])
        
        return np.mean(holding_times) if holding_times else 0
    
    def _calculate_win_rate(self) -> float:
        """计算胜率"""
        if not self.trades_today:
            return 0
        
        winning_trades = sum(1 for trade in self.trades_today if trade.get('pnl', 0) > 0)
        return winning_trades / len(self.trades_today) 