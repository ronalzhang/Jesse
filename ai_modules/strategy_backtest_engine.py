"""
策略回测引擎
用于真实评估策略性能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
import json
import os
from dataclasses import dataclass

@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_duration: float
    volatility: float
    calmar_ratio: float
    sortino_ratio: float

class StrategyBacktestEngine:
    """策略回测引擎"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = "data/backtest"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def backtest_strategy(self, strategy: Dict[str, Any], 
                         market_data: pd.DataFrame,
                         initial_capital: float = 10000.0) -> BacktestResult:
        """
        回测策略
        
        Args:
            strategy: 策略配置
            market_data: 市场数据 (包含 open, high, low, close, volume)
            initial_capital: 初始资金
            
        Returns:
            回测结果
        """
        try:
            self.logger.info(f"📊 开始回测策略: {strategy['name']}")
            
            # 复制市场数据
            data = market_data.copy()
            
            # 添加技术指标
            data = self._add_technical_indicators(data, strategy)
            
            # 生成交易信号
            signals = self._generate_signals(data, strategy)
            
            # 执行回测
            backtest_result = self._execute_backtest(data, signals, initial_capital)
            
            self.logger.info(f"✅ 策略回测完成: {strategy['name']}")
            return backtest_result
            
        except Exception as e:
            self.logger.error(f"❌ 策略回测失败: {e}")
            return self._create_default_result()
    
    def _add_technical_indicators(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.DataFrame:
        """添加技术指标"""
        try:
            # RSI
            if 'rsi_period' in strategy['parameters']:
                data['rsi'] = self._calculate_rsi(data['close'], strategy['parameters']['rsi_period'])
            
            # 移动平均线
            if 'ma_short' in strategy['parameters'] and 'ma_long' in strategy['parameters']:
                data['ma_short'] = data['close'].rolling(window=int(strategy['parameters']['ma_short'])).mean()
                data['ma_long'] = data['close'].rolling(window=int(strategy['parameters']['ma_long'])).mean()
            
            # 布林带
            if 'bollinger_period' in strategy['parameters'] and 'bollinger_std' in strategy['parameters']:
                period = int(strategy['parameters']['bollinger_period'])
                std = strategy['parameters']['bollinger_std']
                data['bb_middle'] = data['close'].rolling(window=period).mean()
                data['bb_upper'] = data['bb_middle'] + (data['close'].rolling(window=period).std() * std)
                data['bb_lower'] = data['bb_middle'] - (data['close'].rolling(window=period).std() * std)
            
            # MACD
            data['ema_12'] = data['close'].ewm(span=12).mean()
            data['ema_26'] = data['close'].ewm(span=26).mean()
            data['macd'] = data['ema_12'] - data['ema_26']
            data['macd_signal'] = data['macd'].ewm(span=9).mean()
            data['macd_histogram'] = data['macd'] - data['macd_signal']
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ 添加技术指标失败: {e}")
            return data
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _generate_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成交易信号"""
        signals = pd.Series(index=data.index, data=0)  # 0: hold, 1: buy, -1: sell
        
        try:
            strategy_type = strategy['type']
            
            if strategy_type == 'trend_following':
                signals = self._generate_trend_following_signals(data, strategy)
            elif strategy_type == 'mean_reversion':
                signals = self._generate_mean_reversion_signals(data, strategy)
            elif strategy_type == 'arbitrage':
                signals = self._generate_arbitrage_signals(data, strategy)
            elif strategy_type == 'grid_trading':
                signals = self._generate_grid_trading_signals(data, strategy)
            else:
                signals = self._generate_hybrid_signals(data, strategy)
            
            return signals
            
        except Exception as e:
            self.logger.error(f"❌ 生成交易信号失败: {e}")
            return signals
    
    def _generate_trend_following_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成趋势跟踪信号"""
        signals = pd.Series(index=data.index, data=0)
        
        # 移动平均线交叉
        if 'ma_short' in data.columns and 'ma_long' in data.columns:
            signals.loc[data['ma_short'] > data['ma_long']] = 1  # 买入信号
            signals.loc[data['ma_short'] < data['ma_long']] = -1  # 卖出信号
        
        # MACD信号
        if 'macd' in data.columns and 'macd_signal' in data.columns:
            signals.loc[data['macd'] > data['macd_signal']] = 1
            signals.loc[data['macd'] < data['macd_signal']] = -1
        
        return signals
    
    def _generate_mean_reversion_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成均值回归信号"""
        signals = pd.Series(index=data.index, data=0)
        
        # RSI信号
        if 'rsi' in data.columns:
            rsi_oversold = 30
            rsi_overbought = 70
            signals.loc[data['rsi'] < rsi_oversold] = 1  # 超卖买入
            signals.loc[data['rsi'] > rsi_overbought] = -1  # 超买卖出
        
        # 布林带信号
        if 'bb_upper' in data.columns and 'bb_lower' in data.columns:
            signals.loc[data['close'] < data['bb_lower']] = 1  # 下轨买入
            signals.loc[data['close'] > data['bb_upper']] = -1  # 上轨卖出
        
        return signals
    
    def _generate_arbitrage_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成套利信号"""
        signals = pd.Series(index=data.index, data=0)
        
        # 简单的价格差异套利
        if len(data) > 1:
            price_change = data['close'].pct_change()
            threshold = 0.02  # 2%阈值
            
            signals.loc[price_change > threshold] = -1  # 价格上涨卖出
            signals.loc[price_change < -threshold] = 1  # 价格下跌买入
        
        return signals
    
    def _generate_grid_trading_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成网格交易信号"""
        signals = pd.Series(index=data.index, data=0)
        
        # 简单的网格策略
        grid_levels = 10
        price_range = data['close'].max() - data['close'].min()
        grid_size = price_range / grid_levels
        
        for i in range(grid_levels):
            grid_price = data['close'].min() + i * grid_size
            signals.loc[data['close'] <= grid_price] = 1
            signals.loc[data['close'] >= grid_price + grid_size] = -1
        
        return signals
    
    def _generate_hybrid_signals(self, data: pd.DataFrame, strategy: Dict[str, Any]) -> pd.Series:
        """生成混合信号"""
        signals = pd.Series(index=data.index, data=0)
        
        # 结合多种信号
        trend_signals = self._generate_trend_following_signals(data, strategy)
        reversion_signals = self._generate_mean_reversion_signals(data, strategy)
        
        # 信号融合
        signals = (trend_signals + reversion_signals) / 2
        signals = signals.round().astype(int)
        
        return signals
    
    def _execute_backtest(self, data: pd.DataFrame, signals: pd.Series, 
                         initial_capital: float) -> BacktestResult:
        """执行回测"""
        try:
            # 初始化变量
            capital = initial_capital
            position = 0
            trades = []
            equity_curve = []
            
            for i in range(1, len(data)):
                current_price = data['close'].iloc[i]
                current_signal = signals.iloc[i]
                
                # 执行交易
                if current_signal == 1 and position == 0:  # 买入
                    position = capital / current_price
                    capital = 0
                    trades.append({
                        'type': 'buy',
                        'price': current_price,
                        'timestamp': data.index[i],
                        'position': position
                    })
                elif current_signal == -1 and position > 0:  # 卖出
                    capital = position * current_price
                    trades.append({
                        'type': 'sell',
                        'price': current_price,
                        'timestamp': data.index[i],
                        'position': position
                    })
                    position = 0
                
                # 计算当前权益
                current_equity = capital + (position * current_price)
                equity_curve.append(current_equity)
            
            # 计算回测指标
            return self._calculate_backtest_metrics(equity_curve, trades, initial_capital)
            
        except Exception as e:
            self.logger.error(f"❌ 执行回测失败: {e}")
            return self._create_default_result()
    
    def _calculate_backtest_metrics(self, equity_curve: List[float], 
                                  trades: List[Dict], initial_capital: float) -> BacktestResult:
        """计算回测指标"""
        try:
            equity_series = pd.Series(equity_curve)
            
            # 总收益率
            total_return = (equity_series.iloc[-1] - initial_capital) / initial_capital
            
            # 收益率序列
            returns = equity_series.pct_change().dropna()
            
            # 夏普比率
            sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std() if returns.std() > 0 else 0
            
            # 最大回撤
            max_drawdown = self._calculate_max_drawdown(equity_series)
            
            # 胜率
            if trades:
                winning_trades = [t for t in trades if t['type'] == 'sell' and 
                                t['price'] > trades[trades.index(t)-1]['price']]
                win_rate = len(winning_trades) / len([t for t in trades if t['type'] == 'sell'])
            else:
                win_rate = 0.0
            
            # 盈亏比
            profit_factor = self._calculate_profit_factor(trades)
            
            # 总交易次数
            total_trades = len([t for t in trades if t['type'] == 'sell'])
            
            # 平均持仓时间
            avg_trade_duration = self._calculate_avg_trade_duration(trades)
            
            # 波动率
            volatility = returns.std() * np.sqrt(252)
            
            # Calmar比率
            calmar_ratio = total_return / max_drawdown if max_drawdown > 0 else 0
            
            # Sortino比率
            negative_returns = returns[returns < 0]
            downside_deviation = negative_returns.std() if len(negative_returns) > 0 else 0
            sortino_ratio = np.sqrt(252) * returns.mean() / downside_deviation if downside_deviation > 0 else 0
            
            return BacktestResult(
                total_return=total_return,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=max_drawdown,
                win_rate=win_rate,
                profit_factor=profit_factor,
                total_trades=total_trades,
                avg_trade_duration=avg_trade_duration,
                volatility=volatility,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio
            )
            
        except Exception as e:
            self.logger.error(f"❌ 计算回测指标失败: {e}")
            return self._create_default_result()
    
    def _calculate_max_drawdown(self, equity_series: pd.Series) -> float:
        """计算最大回撤"""
        try:
            peak = equity_series.expanding().max()
            drawdown = (equity_series - peak) / peak
            return abs(drawdown.min())
        except:
            return 0.0
    
    def _calculate_profit_factor(self, trades: List[Dict]) -> float:
        """计算盈亏比"""
        try:
            if not trades:
                return 0.0
            
            profits = []
            losses = []
            
            for i in range(1, len(trades), 2):
                if i < len(trades):
                    buy_price = trades[i-1]['price']
                    sell_price = trades[i]['price']
                    profit = sell_price - buy_price
                    
                    if profit > 0:
                        profits.append(profit)
                    else:
                        losses.append(abs(profit))
            
            total_profit = sum(profits) if profits else 0
            total_loss = sum(losses) if losses else 1
            
            return total_profit / total_loss if total_loss > 0 else 0
            
        except Exception as e:
            self.logger.error(f"❌ 计算盈亏比失败: {e}")
            return 0.0
    
    def _calculate_avg_trade_duration(self, trades: List[Dict]) -> float:
        """计算平均持仓时间"""
        try:
            if len(trades) < 2:
                return 0.0
            
            durations = []
            for i in range(1, len(trades), 2):
                if i < len(trades):
                    buy_time = trades[i-1]['timestamp']
                    sell_time = trades[i]['timestamp']
                    duration = (sell_time - buy_time).total_seconds() / 3600  # 小时
                    durations.append(duration)
            
            return np.mean(durations) if durations else 0.0
            
        except Exception as e:
            self.logger.error(f"❌ 计算平均持仓时间失败: {e}")
            return 0.0
    
    def _create_default_result(self) -> BacktestResult:
        """创建默认回测结果"""
        return BacktestResult(
            total_return=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            win_rate=0.0,
            profit_factor=0.0,
            total_trades=0,
            avg_trade_duration=0.0,
            volatility=0.0,
            calmar_ratio=0.0,
            sortino_ratio=0.0
        )
    
    def save_backtest_result(self, strategy_name: str, result: BacktestResult):
        """保存回测结果"""
        try:
            result_file = os.path.join(self.data_dir, f"{strategy_name}_backtest_result.json")
            result_dict = {
                'strategy_name': strategy_name,
                'timestamp': datetime.now().isoformat(),
                'total_return': result.total_return,
                'sharpe_ratio': result.sharpe_ratio,
                'max_drawdown': result.max_drawdown,
                'win_rate': result.win_rate,
                'profit_factor': result.profit_factor,
                'total_trades': result.total_trades,
                'avg_trade_duration': result.avg_trade_duration,
                'volatility': result.volatility,
                'calmar_ratio': result.calmar_ratio,
                'sortino_ratio': result.sortino_ratio
            }
            
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ 回测结果已保存: {result_file}")
            
        except Exception as e:
            self.logger.error(f"❌ 保存回测结果失败: {e}")
    
    def load_backtest_result(self, strategy_name: str) -> Optional[BacktestResult]:
        """加载回测结果"""
        try:
            result_file = os.path.join(self.data_dir, f"{strategy_name}_backtest_result.json")
            if os.path.exists(result_file):
                with open(result_file, 'r', encoding='utf-8') as f:
                    result_dict = json.load(f)
                
                return BacktestResult(
                    total_return=result_dict['total_return'],
                    sharpe_ratio=result_dict['sharpe_ratio'],
                    max_drawdown=result_dict['max_drawdown'],
                    win_rate=result_dict['win_rate'],
                    profit_factor=result_dict['profit_factor'],
                    total_trades=result_dict['total_trades'],
                    avg_trade_duration=result_dict['avg_trade_duration'],
                    volatility=result_dict['volatility'],
                    calmar_ratio=result_dict['calmar_ratio'],
                    sortino_ratio=result_dict['sortino_ratio']
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ 加载回测结果失败: {e}")
            return None 