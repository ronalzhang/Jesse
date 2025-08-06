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

# 设置页面配置
st.set_page_config(
    page_title="Jesse+ AI增强量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 专业金融仪表板风格
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* 主标题样式 */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #475569;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .success-metric {
        border-left: 4px solid #059669;
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
    }
    
    .warning-metric {
        border-left: 4px solid #d97706;
        background: linear-gradient(135deg, #451a03 0%, #78350f 100%);
    }
    
    .danger-metric {
        border-left: 4px solid #dc2626;
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
    }
    
    .info-metric {
        border-left: 4px solid #3b82f6;
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    }
    
    /* 图表容器样式 */
    .chart-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #475569;
        margin-bottom: 1.5rem;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 8px 8px 0 0;
        color: #f8fafc;
        border: 1px solid #475569;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
    }
    
    /* 数据表格样式 */
    .dataframe {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #f8fafc;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
    }
    
    /* 状态指示器 */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-running {
        background: #059669;
        box-shadow: 0 0 8px rgba(5, 150, 105, 0.6);
    }
    
    .status-stopped {
        background: #dc2626;
        box-shadow: 0 0 8px rgba(220, 38, 38, 0.6);
    }
    
    .status-warning {
        background: #d97706;
        box-shadow: 0 0 8px rgba(217, 119, 6, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# 设置日志
# setup_logging()
# logger = get_logger('jesse_plus_web')

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
        # 移除对Jesse框架的依赖
        # self.jesse_manager = JesseManager()
        # self.ai_enhancer = AIEnhancer()
        # self.system_monitor = SystemMonitor()
        
        # 获取实时数据连接器
        # self.data_connector = get_data_connector()
        
        # 模拟数据生成器
        self.data_generator = DataGenerator()
        
        # 初始化性能指标
        self.performance_metrics = {
            "total_return": 0.0,
            "win_rate": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
            "total_trades": 0,
            "ai_accuracy": 0.0
        }
        
        # 初始化策略进化数据
        self.strategy_evolution_data = {
            "generations": [],
            "best_fitness": [],
            "avg_fitness": [],
            "improvements": []
        }
        
        # 初始化风险指标
        self.risk_metrics = {
            "volatility": 0.0,
            "var_95": 0.0,
            "max_position": 0.0,
            "leverage": 0.0,
            "liquidity": 0.0
        }
        
    def render_header(self):
        """渲染页面头部"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Jesse+ AI增强量化交易系统</h1>
            <p>专业级量化交易平台 | AI驱动策略优化 | 实时风险监控</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统状态和控制面板
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            status_color = "success" if st.session_state.system_status == "运行中" else "danger"
            status_icon = "🟢" if st.session_state.system_status == "运行中" else "🔴"
            st.markdown(f"""
            <div class="metric-card {status_color}-metric">
                <h3>系统状态</h3>
                <h2>{status_icon} {st.session_state.system_status}</h2>
                <p>实时监控</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>活跃策略</h3>
                <h2>5</h2>
                <p>+2 今日新增</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            daily_return = 2.5
            color = "success" if daily_return >= 3.0 else "warning" if daily_return >= 0 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>今日收益</h3>
                <h2>{daily_return:.1f}%</h2>
                <p>+0.8% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>总资产</h3>
                <h2>$125,430</h2>
                <p>+$3,240 今日</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            ai_accuracy = 68.5
            color = "success" if ai_accuracy >= 70 else "warning" if ai_accuracy >= 60 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>AI预测准确率</h3>
                <h2>{ai_accuracy:.1f}%</h2>
                <p>+2.1% 较昨日</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """渲染侧边栏"""
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="color: white; margin: 0;">🎛️ 控制面板</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统控制
        st.sidebar.subheader("🚀 系统控制")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🟢 启动系统", key="start_system", use_container_width=True):
                st.session_state.system_status = "运行中"
                st.success("✅ 系统已启动")
        with col2:
            if st.button("🔴 停止系统", key="stop_system", use_container_width=True):
                st.session_state.system_status = "停止"
                st.error("❌ 系统已停止")
        
        # 紧急操作
        st.sidebar.subheader("⚠️ 紧急操作")
        if st.sidebar.button("🛑 紧急停止", key="emergency_stop", use_container_width=True):
            st.session_state.system_status = "紧急停止"
            st.error("🚨 系统已紧急停止")
        
        # 实时监控开关
        st.sidebar.subheader("📊 监控设置")
        show_ai_process = st.sidebar.checkbox("显示AI分析过程", value=True)
        show_decision_process = st.sidebar.checkbox("显示决策过程", value=True)
        show_evolution_process = st.sidebar.checkbox("显示策略进化", value=True)
        auto_refresh = st.sidebar.checkbox("自动刷新", value=True)
        
        # 策略管理
        st.sidebar.subheader("🎯 策略管理")
        strategy_options = [
            "AI增强策略", "移动平均线交叉策略", "RSI策略", 
            "MACD策略", "布林带策略", "套利策略"
        ]
        selected_strategies = st.sidebar.multiselect(
            "选择活跃策略",
            strategy_options,
            default=["AI增强策略", "移动平均线交叉策略"]
        )
        
        # AI配置
        st.sidebar.subheader("🤖 AI配置")
        ai_enabled = st.sidebar.checkbox("启用AI增强", value=True)
        prediction_horizon = st.sidebar.slider("预测周期(小时)", 1, 24, 6)
        confidence_threshold = st.sidebar.slider("置信度阈值", 0.0, 1.0, 0.7)
        
        # 风险控制
        st.sidebar.subheader("🛡️ 风险控制")
        max_position_size = st.sidebar.number_input("最大仓位(%)", 1, 100, 10)
        stop_loss = st.sidebar.number_input("止损(%)", 1, 20, 5)
        max_daily_loss = st.sidebar.number_input("日最大亏损(%)", 1, 50, 15)
        
        # 实时状态
        st.sidebar.subheader("📈 实时状态")
        st.sidebar.metric("当前收益", "2.5%", "0.3%")
        st.sidebar.metric("今日交易", "15", "3")
        st.sidebar.metric("胜率", "68%", "2%")
        st.sidebar.metric("最大回撤", "8.2%", "-0.5%")
        
        return {
            "selected_strategies": selected_strategies,
            "ai_enabled": ai_enabled,
            "prediction_horizon": prediction_horizon,
            "confidence_threshold": confidence_threshold,
            "max_position_size": max_position_size,
            "stop_loss": stop_loss,
            "max_daily_loss": max_daily_loss,
            "show_ai_process": show_ai_process,
            "show_decision_process": show_decision_process,
            "show_evolution_process": show_evolution_process,
            "auto_refresh": auto_refresh
        }
    
    def render_dashboard(self):
        """渲染主仪表板"""
        # 创建标签页
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "📊 系统概览", "💰 多交易所价格", "🤖 AI分析过程", "🧠 决策过程", "🧬 策略进化", 
            "📈 交易记录", "🛡️ 风险控制", "⚙️ 系统配置", "📋 日志"
        ])
        
        with tab1:
            self.render_system_overview()
        
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
            self.render_risk_control()
            
        with tab8:
            self.render_system_config()
            
        with tab9:
            self.render_logs()
    

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
            refresh_button = st.button("🔄 刷新价格", key="refresh_prices", use_container_width=True)
        
        # 获取价格数据
        try:
            # from data.multi_exchange_price_collector import get_price_collector
            # price_collector = get_price_collector()
            
            if refresh_button or 'price_data' not in st.session_state:
                with st.spinner("正在获取多交易所价格数据..."):
                    # price_data = price_collector.get_price_comparison_chart_data(selected_symbol)
                    # st.session_state.price_data = price_data
                    # 模拟数据生成
                    dates = pd.date_range(start='2024-01-01', periods=10, freq='H')
                    prices = self.data_generator.generate_price_data(10)
                    volumes = self.data_generator.generate_volume_data(10)
                    exchanges = ["Binance", "OKX", "Bybit", "Gate.io"]
                    last_prices = prices
                    bid_prices = [p * 0.999 for p in prices]
                    ask_prices = [p * 1.001 for p in prices]
                    high_prices = [p * 1.005 for p in prices]
                    low_prices = [p * 0.995 for p in prices]
                    volumes_data = volumes
                    
                    st.session_state.price_data = {
                        'exchanges': exchanges,
                        'last_prices': last_prices,
                        'bid_prices': bid_prices,
                        'ask_prices': ask_prices,
                        'high_prices': high_prices,
                        'low_prices': low_prices,
                        'volumes': volumes_data
                    }
            
            price_data = st.session_state.get('price_data', {})
            
            if price_data and 'exchanges' in price_data:
                # 价格对比图表
                st.markdown("""
                <div class="chart-container">
                    <h4>多交易所价格对比</h4>
                </div>
                """, unsafe_allow_html=True)
                
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
                    showlegend=True,
                    template="plotly_dark"
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
                    
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h3>最高价</h3>
                        <h2>${max_price:.2f}</h2>
                        <p>交易所价格</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h3>最低价</h3>
                        <h2>${min_price:.2f}</h2>
                        <p>交易所价格</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    color = "success" if spread_percentage > 0.1 else "warning"
                    st.markdown(f"""
                    <div class="metric-card {color}-metric">
                        <h3>价差</h3>
                        <h2>${price_spread:.2f}</h2>
                        <p>{spread_percentage:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
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
            <div class="chart-container">
                <h4>策略原理</h4>
                <ul>
                    <li>监控多个交易所的同一币种价格</li>
                    <li>发现价格差异超过阈值时执行套利</li>
                    <li>在低价交易所买入，高价交易所卖出</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
                <h4>风险控制</h4>
                <ul>
                    <li>设置最小价差阈值（0.1%）</li>
                    <li>考虑交易手续费和滑点</li>
                    <li>实时监控市场波动</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
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
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{step["步骤"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                status_color = "success" if "完成" in step["状态"] else "warning" if "进行中" in step["状态"] else "danger"
                st.markdown(f"""
                <div class="metric-card {status_color}-metric">
                    <h4>{step["状态"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{step["时间"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{step["详情"]}</h4>
                </div>
                """, unsafe_allow_html=True)
        
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
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h4>{model}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    status_color = "success" if "运行中" in status["状态"] else "warning"
                    st.markdown(f"""
                    <div class="metric-card {status_color}-metric">
                        <h4>{status["状态"]}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h4>准确率: {status['准确率']}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        
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
                height=300,
                template="plotly_dark"
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
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{step["阶段"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                status_color = "success" if "完成" in step["状态"] else "warning" if "进行中" in step["状态"] else "danger"
                st.markdown(f"""
                <div class="metric-card {status_color}-metric">
                    <h4>{step["状态"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{step["信号"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>置信度: {step['置信度']}</h4>
                </div>
                """, unsafe_allow_html=True)
        
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
                hole=0.3,
                marker_colors=['#1e3a8a', '#3b82f6', '#059669', '#d97706']
            )])
            fig.update_layout(
                title="决策因素权重分布",
                template="plotly_dark"
            )
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
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h4>{key}:</h4>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card info-metric">
                        <h4>{value}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        
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
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{event["时间"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card info-metric">
                    <h4>{event["事件"]}</h4>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                status_color = "success" if "完成" in event["状态"] else "warning" if "进行中" in event["状态"] else "danger"
                st.markdown(f"""
                <div class="metric-card {status_color}-metric">
                    <h4>{event["状态"]}</h4>
                </div>
                """, unsafe_allow_html=True)
        
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
                height=400,
                template="plotly_dark"
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
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>训练回合</h3>
                <h2>1,234</h2>
                <p>+56 今日</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>平均奖励</h3>
                <h2>0.78</h2>
                <p>+0.05 改进</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card warning-metric">
                <h3>探索率</h3>
                <h2>0.15</h2>
                <p>-0.02 调整</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>学习率</h3>
                <h2>0.001</h2>
                <p>稳定</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 训练进度条
        training_progress = st.progress(0.65)
        st.write("强化学习训练进度: 65%")
    
    def render_trading_records(self):
        """渲染交易记录"""
        st.subheader("📈 交易记录")
        
        # 交易统计概览
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>总交易次数</h3>
                <h2>156</h2>
                <p>今日新增</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>胜率</h3>
                <h2>68%</h2>
                <p>目标: > 60%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>平均收益</h3>
                <h2>2.3%</h2>
                <p>每笔交易</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>AI准确率</h3>
                <h2>72.1%</h2>
                <p>预测准确</p>
            </div>
            """, unsafe_allow_html=True)
        
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
        
        # 交易分析图表
        st.subheader("📊 交易分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 收益分布
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=trading_records["收益"],
                nbinsx=10,
                name='收益分布',
                marker_color='#00ff88'
            ))
            fig.update_layout(
                title="交易收益分布",
                xaxis_title="收益 (%)",
                yaxis_title="频次",
                height=400,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 置信度分布
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=trading_records["AI置信度"],
                nbinsx=10,
                name='AI置信度分布',
                marker_color='#3b82f6'
            ))
            fig.update_layout(
                title="AI置信度分布",
                xaxis_title="置信度",
                yaxis_title="频次",
                height=400,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_system_config(self):
        """渲染系统配置"""
        st.subheader("⚙️ 系统配置")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
                <h4>数据库配置</h4>
            </div>
            """, unsafe_allow_html=True)
            
            db_host = st.text_input("数据库主机", value="localhost")
            db_port = st.number_input("数据库端口", value=27017)
            db_name = st.text_input("数据库名称", value="jesse_plus")
            
            st.markdown("""
            <div class="chart-container">
                <h4>交易所配置</h4>
            </div>
            """, unsafe_allow_html=True)
            
            exchange = st.selectbox("交易所", ["Binance", "OKX", "Bybit", "Gate.io"])
            api_key = st.text_input("API Key", type="password")
            api_secret = st.text_input("API Secret", type="password")
        
        with col2:
            st.markdown("""
            <div class="chart-container">
                <h4>AI模型配置</h4>
            </div>
            """, unsafe_allow_html=True)
            
            lstm_units = st.number_input("LSTM单元数", value=128)
            transformer_layers = st.number_input("Transformer层数", value=6)
            learning_rate = st.number_input("学习率", value=0.001, format="%.4f")
            
            st.markdown("""
            <div class="chart-container">
                <h4>风险控制</h4>
            </div>
            """, unsafe_allow_html=True)
            
            max_drawdown = st.number_input("最大回撤(%)", value=10)
            daily_loss_limit = st.number_input("日损失限制(%)", value=5)
            
        if st.button("💾 保存配置", use_container_width=True):
            st.success("✅ 配置已保存")
    
    def render_logs(self):
        """渲染日志"""
        st.subheader("📋 系统日志")
        
        # 日志过滤器
        col1, col2 = st.columns(2)
        with col1:
            selected_level = st.selectbox("日志级别", ["ALL", "INFO", "WARNING", "ERROR", "DEBUG"])
        with col2:
            search_term = st.text_input("搜索日志")
        
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
                            st.markdown(f"""
                            <div class="metric-card danger-metric">
                                <h4>[{timestamp.strftime('%H:%M:%S')}] {level}: {message}</h4>
                            </div>
                            """, unsafe_allow_html=True)
                        elif level == "WARNING":
                            st.markdown(f"""
                            <div class="metric-card warning-metric">
                                <h4>[{timestamp.strftime('%H:%M:%S')}] {level}: {message}</h4>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="metric-card info-metric">
                                <h4>[{timestamp.strftime('%H:%M:%S')}] {level}: {message}</h4>
                            </div>
                            """, unsafe_allow_html=True)

    def render_system_overview(self):
        """渲染系统概览"""
        st.subheader("📊 系统概览仪表板")
        
        # 关键指标展示
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>今日收益率</h3>
                <h2>2.5%</h2>
                <p>目标: 3% - 30%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>交易次数</h3>
                <h2>15</h2>
                <p>高频交易</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>胜率</h3>
                <h2>68%</h2>
                <p>目标: > 60%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card warning-metric">
                <h3>策略评分</h3>
                <h2>75.2</h2>
                <p>满分: 100</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 实时状态监控
        st.subheader("🔄 实时状态监控")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>数据收集</h3>
                <h2>✅ 正常</h2>
                <p>实时更新</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>AI分析</h3>
                <h2>✅ 运行中</h2>
                <p>68.5%准确率</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card success-metric">
                <h3>策略执行</h3>
                <h2>✅ 活跃</h2>
                <p>5个策略</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card info-metric">
                <h3>风险控制</h3>
                <h2>✅ 监控中</h2>
                <p>安全状态</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 市场数据
        st.subheader("📈 市场数据")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
                <h4>价格走势</h4>
            </div>
            """, unsafe_allow_html=True)
            
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
                height=400,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
                <h4>交易量</h4>
            </div>
            """, unsafe_allow_html=True)
            
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
                height=400,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 策略性能
        st.subheader("🎯 策略性能")
        performance_data = {
            "策略": ["AI增强策略", "移动平均线策略", "RSI策略", "MACD策略", "布林带策略"],
            "收益率": [2.5, 1.8, 1.2, 0.9, 1.5],
            "胜率": [68, 62, 58, 55, 60],
            "最大回撤": [3.2, 4.1, 5.8, 6.2, 4.5],
            "夏普比率": [1.8, 1.5, 1.2, 0.9, 1.4]
        }
        
        df_performance = pd.DataFrame(performance_data)
        st.dataframe(df_performance, use_container_width=True)

    def render_risk_control(self):
        """渲染风险控制"""
        st.subheader("🛡️ 风险控制监控")
        
        # 风险指标概览
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            sharpe_ratio = 1.8
            color = "success" if sharpe_ratio >= 1.5 else "warning" if sharpe_ratio >= 1.0 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>夏普比率</h3>
                <h2>{sharpe_ratio:.1f}</h2>
                <p>目标: > 1.5</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            volatility = 12.5
            color = "success" if volatility <= 15 else "warning" if volatility <= 25 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>波动率</h3>
                <h2>{volatility:.1f}%</h2>
                <p>目标: < 15%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            max_drawdown = 8.2
            color = "success" if max_drawdown <= 10 else "warning" if max_drawdown <= 15 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>最大回撤</h3>
                <h2>{max_drawdown:.1f}%</h2>
                <p>警戒: > 10%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            var_95 = 2.1
            color = "success" if var_95 <= 3 else "warning" if var_95 <= 5 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h3>VaR(95%)</h3>
                <h2>{var_95:.1f}%</h2>
                <p>目标: < 3%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 风险趋势图表
        st.subheader("📊 风险趋势分析")
        col1, col2 = st.columns(2)
        
        with col1:
            # 夏普比率趋势
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            sharpe_ratios = [1.2 + np.random.normal(0, 0.2) for _ in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=sharpe_ratios,
                mode='lines+markers',
                name='夏普比率',
                line=dict(color='#059669', width=2)
            ))
            fig.add_hline(y=1.5, line_dash="dash", line_color="green", 
                         annotation_text="目标线(1.5)")
            fig.update_layout(
                title="夏普比率趋势",
                xaxis_title="日期",
                yaxis_title="夏普比率",
                height=300,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 波动率趋势
            volatilities = [10 + np.random.normal(0, 3) for _ in range(30)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, y=volatilities,
                mode='lines+markers',
                name='波动率',
                line=dict(color='#d97706', width=2)
            ))
            fig.add_hline(y=15, line_dash="dash", line_color="orange", 
                         annotation_text="警戒线(15%)")
            fig.update_layout(
                title="波动率趋势",
                xaxis_title="日期",
                yaxis_title="波动率 (%)",
                height=300,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 风险指标仪表板
        st.subheader("🎛️ 风险指标仪表板")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
                <h4>最大仓位监控</h4>
            </div>
            """, unsafe_allow_html=True)
            
            position_sizes = [15, 12, 18, 10, 20, 16, 14, 17, 13, 19]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=position_sizes[-1],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "当前仓位 (%)"},
                delta={'reference': 15},
                gauge={
                    'axis': {'range': [None, 30]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 10], 'color': "lightgray"},
                        {'range': [10, 20], 'color': "gray"},
                        {'range': [20, 30], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 25
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
                <h4>杠杆率监控</h4>
            </div>
            """, unsafe_allow_html=True)
            
            leverage_ratios = [1.2, 1.5, 1.8, 1.3, 1.6, 1.4, 1.7, 1.1, 1.9, 1.2]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=leverage_ratios[-1],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "当前杠杆率"},
                delta={'reference': 1.5},
                gauge={
                    'axis': {'range': [None, 3]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 1], 'color': "lightgray"},
                        {'range': [1, 2], 'color': "gray"},
                        {'range': [2, 3], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 2.5
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("""
            <div class="chart-container">
                <h4>流动性指标</h4>
            </div>
            """, unsafe_allow_html=True)
            
            liquidity_scores = [85, 78, 92, 88, 76, 90, 82, 95, 87, 89]
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=liquidity_scores[-1],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "流动性评分"},
                delta={'reference': 85},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # 风险预警
        st.subheader("⚠️ 风险预警")
        
        risk_alerts = [
            {"级别": "🟡 警告", "内容": "波动率接近警戒线", "时间": "2024-01-01 14:30"},
            {"级别": "🟢 正常", "内容": "夏普比率表现良好", "时间": "2024-01-01 14:25"},
            {"级别": "🟡 警告", "内容": "最大回撤接近10%", "时间": "2024-01-01 14:20"},
            {"级别": "🟢 正常", "内容": "VaR指标在安全范围", "时间": "2024-01-01 14:15"}
        ]
        
        for alert in risk_alerts:
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                st.write(alert["级别"])
            with col2:
                st.write(alert["内容"])
            with col3:
                st.write(alert["时间"])

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
    try:
        # 创建Web界面实例
        web_interface = JessePlusWebInterface()
        
        # 渲染界面
        web_interface.render_header()
        
        # 获取侧边栏配置
        config = web_interface.render_sidebar()
        
        # 渲染主仪表板
        web_interface.render_dashboard()
        
        # 自动刷新（仅在启用时）
        if config.get("auto_refresh", True):
            # 使用st.empty()来避免页面闪烁
            with st.empty():
                time.sleep(5)
                st.rerun()
                
    except Exception as e:
        st.error(f"❌ 系统错误: {e}")
        st.info("💡 请检查系统配置和网络连接")
        print(f"Web界面运行错误: {e}")

if __name__ == "__main__":
    main() 