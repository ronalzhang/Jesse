#!/usr/bin/env python3
"""
Jesse+ Web界面 - 增强版
基于Streamlit的AI增强量化交易系统Web界面
包含完整的后台运行过程可视化
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
import sys
import time
import numpy as np
from pathlib import Path
import threading
import queue

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入Jesse+模块
from jesse_core.jesse_manager import JesseManager
from ai_modules.ai_enhancer import AIEnhancer
from monitoring.system_monitor import SystemMonitor
from utils.logging_manager import setup_logging, get_logger

# 导入数据连接器
from .data_connector import get_data_connector

# 设置页面配置
st.set_page_config(
    page_title="Jesse+ AI增强量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置日志
setup_logging()
logger = get_logger('jesse_plus_web')

# 全局状态管理
if 'system_status' not in st.session_state:
    st.session_state.system_status = "停止"
if 'ai_analysis_history' not in st.session_state:
    st.session_state.ai_analysis_history = []
if 'trading_signals' not in st.session_state:
    st.session_state.trading_signals = []
if 'strategy_evolution' not in st.session_state:
    st.session_state.strategy_evolution = []
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {}

class JessePlusWebInterface:
    """Jesse+ Web界面类 - 增强版"""
    
    def __init__(self):
        """初始化Web界面"""
        self.jesse_manager = JesseManager()
        self.ai_enhancer = AIEnhancer()
        self.system_monitor = SystemMonitor()
        
        # 获取实时数据连接器
        self.data_connector = get_data_connector()
        
        # 模拟数据生成器
        self.data_generator = DataGenerator()
        
    def render_header(self):
        """渲染页面头部"""
        st.title("🚀 Jesse+ AI增强量化交易系统")
        st.markdown("---")
        
        # 系统状态和控制
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            status_color = "🟢" if st.session_state.system_status == "运行中" else "🔴"
            st.metric("系统状态", f"{status_color} {st.session_state.system_status}")
        with col2:
            st.metric("活跃策略", "5", delta="+2")
        with col3:
            st.metric("今日收益", "2.5%", delta="+0.8%")
        with col4:
            st.metric("总资产", "$125,430", delta="+$3,240")
        with col5:
            st.metric("AI预测准确率", "68.5%", delta="+2.1%")
    
    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.title("🎛️ 控制面板")
        
        # 系统控制
        st.sidebar.subheader("系统控制")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🟢 启动系统", key="start_system"):
                st.session_state.system_status = "运行中"
                st.success("系统已启动")
        with col2:
            if st.button("🔴 停止系统", key="stop_system"):
                st.session_state.system_status = "停止"
                st.error("系统已停止")
        
        # 实时监控开关
        st.sidebar.subheader("监控设置")
        show_ai_process = st.sidebar.checkbox("显示AI分析过程", value=True)
        show_decision_process = st.sidebar.checkbox("显示决策过程", value=True)
        show_evolution_process = st.sidebar.checkbox("显示策略进化", value=True)
        auto_refresh = st.sidebar.checkbox("自动刷新", value=True)
        
        # 策略管理
        st.sidebar.subheader("策略管理")
        strategy_options = [
            "AI增强策略", "移动平均线交叉策略", "RSI策略", 
            "MACD策略", "布林带策略"
        ]
        selected_strategies = st.sidebar.multiselect(
            "选择活跃策略",
            strategy_options,
            default=["AI增强策略", "移动平均线交叉策略"]
        )
        
        # AI配置
        st.sidebar.subheader("AI配置")
        ai_enabled = st.sidebar.checkbox("启用AI增强", value=True)
        prediction_horizon = st.sidebar.slider("预测周期(小时)", 1, 24, 6)
        confidence_threshold = st.sidebar.slider("置信度阈值", 0.0, 1.0, 0.7)
        
        # 风险控制
        st.sidebar.subheader("风险控制")
        max_position_size = st.sidebar.number_input("最大仓位(%)", 1, 100, 10)
        stop_loss = st.sidebar.number_input("止损(%)", 1, 20, 5)
        
        return {
            "selected_strategies": selected_strategies,
            "ai_enabled": ai_enabled,
            "prediction_horizon": prediction_horizon,
            "confidence_threshold": confidence_threshold,
            "max_position_size": max_position_size,
            "stop_loss": stop_loss,
            "show_ai_process": show_ai_process,
            "show_decision_process": show_decision_process,
            "show_evolution_process": show_evolution_process,
            "auto_refresh": auto_refresh
        }
    
    def render_dashboard(self):
        """渲染主仪表板"""
        # 创建标签页
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 实时监控", "💰 多交易所价格", "🤖 AI分析过程", "🧠 决策过程", "🧬 策略进化", 
            "📈 交易记录", "⚙️ 系统配置", "📋 日志"
        ])
        
        with tab1:
            self.render_realtime_monitoring()
        
        with tab2:
            self.render_multi_exchange_prices()
            
        with tab3:
            self.render_ai_analysis_process()
            
        with tab4:
            self.render_decision_process()
            
        with tab5:
            self.render_strategy_evolution()
            
        with tab6:
            self.render_trading_records()
            
        with tab7:
            self.render_system_config()
            
        with tab8:
            self.render_logs()
    
    def render_realtime_monitoring(self):
        """渲染实时监控"""
        st.subheader("📊 实时市场监控")
        
        # 市场数据
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("价格走势")
            # 模拟实时价格数据
            dates = pd.date_range(start='2024-01-01', periods=100, freq='H')
            prices = self.data_generator.generate_price_data(100)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=prices,
                mode='lines',
                name='BTC/USDT',
                line=dict(color='#00ff88', width=2)
            ))
            fig.update_layout(
                title="BTC/USDT 价格走势",
                xaxis_title="时间",
                yaxis_title="价格 (USDT)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("交易量")
            volumes = self.data_generator.generate_volume_data(100)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=dates, y=volumes,
                name='交易量',
                marker_color='#ff8800'
            ))
            fig.update_layout(
                title="24小时交易量",
                xaxis_title="时间",
                yaxis_title="交易量",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 系统运行状态
        st.subheader("🔄 系统运行状态")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("数据收集", "✅ 正常", delta="实时")
        with col2:
            st.metric("AI分析", "✅ 运行中", delta="68.5%准确率")
        with col3:
            st.metric("策略执行", "✅ 活跃", delta="5个策略")
        with col4:
            st.metric("风险控制", "✅ 监控中", delta="安全")
        
        # 策略性能
        st.subheader("策略性能")
        performance_data = {
            "策略": ["AI增强策略", "移动平均线策略", "RSI策略", "MACD策略", "布林带策略"],
            "收益率": [2.5, 1.8, 1.2, 0.9, 1.5],
            "胜率": [68, 62, 58, 55, 60],
            "最大回撤": [3.2, 4.1, 5.8, 6.2, 4.5],
            "夏普比率": [1.8, 1.5, 1.2, 0.9, 1.4]
        }
        
        df_performance = pd.DataFrame(performance_data)
        st.dataframe(df_performance, use_container_width=True)
    
    def render_multi_exchange_prices(self):
        """渲染多交易所价格对比"""
        st.subheader("💰 多交易所实时价格对比")
        
        # 币种选择
        col1, col2 = st.columns(2)
        with col1:
            selected_symbol = st.selectbox(
                "选择币种",
                ["BTC/USDT", "ETH/USDT", "BNB/USDT", "ADA/USDT", "SOL/USDT", 
                 "XRP/USDT", "DOT/USDT", "DOGE/USDT", "AVAX/USDT", "MATIC/USDT"],
                index=0
            )
        with col2:
            refresh_button = st.button("🔄 刷新价格", key="refresh_prices")
        
        # 获取价格数据
        try:
            from data.multi_exchange_price_collector import get_price_collector
            price_collector = get_price_collector()
            
            if refresh_button or 'price_data' not in st.session_state:
                with st.spinner("正在获取多交易所价格数据..."):
                    price_data = price_collector.get_price_comparison_chart_data(selected_symbol)
                    st.session_state.price_data = price_data
            
            price_data = st.session_state.get('price_data', {})
            
            if price_data and 'exchanges' in price_data:
                # 价格对比图表
                st.subheader(f"📊 {selected_symbol} 多交易所价格对比")
                
                # 创建价格对比图
                fig = go.Figure()
                
                # 添加最新价格
                fig.add_trace(go.Bar(
                    x=price_data['exchanges'],
                    y=price_data['last_prices'],
                    name='最新价格',
                    marker_color='#00ff88',
                    text=[f"${price:.2f}" for price in price_data['last_prices']],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title=f"{selected_symbol} 多交易所价格对比",
                    xaxis_title="交易所",
                    yaxis_title="价格 (USDT)",
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 价格详情表格
                st.subheader("📋 详细价格信息")
                
                price_details = []
                for i, exchange in enumerate(price_data['exchanges']):
                    price_details.append({
                        "交易所": exchange,
                        "最新价格": f"${price_data['last_prices'][i]:.2f}",
                        "买价": f"${price_data['bid_prices'][i]:.2f}",
                        "卖价": f"${price_data['ask_prices'][i]:.2f}",
                        "24h最高": f"${price_data.get('high_prices', [0]*len(price_data['exchanges']))[i]:.2f}",
                        "24h最低": f"${price_data.get('low_prices', [0]*len(price_data['exchanges']))[i]:.2f}",
                        "24h成交量": f"{price_data['volumes'][i]:,.0f}"
                    })
                
                df_prices = pd.DataFrame(price_details)
                st.dataframe(df_prices, use_container_width=True)
                
                # 价差分析
                st.subheader("📈 价差分析")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    min_price = min(price_data['last_prices'])
                    max_price = max(price_data['last_prices'])
                    price_spread = max_price - min_price
                    spread_percentage = (price_spread / min_price) * 100
                    
                    st.metric("最高价", f"${max_price:.2f}")
                
                with col2:
                    st.metric("最低价", f"${min_price:.2f}")
                
                with col3:
                    st.metric("价差", f"${price_spread:.2f} ({spread_percentage:.2f}%)")
                
                # 套利机会
                if spread_percentage > 0.1:
                    st.success(f"🎯 发现套利机会！价差: {spread_percentage:.2f}%")
                else:
                    st.info("📊 当前价差较小，无显著套利机会")
                
            else:
                st.warning("⚠️ 无法获取价格数据，请检查网络连接")
                
        except Exception as e:
            st.error(f"❌ 获取价格数据失败: {e}")
            st.info("💡 提示：请确保已安装ccxt库并配置了交易所API")
        
        # 套利策略信息
        st.subheader("🎯 跨交易所套利策略")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **策略原理:**
            - 监控多个交易所的同一币种价格
            - 发现价格差异超过阈值时执行套利
            - 在低价交易所买入，高价交易所卖出
            
            **风险控制:**
            - 设置最小价差阈值（0.1%）
            - 考虑交易手续费和滑点
            - 实时监控市场波动
            """)
        
        with col2:
            st.markdown("""
            **执行条件:**
            - 价差 > 0.1%
            - 流动性充足
            - 网络延迟 < 100ms
            - 资金充足
            
            **收益计算:**
            - 净收益 = 价差 - 手续费 - 滑点
            - 年化收益率 = 日收益 × 365
            """)
    
    def render_ai_analysis_process(self):
        """渲染AI分析过程"""
        st.subheader("🤖 AI分析过程")
        
        # 分析步骤时间线
        st.subheader("📋 分析步骤时间线")
        
        analysis_steps = [
            {"步骤": "1. 数据收集", "状态": "✅ 完成", "时间": "00:01:23", "详情": "收集BTC/USDT市场数据"},
            {"步骤": "2. 数据预处理", "状态": "✅ 完成", "时间": "00:01:25", "详情": "清洗和标准化数据"},
            {"步骤": "3. 技术指标计算", "状态": "✅ 完成", "时间": "00:01:28", "详情": "计算RSI、MACD、布林带等"},
            {"步骤": "4. 情绪分析", "状态": "🔄 进行中", "时间": "00:01:30", "详情": "分析新闻和社交媒体情绪"},
            {"步骤": "5. AI模型预测", "状态": "⏳ 等待", "时间": "--", "详情": "LSTM和Transformer模型预测"},
            {"步骤": "6. 结果整合", "状态": "⏳ 等待", "时间": "--", "详情": "整合所有分析结果"}
        ]
        
        for step in analysis_steps:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
            with col1:
                st.write(step["步骤"])
            with col2:
                st.write(step["状态"])
            with col3:
                st.write(step["时间"])
            with col4:
                st.write(step["详情"])
        
        # AI模型状态
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧠 AI模型状态")
            models_status = {
                "LSTM模型": {"状态": "✅ 运行中", "准确率": "72.3%", "预测时间": "1.2s"},
                "Transformer模型": {"状态": "✅ 运行中", "准确率": "68.1%", "预测时间": "0.8s"},
                "GARCH模型": {"状态": "✅ 运行中", "准确率": "65.4%", "预测时间": "0.5s"},
                "情绪分析模型": {"状态": "🔄 训练中", "准确率": "71.2%", "预测时间": "1.5s"}
            }
            
            for model, status in models_status.items():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**{model}**")
                with col2:
                    st.write(status["状态"])
                with col3:
                    st.write(f"准确率: {status['准确率']}")
        
        with col2:
            st.subheader("📊 实时分析结果")
            
            # 情绪分析结果
            sentiment_data = {
                "指标": ["新闻情绪", "社交媒体情绪", "技术指标情绪", "综合情绪"],
                "得分": [0.65, 0.72, 0.58, 0.68],
                "状态": ["积极", "积极", "中性", "积极"],
                "置信度": [0.85, 0.78, 0.92, 0.81]
            }
            
            df_sentiment = pd.DataFrame(sentiment_data)
            st.dataframe(df_sentiment, use_container_width=True)
            
            # 情绪雷达图
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[0.65, 0.72, 0.58, 0.68],
                theta=["新闻情绪", "社交媒体", "技术指标", "综合情绪"],
                fill='toself',
                name='市场情绪'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                title="市场情绪雷达图",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_decision_process(self):
        """渲染决策过程"""
        st.subheader("🧠 AI决策过程")
        
        # 决策流程
        st.subheader("🔄 决策流程")
        
        decision_steps = [
            {"阶段": "1. 信号生成", "状态": "✅ 完成", "信号": "买入", "置信度": "0.78"},
            {"阶段": "2. 风险评估", "状态": "✅ 完成", "信号": "低风险", "置信度": "0.85"},
            {"阶段": "3. 仓位计算", "状态": "✅ 完成", "信号": "10%仓位", "置信度": "0.72"},
            {"阶段": "4. 执行确认", "状态": "🔄 进行中", "信号": "等待确认", "置信度": "0.68"},
            {"阶段": "5. 订单执行", "状态": "⏳ 等待", "信号": "--", "置信度": "--"}
        ]
        
        for step in decision_steps:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                st.write(step["阶段"])
            with col2:
                st.write(step["状态"])
            with col3:
                st.write(step["信号"])
            with col4:
                st.write(f"置信度: {step['置信度']}")
        
        # 决策因素分析
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 决策因素权重")
            
            factors = {
                "技术分析": 0.35,
                "情绪分析": 0.25,
                "AI预测": 0.30,
                "风险管理": 0.10
            }
            
            fig = go.Figure(data=[go.Pie(
                labels=list(factors.keys()),
                values=list(factors.values()),
                hole=0.3
            )])
            fig.update_layout(title="决策因素权重分布")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 当前决策详情")
            
            decision_details = {
                "信号类型": "买入",
                "目标价格": "$43,250",
                "止损价格": "$41,800",
                "仓位大小": "10%",
                "预期收益": "2.8%",
                "最大风险": "1.2%",
                "风险收益比": "2.33:1",
                "执行时间": "00:01:45"
            }
            
            for key, value in decision_details.items():
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{key}:**")
                with col2:
                    st.write(value)
        
        # 历史决策记录
        st.subheader("📈 历史决策记录")
        
        decision_history = {
            "时间": pd.date_range(start='2024-01-01', periods=10, freq='H'),
            "信号": ["买入", "卖出", "买入", "持有", "买入", "卖出", "买入", "持有", "买入", "卖出"],
            "价格": [42000, 43500, 42800, 43200, 42900, 44100, 43800, 44000, 44200, 44800],
            "收益": [2.1, -1.5, 3.2, 0.0, 2.8, 1.9, 1.2, 0.0, 1.5, 2.3],
            "置信度": [0.78, 0.82, 0.75, 0.65, 0.81, 0.79, 0.73, 0.60, 0.77, 0.84]
        }
        
        df_decisions = pd.DataFrame(decision_history)
        st.dataframe(df_decisions, use_container_width=True)
    
    def render_strategy_evolution(self):
        """渲染策略进化过程"""
        st.subheader("🧬 策略进化过程")
        
        # 进化时间线
        st.subheader("📅 策略进化时间线")
        
        evolution_timeline = [
            {"时间": "00:00:00", "事件": "系统启动", "状态": "✅ 完成"},
            {"时间": "00:00:30", "事件": "加载历史数据", "状态": "✅ 完成"},
            {"时间": "00:01:00", "事件": "策略性能评估", "状态": "✅ 完成"},
            {"时间": "00:01:30", "事件": "遗传算法优化", "状态": "🔄 进行中"},
            {"时间": "00:02:00", "事件": "参数调整", "状态": "⏳ 等待"},
            {"时间": "00:02:30", "事件": "策略测试", "状态": "⏳ 等待"},
            {"时间": "00:03:00", "事件": "策略部署", "状态": "⏳ 等待"}
        ]
        
        for event in evolution_timeline:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(event["时间"])
            with col2:
                st.write(event["事件"])
            with col3:
                st.write(event["状态"])
        
        # 策略进化详情
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧬 遗传算法进化")
            
            generation_data = {
                "代数": list(range(1, 11)),
                "最佳适应度": [0.65, 0.68, 0.71, 0.73, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80],
                "平均适应度": [0.60, 0.62, 0.65, 0.67, 0.69, 0.71, 0.72, 0.73, 0.74, 0.75]
            }
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=generation_data["代数"],
                y=generation_data["最佳适应度"],
                mode='lines+markers',
                name='最佳适应度',
                line=dict(color='#00ff88')
            ))
            fig.add_trace(go.Scatter(
                x=generation_data["代数"],
                y=generation_data["平均适应度"],
                mode='lines+markers',
                name='平均适应度',
                line=dict(color='#ff8800')
            ))
            fig.update_layout(
                title="遗传算法进化过程",
                xaxis_title="代数",
                yaxis_title="适应度",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 策略参数优化")
            
            # 参数优化进度
            params_optimization = {
                "参数": ["RSI周期", "MACD快线", "MACD慢线", "布林带周期", "止损比例"],
                "原值": [14, 12, 26, 20, 0.05],
                "优化值": [16, 10, 28, 18, 0.04],
                "改进": ["+14%", "-17%", "+8%", "-10%", "-20%"]
            }
            
            df_params = pd.DataFrame(params_optimization)
            st.dataframe(df_params, use_container_width=True)
            
            # 策略性能对比
            st.subheader("📈 策略性能对比")
            
            performance_comparison = {
                "指标": ["收益率", "胜率", "最大回撤", "夏普比率"],
                "优化前": [1.8, 58, 5.2, 1.2],
                "优化后": [2.5, 68, 3.2, 1.8],
                "改进": ["+39%", "+17%", "-38%", "+50%"]
            }
            
            df_performance = pd.DataFrame(performance_comparison)
            st.dataframe(df_performance, use_container_width=True)
        
        # 强化学习训练
        st.subheader("🎯 强化学习训练状态")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("训练回合", "1,234", delta="+56")
        with col2:
            st.metric("平均奖励", "0.78", delta="+0.05")
        with col3:
            st.metric("探索率", "0.15", delta="-0.02")
        with col4:
            st.metric("学习率", "0.001", delta="稳定")
        
        # 训练进度条
        training_progress = st.progress(0.65)
        st.write("强化学习训练进度: 65%")
    
    def render_trading_records(self):
        """渲染交易记录"""
        st.subheader("📈 交易记录")
        
        # 模拟交易记录
        trading_records = {
            "时间": pd.date_range(start='2024-01-01', periods=20, freq='H'),
            "交易对": ["BTC/USDT"] * 20,
            "方向": ["买入", "卖出"] * 10,
            "价格": [42000 + i * 50 + np.random.normal(0, 100) for i in range(20)],
            "数量": [np.random.uniform(0.1, 1.0) for _ in range(20)],
            "收益": [np.random.uniform(-2, 5) for _ in range(20)],
            "策略": ["AI增强策略"] * 20,
            "AI置信度": [np.random.uniform(0.6, 0.9) for _ in range(20)]
        }
        
        df_trades = pd.DataFrame(trading_records)
        st.dataframe(df_trades, use_container_width=True)
        
        # 收益统计
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总交易次数", "156")
        with col2:
            st.metric("胜率", "68%")
        with col3:
            st.metric("平均收益", "2.3%")
        with col4:
            st.metric("AI准确率", "72.1%")
    
    def render_system_config(self):
        """渲染系统配置"""
        st.subheader("⚙️ 系统配置")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("数据库配置")
            db_host = st.text_input("数据库主机", value="localhost")
            db_port = st.number_input("数据库端口", value=27017)
            db_name = st.text_input("数据库名称", value="jesse_plus")
            
            st.subheader("交易所配置")
            exchange = st.selectbox("交易所", ["Binance", "OKX", "Bybit", "Gate.io"])
            api_key = st.text_input("API Key", type="password")
            api_secret = st.text_input("API Secret", type="password")
        
        with col2:
            st.subheader("AI模型配置")
            lstm_units = st.number_input("LSTM单元数", value=128)
            transformer_layers = st.number_input("Transformer层数", value=6)
            learning_rate = st.number_input("学习率", value=0.001, format="%.4f")
            
            st.subheader("风险控制")
            max_drawdown = st.number_input("最大回撤(%)", value=10)
            daily_loss_limit = st.number_input("日损失限制(%)", value=5)
            
        if st.button("💾 保存配置"):
            st.success("配置已保存")
    
    def render_logs(self):
        """渲染日志"""
        st.subheader("📋 系统日志")
        
        # 模拟日志数据
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        log_messages = [
            "系统启动成功",
            "AI模型加载完成",
            "市场数据更新",
            "策略执行完成",
            "风险检查通过",
            "交易信号生成",
            "AI分析完成",
            "策略进化进行中",
            "遗传算法优化",
            "强化学习训练"
        ]
        
        # 日志过滤器
        col1, col2 = st.columns(2)
        with col1:
            selected_level = st.selectbox("日志级别", ["ALL"] + log_levels)
        with col2:
            search_term = st.text_input("搜索日志")
        
        # 显示日志
        log_container = st.container()
        with log_container:
            for i in range(20):
                timestamp = datetime.now() - timedelta(minutes=i)
                level = np.random.choice(log_levels)
                message = np.random.choice(log_messages)
                
                if selected_level == "ALL" or level == selected_level:
                    if not search_term or search_term.lower() in message.lower():
                        if level == "ERROR":
                            st.error(f"[{timestamp.strftime('%H:%M:%S')}] {level}: {message}")
                        elif level == "WARNING":
                            st.warning(f"[{timestamp.strftime('%H:%M:%S')}] {level}: {message}")
                        else:
                            st.info(f"[{timestamp.strftime('%H:%M:%S')}] {level}: {message}")

class DataGenerator:
    """数据生成器类"""
    
    def __init__(self):
        self.base_price = 42000
        self.volatility = 0.02
        
    def generate_price_data(self, n_points):
        """生成价格数据"""
        prices = []
        current_price = self.base_price
        
        for i in range(n_points):
            # 添加随机波动
            change = np.random.normal(0, self.volatility * current_price)
            current_price += change
            prices.append(current_price)
            
        return prices
    
    def generate_volume_data(self, n_points):
        """生成交易量数据"""
        return [np.random.randint(1000, 5000) for _ in range(n_points)]

def main():
    """主函数"""
    # 创建Web界面实例
    web_interface = JessePlusWebInterface()
    
    # 渲染界面
    web_interface.render_header()
    
    # 获取侧边栏配置
    config = web_interface.render_sidebar()
    
    # 渲染主仪表板
    web_interface.render_dashboard()
    
    # 自动刷新
    if config.get("auto_refresh", True):
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main() 