"""
每日AI复盘系统
分析当日交易表现，优化策略参数，实现策略进化
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any
import json
import os

class DailyReviewAI:
    """
    每日AI复盘系统
    目标：分析交易表现，优化策略，实现日化3%-30%收益
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.review_data = {}
        self.strategy_evolution_history = []
        
        # 导入进化跟踪器
        try:
            from .strategy_evolution_tracker import StrategyEvolutionTracker
            self.evolution_tracker = StrategyEvolutionTracker()
        except ImportError:
            self.evolution_tracker = None
            self.logger.warning("策略进化跟踪器未找到，将跳过长期记录功能")
        
    def analyze_daily_performance(self, trades_data: List[Dict], market_data: Dict) -> Dict:
        """
        分析每日交易表现
        
        Args:
            trades_data: 当日交易数据
            market_data: 市场数据
            
        Returns:
            分析结果
        """
        self.logger.info("🤖 开始AI每日复盘分析...")
        
        # 基础统计
        basic_stats = self._calculate_basic_stats(trades_data)
        
        # 收益分析
        profit_analysis = self._analyze_profit_patterns(trades_data)
        
        # 风险分析
        risk_analysis = self._analyze_risk_metrics(trades_data)
        
        # 策略效果分析
        strategy_analysis = self._analyze_strategy_effectiveness(trades_data)
        
        # 市场环境分析
        market_analysis = self._analyze_market_conditions(market_data)
        
        # 综合评分
        overall_score = self._calculate_overall_score(
            basic_stats, profit_analysis, risk_analysis, strategy_analysis, market_analysis
        )
        
        # 策略优化建议
        optimization_suggestions = self._generate_optimization_suggestions(
            basic_stats, profit_analysis, risk_analysis, strategy_analysis, market_analysis
        )
        
        # 生成复盘报告
        review_report = {
            'date': datetime.now().date().isoformat(),
            'basic_stats': basic_stats,
            'profit_analysis': profit_analysis,
            'risk_analysis': risk_analysis,
            'strategy_analysis': strategy_analysis,
            'market_analysis': market_analysis,
            'overall_score': overall_score,
            'optimization_suggestions': optimization_suggestions,
            'target_achievement': self._evaluate_target_achievement(basic_stats),
            'strategy_evolution': self._plan_strategy_evolution(overall_score)
        }
        
        # 保存复盘数据
        self._save_review_data(review_report)
        
        # 记录到进化跟踪器
        if self.evolution_tracker:
            self.evolution_tracker.record_daily_review(review_report)
        
        # 输出分析结果
        self._output_analysis_summary(review_report)
        
        return review_report
    
    def _calculate_basic_stats(self, trades_data: List[Dict]) -> Dict:
        """计算基础统计"""
        if not trades_data:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_pnl_per_trade': 0,
                'max_profit': 0,
                'max_loss': 0,
                'avg_holding_time': 0,
                'total_volume': 0
            }
        
        df = pd.DataFrame(trades_data)
        
        # 基础统计
        total_trades = len(df)
        winning_trades = len(df[df['pnl'] > 0])
        losing_trades = len(df[df['pnl'] < 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        total_pnl = df['pnl'].sum()
        avg_pnl_per_trade = df['pnl'].mean()
        max_profit = df['pnl'].max()
        max_loss = df['pnl'].min()
        
        # 持仓时间分析
        if 'holding_time' in df.columns:
            avg_holding_time = df['holding_time'].mean()
        else:
            avg_holding_time = 0
        
        # 交易量分析
        if 'qty' in df.columns and 'exit_price' in df.columns:
            total_volume = (df['qty'] * df['exit_price']).sum()
        else:
            total_volume = 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_pnl_per_trade': avg_pnl_per_trade,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'avg_holding_time': avg_holding_time,
            'total_volume': total_volume
        }
    
    def _analyze_profit_patterns(self, trades_data: List[Dict]) -> Dict:
        """分析收益模式"""
        if not trades_data:
            return {'profit_trend': 'no_data', 'profit_consistency': 0}
        
        df = pd.DataFrame(trades_data)
        
        # 收益趋势分析
        df['cumulative_pnl'] = df['pnl'].cumsum()
        profit_trend = self._calculate_trend(df['cumulative_pnl'])
        
        # 收益一致性分析
        profit_consistency = self._calculate_consistency(df['pnl'])
        
        # 最佳交易时间分析
        if 'timestamp' in df.columns:
            df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            hourly_profit = df.groupby('hour')['pnl'].sum()
            best_hour = hourly_profit.idxmax()
            worst_hour = hourly_profit.idxmin()
        else:
            best_hour = None
            worst_hour = None
        
        return {
            'profit_trend': profit_trend,
            'profit_consistency': profit_consistency,
            'best_trading_hour': best_hour,
            'worst_trading_hour': worst_hour,
            'profit_factor': self._calculate_profit_factor(df)
        }
    
    def _analyze_risk_metrics(self, trades_data: List[Dict]) -> Dict:
        """分析风险指标"""
        if not trades_data:
            return {'risk_score': 0, 'max_drawdown': 0}
        
        df = pd.DataFrame(trades_data)
        
        # 计算风险指标
        pnl_std = df['pnl'].std()
        max_drawdown = self._calculate_max_drawdown(df['pnl'])
        sharpe_ratio = self._calculate_sharpe_ratio(df['pnl'])
        risk_score = self._calculate_risk_score(df['pnl'])
        
        return {
            'risk_score': risk_score,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'pnl_volatility': pnl_std,
            'risk_adjusted_return': sharpe_ratio
        }
    
    def _analyze_strategy_effectiveness(self, trades_data: List[Dict]) -> Dict:
        """分析策略有效性"""
        if not trades_data:
            return {'strategy_score': 0, 'efficiency': 0}
        
        df = pd.DataFrame(trades_data)
        
        # 策略效率分析
        if 'holding_time' in df.columns:
            efficiency = self._calculate_strategy_efficiency(df)
        else:
            efficiency = 0
        
        # 信号质量分析
        signal_quality = self._analyze_signal_quality(df)
        
        # 策略适应性分析
        adaptability = self._analyze_strategy_adaptability(df)
        
        return {
            'strategy_score': (efficiency + signal_quality + adaptability) / 3,
            'efficiency': efficiency,
            'signal_quality': signal_quality,
            'adaptability': adaptability
        }
    
    def _analyze_market_conditions(self, market_data: Dict) -> Dict:
        """分析市场环境"""
        # 这里可以添加更复杂的市场分析逻辑
        return {
            'market_volatility': market_data.get('volatility', 0),
            'market_trend': market_data.get('trend', 'neutral'),
            'market_conditions': 'favorable' if market_data.get('volatility', 0) > 0.02 else 'stable'
        }
    
    def _calculate_overall_score(self, basic_stats: Dict, profit_analysis: Dict, 
                                risk_analysis: Dict, strategy_analysis: Dict, 
                                market_analysis: Dict) -> float:
        """计算综合评分"""
        # 权重配置
        weights = {
            'profit_weight': 0.4,
            'risk_weight': 0.3,
            'strategy_weight': 0.2,
            'market_weight': 0.1
        }
        
        # 收益评分 (0-100)
        profit_score = min(100, max(0, (basic_stats['total_pnl'] / 1000) * 100))
        
        # 风险评分 (0-100, 风险越低分数越高)
        risk_score = max(0, 100 - risk_analysis['risk_score'])
        
        # 策略评分 (0-100)
        strategy_score = strategy_analysis['strategy_score'] * 100
        
        # 市场评分 (0-100)
        market_score = 80 if market_analysis['market_conditions'] == 'favorable' else 60
        
        # 加权计算
        overall_score = (
            profit_score * weights['profit_weight'] +
            risk_score * weights['risk_weight'] +
            strategy_score * weights['strategy_weight'] +
            market_score * weights['market_weight']
        )
        
        return round(overall_score, 2)
    
    def _generate_optimization_suggestions(self, basic_stats: Dict, profit_analysis: Dict,
                                         risk_analysis: Dict, strategy_analysis: Dict,
                                         market_analysis: Dict) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        # 基于收益分析的建议
        if basic_stats['win_rate'] < 0.5:
            suggestions.append("🔧 胜率偏低，建议优化入场信号，提高信号质量")
        
        if basic_stats['avg_holding_time'] > 1800:  # 超过30分钟
            suggestions.append("⚡ 持仓时间过长，建议缩短持仓时间以提高资金周转率")
        
        if profit_analysis['profit_consistency'] < 0.6:
            suggestions.append("📈 收益一致性较差，建议优化风险控制参数")
        
        # 基于风险分析的建议
        if risk_analysis['max_drawdown'] > 0.1:
            suggestions.append("⚠️ 最大回撤过大，建议降低单次仓位大小")
        
        if risk_analysis['sharpe_ratio'] < 1.0:
            suggestions.append("📊 夏普比率偏低，建议优化风险收益比")
        
        # 基于策略分析的建议
        if strategy_analysis['efficiency'] < 0.6:
            suggestions.append("🎯 策略效率偏低，建议优化交易逻辑")
        
        if strategy_analysis['signal_quality'] < 0.6:
            suggestions.append("📡 信号质量较差，建议改进技术指标组合")
        
        # 基于市场分析的建议
        if market_analysis['market_conditions'] == 'stable':
            suggestions.append("🌊 市场波动较小，建议增加套利策略")
        
        return suggestions
    
    def _evaluate_target_achievement(self, basic_stats: Dict) -> Dict:
        """评估目标达成情况"""
        daily_return = basic_stats['total_pnl'] / 10000  # 假设初始资金10000
        
        target_achievement = {
            'daily_target_min': 0.03,  # 3%
            'daily_target_max': 0.30,  # 30%
            'current_return': daily_return,
            'achievement_level': 'low'
        }
        
        if daily_return >= 0.30:
            target_achievement['achievement_level'] = 'excellent'
        elif daily_return >= 0.15:
            target_achievement['achievement_level'] = 'good'
        elif daily_return >= 0.03:
            target_achievement['achievement_level'] = 'acceptable'
        else:
            target_achievement['achievement_level'] = 'poor'
        
        return target_achievement
    
    def _plan_strategy_evolution(self, overall_score: float) -> Dict:
        """规划策略进化"""
        evolution_plan = {
            'evolution_level': 'minor',
            'parameter_adjustments': [],
            'strategy_enhancements': []
        }
        
        if overall_score >= 80:
            evolution_plan['evolution_level'] = 'optimize'
            evolution_plan['parameter_adjustments'] = [
                "微调止盈止损参数",
                "优化仓位管理",
                "增强信号过滤"
            ]
        elif overall_score >= 60:
            evolution_plan['evolution_level'] = 'enhance'
            evolution_plan['strategy_enhancements'] = [
                "增加新的技术指标",
                "优化入场时机",
                "改进风险管理"
            ]
        else:
            evolution_plan['evolution_level'] = 'major'
            evolution_plan['strategy_enhancements'] = [
                "重新设计交易逻辑",
                "调整策略参数",
                "增加新的交易策略"
            ]
        
        return evolution_plan
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """计算趋势"""
        if len(series) < 2:
            return 'neutral'
        
        slope = np.polyfit(range(len(series)), series, 1)[0]
        
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'
    
    def _calculate_consistency(self, series: pd.Series) -> float:
        """计算一致性"""
        if len(series) < 2:
            return 0
        
        # 计算变异系数
        cv = series.std() / abs(series.mean()) if series.mean() != 0 else 0
        consistency = max(0, 1 - cv)
        
        return round(consistency, 3)
    
    def _calculate_profit_factor(self, df: pd.DataFrame) -> float:
        """计算盈利因子"""
        gross_profit = df[df['pnl'] > 0]['pnl'].sum()
        gross_loss = abs(df[df['pnl'] < 0]['pnl'].sum())
        
        return gross_profit / gross_loss if gross_loss > 0 else 0
    
    def _calculate_max_drawdown(self, series: pd.Series) -> float:
        """计算最大回撤"""
        cumulative = series.cumsum()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return abs(drawdown.min())
    
    def _calculate_sharpe_ratio(self, series: pd.Series) -> float:
        """计算夏普比率"""
        if len(series) < 2:
            return 0
        
        return series.mean() / series.std() if series.std() > 0 else 0
    
    def _calculate_risk_score(self, series: pd.Series) -> float:
        """计算风险评分"""
        if len(series) < 2:
            return 0
        
        # 基于波动率和最大回撤的风险评分
        volatility = series.std()
        max_drawdown = self._calculate_max_drawdown(series)
        
        risk_score = (volatility * 0.6 + max_drawdown * 0.4) * 100
        return min(100, risk_score)
    
    def _calculate_strategy_efficiency(self, df: pd.DataFrame) -> float:
        """计算策略效率"""
        if 'holding_time' not in df.columns:
            return 0
        
        # 效率 = 收益 / 持仓时间
        total_pnl = df['pnl'].sum()
        total_time = df['holding_time'].sum()
        
        if total_time == 0:
            return 0
        
        efficiency = total_pnl / total_time
        return min(1, max(0, efficiency * 1000))  # 归一化到0-1
    
    def _analyze_signal_quality(self, df: pd.DataFrame) -> float:
        """分析信号质量"""
        if len(df) == 0:
            return 0
        
        # 基于胜率和盈利因子的信号质量
        win_rate = len(df[df['pnl'] > 0]) / len(df)
        profit_factor = self._calculate_profit_factor(df)
        
        signal_quality = (win_rate * 0.6 + min(1, profit_factor) * 0.4)
        return round(signal_quality, 3)
    
    def _analyze_strategy_adaptability(self, df: pd.DataFrame) -> float:
        """分析策略适应性"""
        if len(df) < 10:
            return 0
        
        # 基于收益趋势的适应性
        df['cumulative_pnl'] = df['pnl'].cumsum()
        trend = self._calculate_trend(df['cumulative_pnl'])
        
        if trend == 'increasing':
            adaptability = 0.8
        elif trend == 'stable':
            adaptability = 0.6
        else:
            adaptability = 0.4
        
        return adaptability
    
    def _save_review_data(self, review_report: Dict):
        """保存复盘数据"""
        try:
            # 确保目录存在
            os.makedirs('data/reviews', exist_ok=True)
            
            # 保存到文件
            filename = f"data/reviews/daily_review_{datetime.now().date().isoformat()}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(review_report, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"📁 复盘数据已保存: {filename}")
        except Exception as e:
            self.logger.error(f"保存复盘数据失败: {e}")
    
    def _output_analysis_summary(self, review_report: Dict):
        """输出分析摘要"""
        self.logger.info("=" * 50)
        self.logger.info("🤖 AI每日复盘分析结果")
        self.logger.info("=" * 50)
        
        # 基础统计
        stats = review_report['basic_stats']
        self.logger.info(f"📊 基础统计:")
        self.logger.info(f"   总交易次数: {stats['total_trades']}")
        self.logger.info(f"   胜率: {stats['win_rate']:.2%}")
        self.logger.info(f"   总收益: {stats['total_pnl']:.4f}")
        self.logger.info(f"   平均持仓时间: {stats['avg_holding_time']:.0f}秒")
        
        # 目标达成
        target = review_report['target_achievement']
        self.logger.info(f"🎯 目标达成:")
        self.logger.info(f"   当前收益率: {target['current_return']:.2%}")
        self.logger.info(f"   达成等级: {target['achievement_level']}")
        
        # 综合评分
        self.logger.info(f"📈 综合评分: {review_report['overall_score']}/100")
        
        # 优化建议
        suggestions = review_report['optimization_suggestions']
        if suggestions:
            self.logger.info(f"💡 优化建议:")
            for suggestion in suggestions:
                self.logger.info(f"   {suggestion}")
        
        # 策略进化
        evolution = review_report['strategy_evolution']
        self.logger.info(f"🔄 策略进化: {evolution['evolution_level']}")
        
        self.logger.info("=" * 50) 