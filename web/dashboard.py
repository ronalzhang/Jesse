#!/usr/bin/env python3
"""
高频量化交易系统Web仪表板
美观的界面展示策略进化路径和交易数据
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import numpy as np

# 页面配置
st.set_page_config(
    page_title="高频量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .success-metric {
        border-left-color: #28a745;
    }
    
    .warning-metric {
        border-left-color: #ffc107;
    }
    
    .danger-metric {
        border-left-color: #dc3545;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class TradingDashboard:
    """交易系统仪表板"""
    
    def __init__(self):
        self.data_dir = "data"
        self.charts_dir = "data/charts"
        
    def load_evolution_data(self):
        """加载进化数据"""
        try:
            evolution_file = os.path.join(self.data_dir, "strategy_evolution.json")
            if os.path.exists(evolution_file):
                with open(evolution_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"加载进化数据失败: {e}")
        return {}
    
    def load_performance_data(self):
        """加载性能数据"""
        try:
            performance_file = os.path.join(self.data_dir, "performance_history.json")
            if os.path.exists(performance_file):
                with open(performance_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"加载性能数据失败: {e}")
        return {}
    
    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 高频量化交易系统</h1>
            <p>日化收益率目标: 3% - 30% | 持仓时间: 30秒 - 1小时 | AI每日复盘优化</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.title("📊 系统控制")
        
        # 系统状态
        st.sidebar.subheader("系统状态")
        status = st.sidebar.selectbox(
            "交易状态",
            ["运行中", "已停止", "维护中"],
            index=0
        )
        
        # 快速操作
        st.sidebar.subheader("快速操作")
        if st.sidebar.button("🔄 刷新数据"):
            st.rerun()
        
        if st.sidebar.button("📊 生成报告"):
            self.generate_evolution_report()
        
        if st.sidebar.button("⚙️ 系统设置"):
            st.sidebar.info("设置功能开发中...")
        
        # 实时监控
        st.sidebar.subheader("实时监控")
        st.sidebar.metric("当前收益", "2.5%", "0.3%")
        st.sidebar.metric("今日交易", "15", "3")
        st.sidebar.metric("胜率", "68%", "2%")
        
        # 风险指标
        st.sidebar.subheader("风险指标")
        st.sidebar.metric("最大回撤", "8.2%", "-0.5%")
        st.sidebar.metric("夏普比率", "1.8", "0.1")
        st.sidebar.metric("波动率", "12.5%", "-0.2%")
    
    def render_overview_metrics(self, evolution_data, performance_data):
        """渲染概览指标"""
        st.subheader("📈 系统概览")
        
        # 计算关键指标
        evolution_history = evolution_data.get('evolution_history', [])
        daily_performance = performance_data.get('daily_performance', [])
        
        if evolution_history:
            latest_review = evolution_history[-1]
            basic_stats = latest_review.get('basic_stats', {})
            overall_score = latest_review.get('overall_score', 0)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                daily_return = basic_stats.get('total_pnl', 0) / 10000
                color = "success" if daily_return >= 0.03 else "warning" if daily_return >= 0 else "danger"
                st.markdown(f"""
                <div class="metric-card {color}-metric">
                    <h3>今日收益率</h3>
                    <h2>{daily_return:.2%}</h2>
                    <p>目标: 3% - 30%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_trades = basic_stats.get('total_trades', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <h3>今日交易次数</h3>
                    <h2>{total_trades}</h2>
                    <p>高频交易</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                win_rate = basic_stats.get('win_rate', 0)
                color = "success" if win_rate >= 0.6 else "warning" if win_rate >= 0.5 else "danger"
                st.markdown(f"""
                <div class="metric-card {color}-metric">
                    <h3>胜率</h3>
                    <h2>{win_rate:.1%}</h2>
                    <p>目标: > 60%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                color = "success" if overall_score >= 80 else "warning" if overall_score >= 60 else "danger"
                st.markdown(f"""
                <div class="metric-card {color}-metric">
                    <h3>策略评分</h3>
                    <h2>{overall_score:.1f}</h2>
                    <p>满分: 100</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_evolution_charts(self, evolution_data, performance_data):
        """渲染进化图表"""
        st.subheader("📊 策略进化路径")
        
        # 累积收益图
        cumulative_returns = performance_data.get('cumulative_returns', [])
        if cumulative_returns:
            df_returns = pd.DataFrame(cumulative_returns)
            df_returns['date'] = pd.to_datetime(df_returns['date'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_returns['date'],
                y=df_returns['cumulative_return'] * 100,
                mode='lines+markers',
                name='累积收益率',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title="策略累积收益进化路径",
                xaxis_title="日期",
                yaxis_title="累积收益率 (%)",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # 性能趋势图
        daily_performance = performance_data.get('daily_performance', [])
        if len(daily_performance) >= 7:
            df_performance = pd.DataFrame(daily_performance)
            df_performance['date'] = pd.to_datetime(df_performance['date'])
            
            # 创建子图
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('日收益率趋势', '胜率趋势'),
                vertical_spacing=0.1
            )
            
            # 日收益率
            fig.add_trace(
                go.Scatter(
                    x=df_performance['date'],
                    y=df_performance['daily_return'] * 100,
                    mode='lines+markers',
                    name='日收益率',
                    line=dict(color='#2E86AB', width=2)
                ),
                row=1, col=1
            )
            
            # 添加目标线
            fig.add_hline(y=3, line_dash="dash", line_color="green", 
                         annotation_text="目标下限(3%)", row=1, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="red", 
                         annotation_text="目标上限(30%)", row=1, col=1)
            
            # 胜率
            fig.add_trace(
                go.Scatter(
                    x=df_performance['date'],
                    y=df_performance['win_rate'] * 100,
                    mode='lines+markers',
                    name='胜率',
                    line=dict(color='#A23B72', width=2)
                ),
                row=2, col=1
            )
            
            fig.add_hline(y=60, line_dash="dash", line_color="orange", 
                         annotation_text="目标胜率(60%)", row=2, col=1)
            
            fig.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_strategy_analysis(self, evolution_data):
        """渲染策略分析"""
        st.subheader("🤖 AI策略分析")
        
        evolution_history = evolution_data.get('evolution_history', [])
        if evolution_history:
            latest_review = evolution_history[-1]
            
            # 策略评分趋势
            scores = [h.get('overall_score', 0) for h in evolution_history]
            dates = [h.get('date', '') for h in evolution_history]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=scores,
                mode='lines+markers',
                name='策略评分',
                line=dict(color='#F18F01', width=3),
                marker=dict(size=6)
            ))
            
            fig.add_hline(y=80, line_dash="dash", line_color="green", 
                         annotation_text="优秀(80)")
            fig.add_hline(y=60, line_dash="dash", line_color="orange", 
                         annotation_text="良好(60)")
            
            fig.update_layout(
                title="策略综合评分进化",
                xaxis_title="日期",
                yaxis_title="综合评分",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 优化建议
            optimization_suggestions = latest_review.get('optimization_suggestions', [])
            if optimization_suggestions:
                st.subheader("💡 优化建议")
                for suggestion in optimization_suggestions:
                    st.info(suggestion)
    
    def render_risk_metrics(self, performance_data):
        """渲染风险指标"""
        st.subheader("🛡️ 风险控制")
        
        risk_metrics = performance_data.get('risk_metrics', [])
        if risk_metrics:
            df_risk = pd.DataFrame([m['metrics'] for m in risk_metrics])
            dates = [m['date'] for m in risk_metrics]
            
            # 创建子图
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=('夏普比率趋势', '波动率趋势', '最大回撤趋势'),
                vertical_spacing=0.1
            )
            
            # 夏普比率
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=df_risk['sharpe_ratio'],
                    mode='lines+markers',
                    name='夏普比率',
                    line=dict(color='#C73E1D', width=2)
                ),
                row=1, col=1
            )
            fig.add_hline(y=1.5, line_dash="dash", line_color="green", 
                         annotation_text="目标(1.5)", row=1, col=1)
            
            # 波动率
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=df_risk['volatility'] * 100,
                    mode='lines+markers',
                    name='波动率',
                    line=dict(color='#3E92CC', width=2)
                ),
                row=2, col=1
            )
            
            # 最大回撤
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=df_risk['max_drawdown'] * 100,
                    mode='lines+markers',
                    name='最大回撤',
                    line=dict(color='#FF6B6B', width=2)
                ),
                row=3, col=1
            )
            fig.add_hline(y=10, line_dash="dash", line_color="red", 
                         annotation_text="警戒线(10%)", row=3, col=1)
            
            fig.update_layout(height=800, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_evolution_milestones(self, evolution_data):
        """渲染进化里程碑"""
        st.subheader("🏆 进化里程碑")
        
        evolution_history = evolution_data.get('evolution_history', [])
        if evolution_history:
            milestones = []
            
            for record in evolution_history:
                score = record.get('overall_score', 0)
                daily_return = record.get('basic_stats', {}).get('total_pnl', 0) / 10000
                
                if score >= 80:
                    milestones.append({
                        'date': record['date'],
                        'type': 'excellent_score',
                        'description': f'策略评分达到优秀水平: {score}',
                        'icon': '🏆'
                    })
                
                if daily_return >= 0.30:
                    milestones.append({
                        'date': record['date'],
                        'type': 'high_return',
                        'description': f'日收益率达到高目标: {daily_return:.2%}',
                        'icon': '💰'
                    })
                
                if daily_return <= -0.15:
                    milestones.append({
                        'date': record['date'],
                        'type': 'risk_alert',
                        'description': f'触发风险警报: {daily_return:.2%}',
                        'icon': '⚠️'
                    })
            
            # 显示最近10个里程碑
            for milestone in milestones[-10:]:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{milestone['icon']} {milestone['date']}</h4>
                    <p>{milestone['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def generate_evolution_report(self):
        """生成进化报告"""
        try:
            from ai_modules.strategy_evolution_tracker import StrategyEvolutionTracker
            tracker = StrategyEvolutionTracker()
            tracker.export_evolution_report()
            st.success("✅ 进化报告已生成: data/evolution_report.html")
        except Exception as e:
            st.error(f"生成报告失败: {e}")
    
    def run(self):
        """运行仪表板"""
        # 加载数据
        evolution_data = self.load_evolution_data()
        performance_data = self.load_performance_data()
        
        # 渲染页面
        self.render_header()
        self.render_sidebar()
        
        # 主要内容区域
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_overview_metrics(evolution_data, performance_data)
            self.render_evolution_charts(evolution_data, performance_data)
            self.render_strategy_analysis(evolution_data)
        
        with col2:
            self.render_risk_metrics(performance_data)
            self.render_evolution_milestones(evolution_data)

def main():
    """主函数"""
    dashboard = TradingDashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 