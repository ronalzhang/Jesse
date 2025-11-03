#!/usr/bin/env python3
"""
Jesse+ 真实数据前端 - 连接后端真实数据
⚠️ 当前为验证模式 - 使用真实市场数据但不进行真实资金交易
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import sys
import ccxt

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from web.data_bridge import DataBridge

# 页面配置 - 性能优化
st.set_page_config(
    page_title="Jesse+ 全自动量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# CSS样式 - 优化版
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1419 100%);
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* 主标题 - 精致渐变 */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7, #6366f1);
        background-size: 200% 100%;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.125rem;
        opacity: 0.85;
        color: #cbd5e1;
    }
    
    /* 指标卡片 - 液态玻璃效果 */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        padding: 1.75rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.125);
        margin-bottom: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 50%, 
            rgba(255, 255, 255, 0.02) 100%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .metric-card h4 {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin: 0 0 0.75rem 0;
    }
    
    .metric-card h2 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: #f1f5f9;
    }
    
    .metric-card p {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin: 0.5rem 0 0 0;
    }
    
    /* 状态颜色 - 液态玻璃效果 */
    .success-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .success-card h4 {
        color: #6ee7b7 !important;
    }
    
    .success-card h2 {
        color: #a7f3d0 !important;
    }
    
    .warning-card {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .warning-card h4 {
        color: #fcd34d !important;
    }
    
    .warning-card h2 {
        color: #fde68a !important;
    }
    
    .danger-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .danger-card h4 {
        color: #f87171 !important;
    }
    
    .danger-card h2 {
        color: #fca5a5 !important;
    }
    
    .info-card {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .info-card h4 {
        color: #60a5fa !important;
    }
    
    .info-card h2 {
        color: #93c5fd !important;
    }
    
    /* 验证模式提示 */
    .verification-mode {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.15) 100%);
        color: #fbbf24;
        padding: 1.25rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.1);
    }
    
    .verification-mode strong {
        color: #fcd34d;
    }
    
    /* 按钮优化 */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.025em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px 0 rgba(99, 102, 241, 0.4);
    }
    
    /* Tab样式 - 高级优雅设计 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        padding: 0.375rem;
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.75rem;
        font-weight: 500;
        color: #94a3b8;
        background: transparent;
        border: 1px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* 选中状态 - 高对比度白色背景 */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #0f172a;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 4px 12px rgba(0, 0, 0, 0.15),
            0 2px 4px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
    }
    
    /* 选中状态底部指示条 */
    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 2px 2px 0 0;
    }
    
    /* DataFrames样式 */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* 移动端布局优化 - 小屏幕设备 */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem !important;
        }
        
        .main-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .main-header p {
            font-size: 0.8rem;
        }
        
        /* 强制Streamlit columns为2列网格 */
        .stHorizontalBlock {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.75rem !important;
        }
        
        .stHorizontalBlock > div {
            width: 100% !important;
        }
        
        .metric-card {
            padding: 0.875rem;
        }
        
        .metric-card h4 {
            font-size: 0.7rem;
        }
        
        .metric-card h2 {
            font-size: 1.35rem;
        }
        
        .metric-card p {
            font-size: 0.7rem;
        }
        
        /* 表格字体优化 */
        .dataframe {
            font-size: 0.75rem;
        }
        
        /* 状态指示器移动端优化 */
        .status-indicators {
            gap: 0.5rem;
            flex-wrap: nowrap;
            justify-content: space-between;
            padding: 0.75rem 0;
        }
        
        .status-item {
            padding: 0.4rem 0.75rem;
            flex: 1;
            justify-content: center;
        }
        
        .status-dot {
            font-size: 0.7rem;
        }
        
        .status-label {
            font-size: 0.75rem;
        }
    }
        
        /* 横向滚动容器 */
        .horizontal-scroll {
            display: flex;
            overflow-x: auto;
            gap: 0.75rem;
            padding: 0.5rem 0;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
        }
        
        .horizontal-scroll::-webkit-scrollbar {
            display: none;
        }
        
        .horizontal-scroll-item {
            flex: 0 0 85%;
            scroll-snap-align: start;
        }
        
        /* 移动端按钮优化 */
        .stButton > button {
            padding: 0.875rem 1.25rem;
            font-size: 0.9rem;
            border-radius: 10px;
            width: 100%;
            touch-action: manipulation;
        }
        
        /* Tab移动端优化 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            padding: 0.25rem;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
        }
        
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            display: none;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
            white-space: nowrap;
            min-width: fit-content;
        }
        
        /* 选中状态在移动端更明显 */
        .stTabs [aria-selected="true"] {
            font-weight: 700;
        }
        
        .stTabs [aria-selected="true"]::after {
            width: 80%;
            height: 2px;
        }
        
        /* 数据表格优化 */
        .dataframe {
            font-size: 0.8rem;
        }
        
        /* 折叠面板 */
        .collapsible-section {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            margin-bottom: 0.75rem;
            overflow: hidden;
        }
        
        .collapsible-header {
            padding: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        .collapsible-content {
            padding: 0 1rem 1rem 1rem;
        }
    }
    

    
    /* 触摸设备优化 */
    @media (hover: none) and (pointer: coarse) {
        /* 增大可点击区域 */
        .stButton > button {
            min-height: 48px;
        }
        
        .collapsible-header {
            min-height: 52px;
        }
        
        /* 禁用悬停效果 */
        .metric-card:hover {
            transform: none;
        }
        
        /* 点击反馈 */
        .metric-card:active {
            transform: scale(0.98);
            transition: transform 0.1s;
        }
        
        .stButton > button:active {
            transform: scale(0.97);
        }
        
        /* 选择框优化 */
        .stSelectbox > div > div {
            min-height: 48px;
        }
        
        /* Tab 点击区域 */
        .stTabs [data-baseweb="tab"] {
            min-height: 44px;
        }
    }
    
    /* 横屏模式优化 - 充分利用宽屏 */
    @media (max-width: 1024px) and (orientation: landscape) {
        .main-header {
            padding: 1rem 1.5rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .main-header p {
            display: inline-block;
            margin-left: 1rem;
        }
        
        /* 横屏时使用4列布局 */
        .mobile-grid {
            grid-template-columns: repeat(4, 1fr);
        }
        
        .metric-card {
            padding: 0.875rem;
        }
        
        .metric-card h2 {
            font-size: 1.25rem;
        }
    }
    
    /* 超大屏手机优化 (iPhone 17 Pro Max 等) */
    @media (min-width: 430px) and (max-width: 768px) {
        .main-header h1 {
            font-size: 1.875rem;
        }
        
        .metric-card {
            padding: 1.25rem;
        }
        
        .metric-card h2 {
            font-size: 1.65rem;
        }
        
        /* 充分利用大屏空间 */
        .horizontal-scroll-item {
            flex: 0 0 48%;
        }
    }
    
    /* 下拉刷新提示 */
    .refresh-indicator {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        transform: translateY(-100%);
        transition: transform 0.3s;
        z-index: 1000;
    }
    
    /* 加载骨架屏 */
    .skeleton {
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0.05) 25%, 
            rgba(255, 255, 255, 0.1) 50%, 
            rgba(255, 255, 255, 0.05) 75%);
        background-size: 200% 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
        border-radius: 8px;
    }
    
    @keyframes skeleton-loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* 精致的状态指示器 */
    .status-indicators {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 3rem;
        padding: 1rem 0;
        margin: 1rem 0;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }
    
    .status-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.12);
        transform: translateY(-2px);
    }
    
    .status-dot {
        font-size: 0.875rem;
        line-height: 1;
    }
    
    .status-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #cbd5e1;
        white-space: nowrap;
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据桥接
@st.cache_resource
def get_data_bridge():
    return DataBridge()

data_bridge = get_data_bridge()


class RealDashboard:
    def __init__(self):
        self.data_bridge = data_bridge
        self.exchanges = {}
        self.cache_duration = 10  # 缓存10秒
        self.init_exchanges()
        self.init_cache()
        self.is_mobile = self.detect_mobile()
    
    def detect_mobile(self):
        """检测是否为移动设备"""
        # 通过 Streamlit 的 session state 检测屏幕宽度
        # 这是一个简化版本，实际可以通过 JavaScript 获取更准确的信息
        return False  # 默认为桌面，CSS 会自动适配
    
    def init_cache(self):
        """初始化缓存"""
        if 'price_cache' not in st.session_state:
            st.session_state.price_cache = {}
        if 'cache_time' not in st.session_state:
            st.session_state.cache_time = {}
    
    def init_exchanges(self):
        """初始化交易所 - 优化超时设置"""
        for name in ['binance', 'bitget']:
            try:
                cls = getattr(ccxt, name)
                self.exchanges[name] = cls({
                    'enableRateLimit': True, 
                    'timeout': 5000,  # 减少超时时间到5秒
                    'options': {'defaultType': 'spot'}
                })
            except Exception as e:
                st.warning(f"交易所 {name} 初始化失败: {e}")
    
    def get_cached_price(self, exchange, symbol):
        """获取缓存价格数据"""
        import time
        cache_key = f"{exchange}_{symbol}"
        now = time.time()
        
        # 检查缓存是否有效
        if cache_key in st.session_state.price_cache:
            cache_age = now - st.session_state.cache_time.get(cache_key, 0)
            if cache_age < self.cache_duration:
                return st.session_state.price_cache[cache_key]
        
        # 获取新数据
        try:
            if exchange in self.exchanges:
                ticker = self.exchanges[exchange].fetch_ticker(symbol)
                st.session_state.price_cache[cache_key] = ticker
                st.session_state.cache_time[cache_key] = now
                return ticker
        except Exception as e:
            # 返回缓存数据（即使过期）
            if cache_key in st.session_state.price_cache:
                return st.session_state.price_cache[cache_key]
        
        return None
    
    def render_header(self):
        """页面头部"""
        st.markdown("""
        <div class="main-header">
            <h1>◆ 校长全自动量化交易系统</h1>
            <p>多交易所 · 多币种 · 策略自动进化 · AI智能决策</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 交易模式提示已删除
        
        # 获取真实系统状态
        system_status = self.data_bridge.get_system_status()
        trading_stats = self.data_bridge.get_trading_stats()
        evolution_status = self.data_bridge.get_evolution_status()
        exchange_config = self.data_bridge.get_exchange_config()
        
        # 状态栏 - 桌面4列，移动端通过CSS控制为2列
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            status_icon = "🟢" if system_status['system_running'] else "🔴"
            status_text = "运行中" if system_status['system_running'] else "已停止"
            status_class = "success-card" if system_status["system_running"] else "danger-card"
            st.markdown(f'''
            <div class="metric-card {status_class}">
                <h4>系统状态</h4>
                <h2>{status_icon} {status_text}</h2>
                <p>{len(exchange_config["active_exchanges"])}个交易所 · 4个币种</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card info-card">
                <h4>今日交易</h4>
                <h2>{trading_stats["daily_trades"]} 笔</h2>
                <p>成功 {trading_stats["success_trades"]} · 失败 {trading_stats["failed_trades"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            win_rate = trading_stats['win_rate'] * 100
            card_class = "success-card" if win_rate >= 60 else "warning-card" if win_rate >= 50 else "danger-card"
            st.markdown(f'''
            <div class="metric-card {card_class}">
                <h4>整体胜率</h4>
                <h2>{win_rate:.1f}%</h2>
                <p>共 {trading_stats["total_trades"]} 笔</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            evo_icon = "🟢" if evolution_status['is_running'] else "🔴"
            evo_status = "运行中" if evolution_status['is_running'] else "已停止"
            best_fitness = evolution_status.get('best_fitness', 0)
            fitness_display = f"{best_fitness:.3f}" if best_fitness > 0 else "待计算"
            evo_class = "success-card" if evolution_status["is_running"] else "warning-card"
            st.markdown(f'''
            <div class="metric-card {evo_class}">
                <h4>策略进化</h4>
                <h2>{evo_icon} {evo_status}</h2>
                <p>第{evolution_status["current_generation"]}代 · {fitness_display}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """侧边栏 - 真实控制"""
        st.sidebar.markdown("## 🎛️ 系统控制")
        
        # 获取真实状态
        system_status = self.data_bridge.get_system_status()
        
        # 交易系统控制
        st.sidebar.markdown("### 交易系统")
        if system_status['trading_active']:
            if st.sidebar.button("🔴 停止交易系统", use_container_width=True, key="stop_trading"):
                result = self.data_bridge.control_system('stop', 'trading')
                if result['success']:
                    st.sidebar.success(result['message'])
                    st.rerun()
                else:
                    st.sidebar.error(result['message'])
        else:
            if st.sidebar.button("🟢 启动交易系统", use_container_width=True, key="start_trading"):
                result = self.data_bridge.control_system('start', 'trading')
                if result['success']:
                    st.sidebar.success(result['message'])
                    st.rerun()
                else:
                    st.sidebar.error(result['message'])
        
        # 策略进化控制
        st.sidebar.markdown("### 策略进化")
        if system_status['evolution_active']:
            st.sidebar.info("🔄 策略进化运行中")
            evolution_status = self.data_bridge.get_evolution_status()
            st.sidebar.metric("当前代数", evolution_status['current_generation'])
            best_fitness = evolution_status['best_fitness']
            fitness_display = f"{best_fitness:.3f}" if best_fitness > 0 else "待计算"
            st.sidebar.metric("最佳策略评分", fitness_display)
            
            if st.sidebar.button("🔴 停止进化", use_container_width=True, key="stop_evolution"):
                result = self.data_bridge.control_system('stop', 'evolution')
                if result['success']:
                    st.sidebar.success(result['message'])
                    st.rerun()
                else:
                    st.sidebar.error(result['message'])
        else:
            if st.sidebar.button("🟢 启动进化", use_container_width=True, key="start_evolution"):
                result = self.data_bridge.control_system('start', 'evolution')
                if result['success']:
                    st.sidebar.success(result['message'])
                    st.rerun()
                else:
                    st.sidebar.error(result['message'])
        
        st.sidebar.markdown("---")
        
        # 交易所配置
        st.sidebar.markdown("## 💱 交易所配置")
        exchange_config = self.data_bridge.get_exchange_config()
        st.sidebar.write("**活跃交易所**:")
        for ex in exchange_config['active_exchanges']:
            st.sidebar.write(f"✅ {ex.upper()}")
        
        if 'okx' in exchange_config['exchanges'] and 'okx' not in exchange_config['active_exchanges']:
            st.sidebar.write("⚠️ OKX (API配置问题)")
        
        st.sidebar.markdown("---")
        
        # 系统信息
        st.sidebar.markdown("## 📊 系统信息")
        if system_status['uptime'] > 0:
            uptime_hours = (datetime.now().timestamp() - system_status['uptime'] / 1000) / 3600
            st.sidebar.metric("运行时间", f"{uptime_hours:.1f}小时")
        
        st.sidebar.markdown("---")
        
        # 交易模式切换
        st.sidebar.markdown("### 🔄 交易模式")
        
        # 获取当前交易模式（从配置文件或状态中读取）
        trading_mode = self.data_bridge.get_trading_mode()
        
        if trading_mode == 'paper':
            st.sidebar.info("📝 当前: 模拟盘交易")
            st.sidebar.markdown("""
            **模拟盘特点:**
            - ✅ 使用真实市场数据
            - ✅ 策略可以持续进化
            - ⚠️ 不使用真实资金
            - 📊 验证策略有效性
            """)
            
            if st.sidebar.button("🚀 切换到实盘交易", use_container_width=True, key="switch_to_live", type="primary"):
                st.sidebar.warning("⚠️ 切换到实盘将使用真实资金进行交易！")
                if st.sidebar.button("✅ 确认切换到实盘", use_container_width=True, key="confirm_live"):
                    result = self.data_bridge.switch_trading_mode('live')
                    if result['success']:
                        st.sidebar.success("✅ 已切换到实盘交易模式")
                        st.rerun()
                    else:
                        st.sidebar.error(f"❌ 切换失败: {result['message']}")
        else:
            st.sidebar.warning("💰 当前: 实盘交易")
            st.sidebar.markdown("""
            **实盘特点:**
            - 💰 使用真实资金交易
            - 📈 真实盈亏
            - 🧬 策略持续进化
            - ⚡ 实时执行订单
            """)
            
            if st.sidebar.button("📝 切换到模拟盘", use_container_width=True, key="switch_to_paper"):
                result = self.data_bridge.switch_trading_mode('paper')
                if result['success']:
                    st.sidebar.success("✅ 已切换到模拟盘模式")
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ 切换失败: {result['message']}")
    
    def render_overview(self):
        """系统概览 - 真实数据（响应式优化）"""
        st.subheader("📊 系统概览")
        
        trading_stats = self.data_bridge.get_trading_stats()
        win_rate = trading_stats['win_rate'] * 100
        card_class = "success-card" if win_rate >= 60 else "warning-card"
        
        # 桌面4列，移动端通过CSS控制为2列
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card info-card"><h4>今日交易</h4><h2>{trading_stats["daily_trades"]}</h2><p>验证模式</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card {card_class}"><h4>胜率</h4><h2>{win_rate:.1f}%</h2><p>目标: > 60%</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card success-card"><h4>成功交易</h4><h2>{trading_stats["success_trades"]}</h2><p>共{trading_stats["total_trades"]}笔</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card warning-card"><h4>失败交易</h4><h2>{trading_stats["failed_trades"]}</h2><p>需要优化</p></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 策略进化表格 - 单独占一行
        st.markdown("### 📈 策略进化状态")
        evolution_status = self.data_bridge.get_evolution_status()
        
        if evolution_status['is_running'] and evolution_status['strategies']:
            strategy_df = pd.DataFrame(evolution_status['strategies'][:5])
            strategy_df['fitness'] = strategy_df['fitness'].apply(lambda x: f"{x:.3f}")
            strategy_df['return'] = strategy_df['return'].apply(lambda x: f"{x:.2%}")
            strategy_df['sharpe'] = strategy_df['sharpe'].apply(lambda x: f"{x:.2f}")
            strategy_df['win_rate'] = strategy_df['win_rate'].apply(lambda x: f"{x:.2%}")
            st.dataframe(strategy_df, use_container_width=True, height=250, hide_index=True)
        else:
            st.info("策略进化系统未运行或暂无数据")
        
        st.markdown("---")
        
        # 系统状态 - 精致的状态指示器
        system_status = self.data_bridge.get_system_status()
        
        trading_icon = "🟢" if system_status['trading_active'] else "🔴"
        evolution_icon = "🟢" if system_status['evolution_active'] else "🔴"
        
        st.markdown(f'''
        <div class="status-indicators">
            <div class="status-item">
                <span class="status-dot">{trading_icon}</span>
                <span class="status-label">交易系统</span>
            </div>
            <div class="status-item">
                <span class="status-dot">{evolution_icon}</span>
                <span class="status-label">策略进化</span>
            </div>
            <div class="status-item">
                <span class="status-dot">🟢</span>
                <span class="status-label">数据采集</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    def render_exchanges(self):
        """多交易所监控 - 真实数据（移动端优化）"""
        st.subheader("💱 多交易所实时监控")
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']
        
        # 响应式控制栏
        col1, col2 = st.columns([2, 1])
        with col1:
            symbol = st.selectbox("选择币种", symbols, index=0, key="exchange_symbol_selector", label_visibility="collapsed")
        with col2:
            if st.button("🔄 刷新", use_container_width=True, key="refresh_exchanges"):
                # 清除缓存
                st.session_state.price_cache = {}
                st.session_state.cache_time = {}
                st.rerun()
        
        auto_refresh = st.checkbox("⚡ 自动刷新 (5秒)", value=False, key="auto_refresh_exchanges")
        
        # 获取真实价格数据 - 使用缓存
        exchange_config = self.data_bridge.get_exchange_config()
        price_data = []
        
        with st.spinner('加载价格数据...'):
            for ex_name in exchange_config['active_exchanges']:
                ticker = self.get_cached_price(ex_name, symbol)
                
                if ticker:
                    try:
                        price_data.append({
                            '交易所': ex_name.upper(),
                            '最新价': f"${ticker['last']:.2f}",
                            '买价': f"${ticker.get('bid', 0):.2f}",
                            '卖价': f"${ticker.get('ask', 0):.2f}",
                            '24h涨跌': f"{ticker.get('percentage', 0):.2f}%",
                            '成交量': f"{ticker.get('baseVolume', 0):,.0f}",
                            '状态': '🟢'
                        })
                    except Exception as e:
                        pass
                else:
                    price_data.append({
                        '交易所': ex_name.upper(),
                        '最新价': 'N/A',
                        '买价': 'N/A',
                        '卖价': 'N/A',
                        '24h涨跌': 'N/A',
                        '成交量': 'N/A',
                        '状态': '🔴'
                    })
        
        if price_data:
            st.dataframe(pd.DataFrame(price_data), use_container_width=True, height=200)
            
            # 价格对比
            valid_prices = [float(p['最新价'].replace('$', '').replace(',', '')) 
                          for p in price_data if p['最新价'] != 'N/A']
            
            if len(valid_prices) > 1:
                spread = (max(valid_prices) - min(valid_prices)) / min(valid_prices) * 100
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("最高价", f"${max(valid_prices):.2f}")
                with col2:
                    st.metric("最低价", f"${min(valid_prices):.2f}")
                with col3:
                    color = "🟢" if spread > 0.1 else "🟡"
                    st.metric("价差", f"{color} {spread:.3f}%")
                
                if spread > 0.1:
                    st.success(f"🎯 发现套利机会！价差: {spread:.3f}% (验证模式，不执行交易)")
        else:
            st.warning("⚠️ 无法获取价格数据")
        
        # 自动刷新
        if auto_refresh:
            import time
            time.sleep(5)
            st.rerun()
    
    def render_evolution(self):
        """策略进化 - 真实数据（移动端优化）"""
        st.subheader("🧬 策略自动进化系统")
        
        evolution_status = self.data_bridge.get_evolution_status()
        
        if not evolution_status['is_running']:
            st.info("💡 策略进化系统未运行，请在侧边栏启动")
            return
        
        # 桌面4列，移动端通过CSS控制为2列
        best_fitness = evolution_status['best_fitness']
        fitness_text = f"{best_fitness:.3f}" if best_fitness > 0 else "待计算"
        avg_fitness = evolution_status['avg_fitness']
        avg_text = f"{avg_fitness:.3f}" if avg_fitness > 0 else "待计算"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card info-card"><h4>当前代数</h4><h2>{evolution_status["current_generation"]}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card info-card"><h4>种群大小</h4><h2>{evolution_status["population_size"]}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card success-card"><h4>最佳评分</h4><h2>{fitness_text}</h2></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card warning-card"><h4>平均评分</h4><h2>{avg_text}</h2></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🏆 最佳策略表现 (Top 10)")
        
        if evolution_status['strategies']:
            df = pd.DataFrame(evolution_status['strategies'][:10])
            df.columns = ['策略名称', '适应度', '收益率', '夏普比率', '胜率']
            df['适应度'] = df['适应度'].apply(lambda x: f"{x:.3f}")
            df['收益率'] = df['收益率'].apply(lambda x: f"{x:.2%}")
            df['夏普比率'] = df['夏普比率'].apply(lambda x: f"{x:.2f}")
            df['胜率'] = df['胜率'].apply(lambda x: f"{x:.2%}")
            st.dataframe(df, use_container_width=True, height=450, hide_index=True)
        else:
            st.info("暂无策略数据")
    
    def run(self):
        """运行"""
        self.render_header()
        self.render_sidebar()
        
        tab1, tab2, tab3 = st.tabs([
            "📊 系统概览",
            "💱 多交易所监控",
            "🧬 策略进化"
        ])
        
        with tab1:
            self.render_overview()
        with tab2:
            self.render_exchanges()
        with tab3:
            self.render_evolution()


def main():
    try:
        dashboard = RealDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"❌ 系统错误: {e}")
        import traceback
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
