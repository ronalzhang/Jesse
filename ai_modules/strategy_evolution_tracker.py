"""
策略进化跟踪器
记录和分析策略的长期进化路径
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class StrategyEvolutionTracker:
    """
    策略进化跟踪器
    记录和分析策略的长期进化路径
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.evolution_data_file = "data/strategy_evolution.json"
        self.performance_history_file = "data/performance_history.json"
        self.evolution_charts_dir = "data/charts"
        
        # 确保目录存在
        os.makedirs("data", exist_ok=True)
        os.makedirs(self.evolution_charts_dir, exist_ok=True)
        
        # 初始化数据
        self.evolution_data = self._load_evolution_data()
        self.performance_history = self._load_performance_history()
    
    def _load_evolution_data(self) -> Dict:
        """加载进化数据"""
        if os.path.exists(self.evolution_data_file):
            try:
                with open(self.evolution_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载进化数据失败: {e}")
        
        return {
            'evolution_history': [],
            'strategy_versions': [],
            'parameter_changes': [],
            'performance_trends': [],
            'optimization_milestones': []
        }
    
    def _load_performance_history(self) -> Dict:
        """加载性能历史"""
        if os.path.exists(self.performance_history_file):
            try:
                with open(self.performance_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载性能历史失败: {e}")
        
        return {
            'daily_performance': [],
            'weekly_performance': [],
            'monthly_performance': [],
            'cumulative_returns': [],
            'risk_metrics': []
        }
    
    def record_daily_review(self, review_data: Dict):
        """记录每日复盘数据"""
        try:
            # 添加时间戳
            review_data['timestamp'] = datetime.now().isoformat()
            review_data['date'] = datetime.now().date().isoformat()
            
            # 记录到进化历史
            self.evolution_data['evolution_history'].append(review_data)
            
            # 记录性能数据
            self._record_performance_data(review_data)
            
            # 分析进化趋势
            self._analyze_evolution_trends()
            
            # 保存数据
            self._save_evolution_data()
            self._save_performance_history()
            
            # 生成可视化图表
            self._generate_evolution_charts()
            
            self.logger.info("✅ 每日复盘数据已记录到进化跟踪器")
            
        except Exception as e:
            self.logger.error(f"记录每日复盘数据失败: {e}")
    
    def _record_performance_data(self, review_data: Dict):
        """记录性能数据"""
        # 基础性能指标
        basic_stats = review_data.get('basic_stats', {})
        performance_data = {
            'date': review_data['date'],
            'total_trades': basic_stats.get('total_trades', 0),
            'win_rate': basic_stats.get('win_rate', 0),
            'total_pnl': basic_stats.get('total_pnl', 0),
            'daily_return': basic_stats.get('total_pnl', 0) / 10000,  # 假设初始资金10000
            'avg_holding_time': basic_stats.get('avg_holding_time', 0),
            'overall_score': review_data.get('overall_score', 0)
        }
        
        self.performance_history['daily_performance'].append(performance_data)
        
        # 计算累积收益
        self._calculate_cumulative_returns()
        
        # 计算风险指标
        self._calculate_risk_metrics()
    
    def _calculate_cumulative_returns(self):
        """计算累积收益"""
        daily_performance = self.performance_history['daily_performance']
        if not daily_performance:
            return
        
        cumulative_return = 0
        cumulative_returns = []
        
        for performance in daily_performance:
            cumulative_return += performance['daily_return']
            cumulative_returns.append({
                'date': performance['date'],
                'cumulative_return': cumulative_return,
                'daily_return': performance['daily_return']
            })
        
        self.performance_history['cumulative_returns'] = cumulative_returns
    
    def _calculate_risk_metrics(self):
        """计算风险指标"""
        daily_performance = self.performance_history['daily_performance']
        if len(daily_performance) < 2:
            return
        
        returns = [p['daily_return'] for p in daily_performance]
        
        risk_metrics = {
            'volatility': np.std(returns),
            'sharpe_ratio': np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0,
            'max_drawdown': self._calculate_max_drawdown(returns),
            'win_rate_avg': np.mean([p['win_rate'] for p in daily_performance]),
            'avg_holding_time': np.mean([p['avg_holding_time'] for p in daily_performance])
        }
        
        self.performance_history['risk_metrics'].append({
            'date': datetime.now().date().isoformat(),
            'metrics': risk_metrics
        })
    
    def _calculate_max_drawdown(self, returns: List[float]) -> float:
        """计算最大回撤"""
        cumulative = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return abs(np.min(drawdown)) if len(drawdown) > 0 else 0
    
    def _analyze_evolution_trends(self):
        """分析进化趋势"""
        if len(self.evolution_data['evolution_history']) < 7:
            return
        
        # 获取最近30天的数据
        recent_data = self.evolution_data['evolution_history'][-30:]
        
        # 分析趋势
        trends = {
            'score_trend': self._calculate_trend([d.get('overall_score', 0) for d in recent_data]),
            'return_trend': self._calculate_trend([d.get('basic_stats', {}).get('total_pnl', 0) for d in recent_data]),
            'win_rate_trend': self._calculate_trend([d.get('basic_stats', {}).get('win_rate', 0) for d in recent_data]),
            'holding_time_trend': self._calculate_trend([d.get('basic_stats', {}).get('avg_holding_time', 0) for d in recent_data])
        }
        
        # 记录趋势分析
        self.evolution_data['performance_trends'].append({
            'date': datetime.now().date().isoformat(),
            'trends': trends,
            'analysis_period': '30_days'
        })
    
    def _calculate_trend(self, data: List[float]) -> str:
        """计算趋势"""
        if len(data) < 2:
            return 'stable'
        
        slope = np.polyfit(range(len(data)), data, 1)[0]
        
        if slope > 0.01:
            return 'increasing'
        elif slope < -0.01:
            return 'decreasing'
        else:
            return 'stable'
    
    def _save_evolution_data(self):
        """保存进化数据"""
        try:
            with open(self.evolution_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.evolution_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"保存进化数据失败: {e}")
    
    def _save_performance_history(self):
        """保存性能历史"""
        try:
            with open(self.performance_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.performance_history, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"保存性能历史失败: {e}")
    
    def _generate_evolution_charts(self):
        """生成进化图表"""
        try:
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 生成累积收益图
            self._generate_cumulative_returns_chart()
            
            # 生成性能趋势图
            self._generate_performance_trends_chart()
            
            # 生成策略评分图
            self._generate_strategy_score_chart()
            
            # 生成风险指标图
            self._generate_risk_metrics_chart()
            
            self.logger.info("✅ 进化图表已生成")
            
        except Exception as e:
            self.logger.error(f"生成进化图表失败: {e}")
    
    def _generate_cumulative_returns_chart(self):
        """生成累积收益图"""
        cumulative_returns = self.performance_history.get('cumulative_returns', [])
        if not cumulative_returns:
            return
        
        dates = [r['date'] for r in cumulative_returns]
        returns = [r['cumulative_return'] for r in cumulative_returns]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, returns, marker='o', linewidth=2, markersize=4)
        plt.title('策略累积收益进化路径', fontsize=16, fontweight='bold')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('累积收益率 (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.evolution_charts_dir, 'cumulative_returns.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_performance_trends_chart(self):
        """生成性能趋势图"""
        daily_performance = self.performance_history.get('daily_performance', [])
        if len(daily_performance) < 7:
            return
        
        # 获取最近30天数据
        recent_data = daily_performance[-30:]
        dates = [p['date'] for p in recent_data]
        returns = [p['daily_return'] * 100 for p in recent_data]  # 转换为百分比
        win_rates = [p['win_rate'] * 100 for p in recent_data]  # 转换为百分比
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 日收益率图
        ax1.plot(dates, returns, marker='o', linewidth=2, color='#2E86AB')
        ax1.set_title('日收益率趋势', fontsize=14, fontweight='bold')
        ax1.set_ylabel('日收益率 (%)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=3, color='green', linestyle='--', alpha=0.7, label='目标下限(3%)')
        ax1.axhline(y=30, color='red', linestyle='--', alpha=0.7, label='目标上限(30%)')
        ax1.legend()
        
        # 胜率图
        ax2.plot(dates, win_rates, marker='s', linewidth=2, color='#A23B72')
        ax2.set_title('胜率趋势', fontsize=14, fontweight='bold')
        ax2.set_xlabel('日期', fontsize=12)
        ax2.set_ylabel('胜率 (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='目标胜率(60%)')
        ax2.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.evolution_charts_dir, 'performance_trends.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_strategy_score_chart(self):
        """生成策略评分图"""
        evolution_history = self.evolution_data.get('evolution_history', [])
        if not evolution_history:
            return
        
        dates = [h['date'] for h in evolution_history]
        scores = [h.get('overall_score', 0) for h in evolution_history]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, scores, marker='o', linewidth=2, color='#F18F01')
        plt.title('策略综合评分进化', fontsize=16, fontweight='bold')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('综合评分', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=80, color='green', linestyle='--', alpha=0.7, label='优秀(80)')
        plt.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='良好(60)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.evolution_charts_dir, 'strategy_score.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_risk_metrics_chart(self):
        """生成风险指标图"""
        risk_metrics = self.performance_history.get('risk_metrics', [])
        if not risk_metrics:
            return
        
        dates = [m['date'] for m in risk_metrics]
        sharpe_ratios = [m['metrics']['sharpe_ratio'] for m in risk_metrics]
        volatilities = [m['metrics']['volatility'] * 100 for m in risk_metrics]  # 转换为百分比
        max_drawdowns = [m['metrics']['max_drawdown'] * 100 for m in risk_metrics]  # 转换为百分比
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
        
        # 夏普比率
        ax1.plot(dates, sharpe_ratios, marker='o', linewidth=2, color='#C73E1D')
        ax1.set_title('夏普比率趋势', fontsize=14, fontweight='bold')
        ax1.set_ylabel('夏普比率', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=1.5, color='green', linestyle='--', alpha=0.7, label='目标(1.5)')
        ax1.legend()
        
        # 波动率
        ax2.plot(dates, volatilities, marker='s', linewidth=2, color='#3E92CC')
        ax2.set_title('波动率趋势', fontsize=14, fontweight='bold')
        ax2.set_ylabel('波动率 (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # 最大回撤
        ax3.plot(dates, max_drawdowns, marker='^', linewidth=2, color='#FF6B6B')
        ax3.set_title('最大回撤趋势', fontsize=14, fontweight='bold')
        ax3.set_xlabel('日期', fontsize=12)
        ax3.set_ylabel('最大回撤 (%)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='警戒线(10%)')
        ax3.legend()
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图表
        chart_path = os.path.join(self.evolution_charts_dir, 'risk_metrics.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def get_evolution_summary(self) -> Dict:
        """获取进化总结"""
        if not self.evolution_data['evolution_history']:
            return {}
        
        # 计算总体统计
        total_days = len(self.evolution_data['evolution_history'])
        recent_data = self.evolution_data['evolution_history'][-30:]  # 最近30天
        
        # 性能统计
        daily_performance = self.performance_history.get('daily_performance', [])
        if daily_performance:
            total_return = sum([p['daily_return'] for p in daily_performance])
            avg_daily_return = np.mean([p['daily_return'] for p in daily_performance])
            best_day = max([p['daily_return'] for p in daily_performance])
            worst_day = min([p['daily_return'] for p in daily_performance])
        else:
            total_return = avg_daily_return = best_day = worst_day = 0
        
        # 评分统计
        scores = [h.get('overall_score', 0) for h in self.evolution_data['evolution_history']]
        avg_score = np.mean(scores) if scores else 0
        best_score = max(scores) if scores else 0
        
        # 趋势分析
        trends = self.evolution_data.get('performance_trends', [])
        current_trends = trends[-1] if trends else {}
        
        return {
            'summary': {
                'total_days': total_days,
                'total_return': total_return,
                'avg_daily_return': avg_daily_return,
                'best_day_return': best_day,
                'worst_day_return': worst_day,
                'avg_score': avg_score,
                'best_score': best_score
            },
            'current_trends': current_trends.get('trends', {}),
            'evolution_milestones': self._get_evolution_milestones(),
            'optimization_suggestions': self._get_optimization_suggestions()
        }
    
    def _get_evolution_milestones(self) -> List[Dict]:
        """获取进化里程碑"""
        milestones = []
        evolution_history = self.evolution_data['evolution_history']
        
        for i, record in enumerate(evolution_history):
            score = record.get('overall_score', 0)
            daily_return = record.get('basic_stats', {}).get('total_pnl', 0) / 10000
            
            # 重要里程碑
            if score >= 80:
                milestones.append({
                    'date': record['date'],
                    'type': 'excellent_score',
                    'description': f'策略评分达到优秀水平: {score}',
                    'value': score
                })
            
            if daily_return >= 0.30:
                milestones.append({
                    'date': record['date'],
                    'type': 'high_return',
                    'description': f'日收益率达到高目标: {daily_return:.2%}',
                    'value': daily_return
                })
            
            if daily_return <= -0.15:
                milestones.append({
                    'date': record['date'],
                    'type': 'risk_alert',
                    'description': f'触发风险警报: {daily_return:.2%}',
                    'value': daily_return
                })
        
        return milestones[-10:]  # 返回最近10个里程碑
    
    def _get_optimization_suggestions(self) -> List[str]:
        """获取优化建议"""
        suggestions = []
        
        # 基于当前趋势生成建议
        trends = self.evolution_data.get('performance_trends', [])
        if trends:
            current_trends = trends[-1].get('trends', {})
            
            if current_trends.get('score_trend') == 'decreasing':
                suggestions.append("📉 策略评分呈下降趋势，建议优化交易逻辑")
            
            if current_trends.get('return_trend') == 'decreasing':
                suggestions.append("📉 收益呈下降趋势，建议调整风险参数")
            
            if current_trends.get('win_rate_trend') == 'decreasing':
                suggestions.append("📉 胜率呈下降趋势，建议改进入场信号")
        
        # 基于风险指标生成建议
        risk_metrics = self.performance_history.get('risk_metrics', [])
        if risk_metrics:
            latest_metrics = risk_metrics[-1]['metrics']
            
            if latest_metrics['sharpe_ratio'] < 1.0:
                suggestions.append("📊 夏普比率偏低，建议优化风险收益比")
            
            if latest_metrics['max_drawdown'] > 0.1:
                suggestions.append("⚠️ 最大回撤过大，建议降低仓位大小")
        
        return suggestions
    
    def export_evolution_report(self, output_path: str = "data/evolution_report.html"):
        """导出进化报告"""
        try:
            summary = self.get_evolution_summary()
            
            # 生成HTML报告
            html_content = self._generate_html_report(summary)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"✅ 进化报告已导出: {output_path}")
            
        except Exception as e:
            self.logger.error(f"导出进化报告失败: {e}")
    
    def _generate_html_report(self, summary: Dict) -> str:
        """生成HTML报告"""
        html_template = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>策略进化报告</title>
            <style>
                body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
                .summary-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }
                .summary-card h3 { margin: 0 0 10px 0; font-size: 18px; }
                .summary-card .value { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
                .trends-section { margin: 30px 0; }
                .trend-item { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #3498db; }
                .milestones-section { margin: 30px 0; }
                .milestone { background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ffc107; }
                .suggestions-section { margin: 30px 0; }
                .suggestion { background: #d1ecf1; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #17a2b8; }
                .charts-section { margin: 30px 0; }
                .chart-container { text-align: center; margin: 20px 0; }
                .chart-container img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 策略进化报告</h1>
                
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>总运行天数</h3>
                        <div class="value">{total_days}</div>
                    </div>
                    <div class="summary-card">
                        <h3>总收益率</h3>
                        <div class="value">{total_return:.2%}</div>
                    </div>
                    <div class="summary-card">
                        <h3>平均日收益率</h3>
                        <div class="value">{avg_daily_return:.2%}</div>
                    </div>
                    <div class="summary-card">
                        <h3>平均策略评分</h3>
                        <div class="value">{avg_score:.1f}</div>
                    </div>
                </div>
                
                <div class="trends-section">
                    <h2>📈 当前趋势分析</h2>
                    {trends_html}
                </div>
                
                <div class="milestones-section">
                    <h2>🏆 进化里程碑</h2>
                    {milestones_html}
                </div>
                
                <div class="suggestions-section">
                    <h2>💡 优化建议</h2>
                    {suggestions_html}
                </div>
                
                <div class="charts-section">
                    <h2>📊 进化图表</h2>
                    <div class="chart-container">
                        <h3>累积收益进化路径</h3>
                        <img src="charts/cumulative_returns.png" alt="累积收益">
                    </div>
                    <div class="chart-container">
                        <h3>性能趋势分析</h3>
                        <img src="charts/performance_trends.png" alt="性能趋势">
                    </div>
                    <div class="chart-container">
                        <h3>策略评分进化</h3>
                        <img src="charts/strategy_score.png" alt="策略评分">
                    </div>
                    <div class="chart-container">
                        <h3>风险指标监控</h3>
                        <img src="charts/risk_metrics.png" alt="风险指标">
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # 填充数据
        summary_data = summary.get('summary', {})
        trends = summary.get('current_trends', {})
        milestones = summary.get('evolution_milestones', [])
        suggestions = summary.get('optimization_suggestions', [])
        
        # 生成趋势HTML
        trends_html = ""
        for trend_name, trend_value in trends.items():
            trend_icon = "📈" if trend_value == "increasing" else "📉" if trend_value == "decreasing" else "➡️"
            trends_html += f'<div class="trend-item"><strong>{trend_icon} {trend_name}:</strong> {trend_value}</div>'
        
        # 生成里程碑HTML
        milestones_html = ""
        for milestone in milestones:
            milestone_icon = "🏆" if milestone['type'] == 'excellent_score' else "💰" if milestone['type'] == 'high_return' else "⚠️"
            milestones_html += f'<div class="milestone"><strong>{milestone_icon} {milestone["date"]}:</strong> {milestone["description"]}</div>'
        
        # 生成建议HTML
        suggestions_html = ""
        for suggestion in suggestions:
            suggestions_html += f'<div class="suggestion">{suggestion}</div>'
        
        return html_template.format(
            total_days=summary_data.get('total_days', 0),
            total_return=summary_data.get('total_return', 0),
            avg_daily_return=summary_data.get('avg_daily_return', 0),
            avg_score=summary_data.get('avg_score', 0),
            trends_html=trends_html,
            milestones_html=milestones_html,
            suggestions_html=suggestions_html
        ) 