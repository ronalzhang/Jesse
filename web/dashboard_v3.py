#!/usr/bin/env python3
"""
Jesse+ 全自动量化交易系统 V3
专注于：多交易所监控 | 多币种交易 | 策略自动进化
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

# 页面配置
st.set_page_config(
    page_title="Jesse+ 全自动量化交易系统",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS样式
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.metric-card {
    background: #1e1e1e;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin-bottom: 1rem;
}
.success-card { border-left-color: #10b981; }
.warning-card { border-left-color: #f59e0b; }
.danger-card { border-left-color: #ef4444; }
.info-card { border-left-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# 全局状态
if 'system_running' not in st.session_state:
    st.session_state.system_running = False
if 'auto_evolution' not in st.session_state:
    st.session_state.auto_evolution = False
if 'exchanges' not in st.session_state:
    st.session_state.exchanges = ['binance', 'okx', 'bitget']
if 'symbols' not in st.session_state:
    st.session_state.symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']


class Dashboard:
    def __init__(self):
        self.exchange_clients = {}
        self.init_exchanges()
    
    def init_exchanges(self):
        """初始化交易所"""
        for name in ['binance', 'okx', 'bitget']:
            try:
                cls = getattr(ccxt, name)
                self.exchange_clients[name] = cls({'enableRateLimit': True, 'timeout': 30000})
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
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            status = "🟢 运行中" if st.session_state.system_running else "🔴 停止"
            st.metric("系统状态", status)
        with col2:
            st.metric("交易所", len(st.session_state.exchanges))
        with col3:
            st.metric("币种", len(st.session_state.symbols))
        with col4:
            st.metric("活跃策略", "5", delta="+2")
        with col5:
            st.metric("今日收益", "+2.5%", delta="+0.8%")
        with col6:
            evo = "✅ 启用" if st.session_state.auto_evolution else "❌ 禁用"
            st.metric("策略进化", evo)
    
    def render_sidebar(self):
        """侧边栏"""
        st.sidebar.markdown("## 🎛️ 系统控制")
        
        if st.session_state.system_running:
            if st.sidebar.button("🔴 停止系统", use_container_width=True):
                st.session_state.system_running = False
                st.rerun()
        else:
            if st.sidebar.button("🟢 启动系统", use_container_width=True):
                st.session_state.system_running = True
                st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 🧬 策略进化")
        auto_evo = st.sidebar.checkbox("启用自动进化", st.session_state.auto_evolution)
        if auto_evo != st.session_state.auto_evolution:
            st.session_state.auto_evolution = auto_evo
            st.rerun()
        
        if st.session_state.auto_evolution:
            st.sidebar.info("🔄 进化系统运行中")
            st.sidebar.metric("当前代数", "15", delta="+1")
            st.sidebar.metric("最佳适应度", "0.85", delta="+0.05")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 💱 交易所")
        exchanges = st.sidebar.multiselect(
            "选择交易所",
            ['binance', 'okx', 'bitget', 'bybit', 'gate'],
            default=st.session_state.exchanges
        )
        if exchanges != st.session_state.exchanges:
            st.session_state.exchanges = exchanges
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 💰 币种")
        symbols = st.sidebar.multiselect(
            "选择币种",
            ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT'],
            default=st.session_state.symbols
        )
        if symbols != st.session_state.symbols:
            st.session_state.symbols = symbols
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 🛡️ 风险控制")
        st.sidebar.slider("最大仓位(%)", 1, 50, 15)
        st.sidebar.slider("止损(%)", 1, 20, 5)
        st.sidebar.slider("日损失限制(%)", 1, 20, 10)
    
    def render_overview(self):
        """系统概览"""
        st.subheader("📊 系统概览")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card success-card"><h4>总资产</h4><h2>$125,430</h2><p>+$3,240 今日</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card info-card"><h4>今日收益</h4><h2>+2.5%</h2><p>+0.8% 较昨日</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card success-card"><h4>胜率</h4><h2>68%</h2><p>目标: > 60%</p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card warning-card"><h4>最大回撤</h4><h2>8.2%</h2><p>警戒: > 10%</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💼 资产分布")
            data = {'币种': ['BTC', 'ETH', 'BNB', 'SOL', 'USDT'], '价值': [45000, 28000, 15000, 12000, 25430]}
            fig = px.pie(pd.DataFrame(data), values='价值', names='币种', color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 收益曲线")
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
            returns = np.cumsum(np.random.normal(0.001, 0.02, 30))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=returns, mode='lines', name='累计收益', 
                                    line=dict(color='#10b981', width=2), fill='tozeroy'))
            fig.update_layout(title='30天累计收益', xaxis_title='日期', yaxis_title='收益率',
                            template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_exchanges(self):
        """多交易所监控"""
        st.subheader("💱 多交易所监控")
        
        symbol = st.selectbox("选择币种", st.session_state.symbols, index=0)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 刷新", use_container_width=True):
                st.rerun()
        
        price_data = []
        for ex_name in st.session_state.exchanges:
            try:
                if ex_name in self.exchange_clients:
                    ticker = self.exchange_clients[ex_name].fetch_ticker(symbol)
                    price_data.append({
                        '交易所': ex_name.upper(),
                        '最新价': f"${ticker['last']:.2f}",
                        '买价': f"${ticker['bid']:.2f}",
                        '卖价': f"${ticker['ask']:.2f}",
                        '24h涨跌': f"{ticker.get('percentage', 0):.2f}%",
                        '成交量': f"{ticker.get('baseVolume', 0):,.0f}",
                        '状态': '🟢 正常'
                    })
            except:
                price_data.append({
                    '交易所': ex_name.upper(), '最新价': 'N/A', '买价': 'N/A',
                    '卖价': 'N/A', '24h涨跌': 'N/A', '成交量': 'N/A', '状态': '🔴 异常'
                })
        
        if price_data:
            st.dataframe(pd.DataFrame(price_data), use_container_width=True, height=250)
            
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
                    st.metric("价差", f"{spread:.3f}%")
                
                if spread > 0.1:
                    st.success(f"🎯 发现套利机会！价差: {spread:.3f}%")
    
    def render_evolution(self):
        """策略进化"""
        st.subheader("🧬 策略自动进化")
        
        if not st.session_state.auto_evolution:
            st.info("💡 策略进化未启用，请在侧边栏启用")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("当前代数", "15", delta="+1")
        with col2:
            st.metric("种群大小", "20")
        with col3:
            st.metric("最佳适应度", "0.85", delta="+0.05")
        with col4:
            st.metric("平均适应度", "0.72", delta="+0.03")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📈 适应度进化")
            gens = list(range(1, 16))
            best = [0.5 + i * 0.025 + np.random.uniform(-0.02, 0.02) for i in range(15)]
            avg = [0.4 + i * 0.02 + np.random.uniform(-0.02, 0.02) for i in range(15)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=gens, y=best, mode='lines+markers', name='最佳', line=dict(color='#10b981', width=2)))
            fig.add_trace(go.Scatter(x=gens, y=avg, mode='lines+markers', name='平均', line=dict(color='#3b82f6', width=2)))
            fig.update_layout(xaxis_title='代数', yaxis_title='适应度', template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏆 最佳策略")
            data = {
                '策略': ['进化_15', '进化_14', '进化_13', '进化_12', '进化_11'],
                '适应度': [0.85, 0.82, 0.79, 0.76, 0.73],
                '收益率': ['3.2%', '2.8%', '2.5%', '2.3%', '2.1%'],
                '夏普': [1.8, 1.7, 1.6, 1.5, 1.4],
                '胜率': ['68%', '65%', '63%', '62%', '60%']
            }
            st.dataframe(pd.DataFrame(data), use_container_width=True, height=250)
    
    def render_trading(self):
        """交易监控"""
        st.subheader("📈 交易监控")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("今日交易", "45", delta="+12")
        with col2:
            st.metric("成功", "31", delta="+8")
        with col3:
            st.metric("失败", "14", delta="+4")
        with col4:
            st.metric("胜率", "68.9%", delta="+2.1%")
        
        st.markdown("### 📋 最近交易")
        data = {
            '时间': [datetime.now() - timedelta(minutes=i*5) for i in range(10)],
            '交易所': np.random.choice(st.session_state.exchanges, 10),
            '币种': np.random.choice(st.session_state.symbols, 10),
            '方向': np.random.choice(['买入', '卖出'], 10),
            '价格': [f"${42000 + np.random.uniform(-500, 500):.2f}" for _ in range(10)],
            '数量': [f"{np.random.uniform(0.01, 0.5):.4f}" for _ in range(10)],
            '收益': [f"{np.random.uniform(-2, 5):+.2f}%" for _ in range(10)],
            '策略': np.random.choice(['进化_15', 'AI策略', '套利'], 10),
            '状态': np.random.choice(['✅ 成功', '❌ 失败'], 10, p=[0.7, 0.3])
        }
        df = pd.DataFrame(data)
        df['时间'] = df['时间'].dt.strftime('%H:%M:%S')
        st.dataframe(df, use_container_width=True, height=400)
    
    def render_risk(self):
        """风险监控"""
        st.subheader("🛡️ 风险监控")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("夏普比率", "1.8", delta="+0.1")
        with col2:
            st.metric("最大回撤", "8.2%", delta="-0.5%")
        with col3:
            st.metric("波动率", "12.5%", delta="-0.2%")
        with col4:
            st.metric("VaR(95%)", "2.1%", delta="-0.3%")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📊 收益分布")
            returns = np.random.normal(0.001, 0.02, 1000)
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=returns, nbinsx=50, marker_color='#10b981'))
            fig.update_layout(xaxis_title='收益率', yaxis_title='频次', template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📉 回撤分析")
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
            drawdown = -np.abs(np.random.normal(0, 0.03, 30))
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=drawdown, mode='lines', line=dict(color='#ef4444', width=2), fill='tozeroy'))
            fig.update_layout(xaxis_title='日期', yaxis_title='回撤(%)', template="plotly_dark", height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        """运行"""
        self.render_header()
        self.render_sidebar()
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 系统概览", "💱 多交易所", "🧬 策略进化", "📈 交易监控", "🛡️ 风险监控"
        ])
        
        with tab1:
            self.render_overview()
        with tab2:
            self.render_exchanges()
        with tab3:
            self.render_evolution()
        with tab4:
            self.render_trading()
        with tab5:
            self.render_risk()


def main():
    try:
        dashboard = Dashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"❌ 系统错误: {e}")


if __name__ == "__main__":
    main()
