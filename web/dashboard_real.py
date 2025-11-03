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

# 页面配置
st.set_page_config(
    page_title="Jesse+ 全自动量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    /* 指标卡片 - 现代设计 */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(51, 65, 85, 0.6) 100%);
        padding: 1.75rem;
        border-radius: 14px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        border-color: rgba(148, 163, 184, 0.25);
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
    
    /* 状态颜色 */
    .success-card {
        border-left-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.1) 100%);
    }
    
    .warning-card {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
    }
    
    .danger-card {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
    }
    
    .info-card {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.1) 100%);
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
    
    /* Tab样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.4);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* DataFrames样式 */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.875rem;
        }
        .main-header p {
            font-size: 0.95rem;
        }
        .metric-card {
            padding: 1.25rem;
        }
        .metric-card h2 {
            font-size: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem;
        }
        .main-header h1 {
            font-size: 1.5rem;
        }
        .metric-card {
            padding: 1rem;
        }
        .stButton > button {
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
        }
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
        self.init_exchanges()
    
    def init_exchanges(self):
        """初始化交易所"""
        for name in ['binance', 'bitget']:
            try:
                cls = getattr(ccxt, name)
                self.exchanges[name] = cls({'enableRateLimit': True, 'timeout': 30000})
            except:
                pass
    
    def render_header(self):
        """页面头部"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Jesse+ 全自动量化交易系统</h1>
            <p>多交易所 · 多币种 · 策略自动进化 · AI智能决策</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 验证模式提示
        st.markdown("""
        <div class="verification-mode">
            ⚠️ <strong>验证模式</strong>: 当前使用真实市场数据进行策略验证，不进行真实资金交易。
            需要开启实盘交易时请联系管理员。
        </div>
        """, unsafe_allow_html=True)
        
        # 获取真实系统状态
        system_status = self.data_bridge.get_system_status()
        trading_stats = self.data_bridge.get_trading_stats()
        evolution_status = self.data_bridge.get_evolution_status()
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            status_icon = "🟢" if system_status['system_running'] else "🔴"
            status_text = "运行中" if system_status['system_running'] else "已停止"
            st.metric("系统状态", f"{status_icon} {status_text}")
        
        with col2:
            exchange_config = self.data_bridge.get_exchange_config()
            st.metric("活跃交易所", len(exchange_config['active_exchanges']))
        
        with col3:
            st.metric("监控币种", "4")  # BTC, ETH, SOL, BNB
        
        with col4:
            st.metric("今日交易", trading_stats['daily_trades'])
        
        with col5:
            win_rate = trading_stats['win_rate'] * 100
            st.metric("胜率", f"{win_rate:.1f}%")
        
        with col6:
            evo_icon = "✅" if evolution_status['is_running'] else "❌"
            st.metric("策略进化", f"{evo_icon} 第{evolution_status['current_generation']}代")
    
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
            st.sidebar.metric("最佳适应度", f"{evolution_status['best_fitness']:.3f}")
            
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
        st.sidebar.markdown("### ⚠️ 安全提示")
        st.sidebar.info("当前为验证模式，不使用真实资金交易")
    
    def render_overview(self):
        """系统概览 - 真实数据"""
        st.subheader("📊 系统概览")
        
        trading_stats = self.data_bridge.get_trading_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card info-card"><h4>今日交易</h4><h2>{trading_stats["daily_trades"]}</h2><p>验证模式</p></div>', unsafe_allow_html=True)
        with col2:
            win_rate = trading_stats['win_rate'] * 100
            card_class = "success-card" if win_rate >= 60 else "warning-card"
            st.markdown(f'<div class="metric-card {card_class}"><h4>胜率</h4><h2>{win_rate:.1f}%</h2><p>目标: > 60%</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card success-card"><h4>成功交易</h4><h2>{trading_stats["success_trades"]}</h2><p>共{trading_stats["total_trades"]}笔</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card warning-card"><h4>失败交易</h4><h2>{trading_stats["failed_trades"]}</h2><p>需要优化</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📈 策略进化状态")
            evolution_status = self.data_bridge.get_evolution_status()
            
            if evolution_status['is_running'] and evolution_status['strategies']:
                # 显示真实的策略数据
                strategy_df = pd.DataFrame(evolution_status['strategies'][:5])
                strategy_df['fitness'] = strategy_df['fitness'].apply(lambda x: f"{x:.3f}")
                strategy_df['return'] = strategy_df['return'].apply(lambda x: f"{x:.2%}")
                strategy_df['sharpe'] = strategy_df['sharpe'].apply(lambda x: f"{x:.2f}")
                strategy_df['win_rate'] = strategy_df['win_rate'].apply(lambda x: f"{x:.2%}")
                st.dataframe(strategy_df, use_container_width=True)
            else:
                st.info("策略进化系统未运行或暂无数据")
        
        with col2:
            st.markdown("### 🎯 系统状态")
            system_status = self.data_bridge.get_system_status()
            
            status_data = {
                '组件': ['交易系统', '策略进化', '数据采集'],
                '状态': [
                    '🟢 运行中' if system_status['trading_active'] else '🔴 已停止',
                    '🟢 运行中' if system_status['evolution_active'] else '🔴 已停止',
                    '🟢 正常'
                ]
            }
            st.dataframe(pd.DataFrame(status_data), use_container_width=True, hide_index=True)
    
    def render_exchanges(self):
        """多交易所监控 - 真实数据"""
        st.subheader("💱 多交易所实时监控")
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']
        symbol = st.selectbox("选择币种", symbols, index=0)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 刷新", use_container_width=True):
                st.rerun()
        
        # 获取真实价格数据
        exchange_config = self.data_bridge.get_exchange_config()
        price_data = []
        
        for ex_name in exchange_config['active_exchanges']:
            try:
                if ex_name in self.exchanges:
                    ticker = self.exchanges[ex_name].fetch_ticker(symbol)
                    price_data.append({
                        '交易所': ex_name.upper(),
                        '最新价': f"${ticker['last']:.2f}",
                        '买价': f"${ticker['bid']:.2f}",
                        '卖价': f"${ticker['ask']:.2f}",
                        '24h涨跌': f"{ticker.get('percentage', 0):.2f}%",
                        '成交量': f"{ticker.get('baseVolume', 0):,.0f}",
                        '状态': '🟢 正常'
                    })
            except Exception as e:
                price_data.append({
                    '交易所': ex_name.upper(),
                    '最新价': 'N/A',
                    '买价': 'N/A',
                    '卖价': 'N/A',
                    '24h涨跌': 'N/A',
                    '成交量': 'N/A',
                    '状态': f'🔴 {str(e)[:20]}'
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
    
    def render_evolution(self):
        """策略进化 - 真实数据"""
        st.subheader("🧬 策略自动进化系统")
        
        evolution_status = self.data_bridge.get_evolution_status()
        
        if not evolution_status['is_running']:
            st.info("💡 策略进化系统未运行，请在侧边栏启动")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("当前代数", evolution_status['current_generation'])
        with col2:
            st.metric("种群大小", evolution_status['population_size'])
        with col3:
            st.metric("最佳适应度", f"{evolution_status['best_fitness']:.3f}")
        with col4:
            st.metric("平均适应度", f"{evolution_status['avg_fitness']:.3f}")
        
        st.markdown("### 🏆 最佳策略表现")
        if evolution_status['strategies']:
            df = pd.DataFrame(evolution_status['strategies'][:10])
            df.columns = ['策略名称', '适应度', '收益率', '夏普比率', '胜率']
            df['适应度'] = df['适应度'].apply(lambda x: f"{x:.3f}")
            df['收益率'] = df['收益率'].apply(lambda x: f"{x:.2%}")
            df['夏普比率'] = df['夏普比率'].apply(lambda x: f"{x:.2f}")
            df['胜率'] = df['胜率'].apply(lambda x: f"{x:.2%}")
            st.dataframe(df, use_container_width=True)
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
