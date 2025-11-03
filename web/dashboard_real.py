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
.verification-mode {
    background: #fef3c7;
    color: #92400e;
    padding: 1rem;
    border-radius: 5px;
    border-left: 4px solid #f59e0b;
    margin-bottom: 1rem;
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
