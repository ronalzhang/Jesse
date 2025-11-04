"""
套利机会仪表板组件
自动扫描并展示套利机会，无需手动选择
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from pathlib import Path
import sys
import time

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.arbitrage_scanner import ArbitrageScanner
from data.market_data_collector import MarketDataCollector


class ArbitrageDashboard:
    """套利机会仪表板"""
    
    def __init__(self):
        """初始化仪表板"""
        self.collector = MarketDataCollector()
        self.scanner = ArbitrageScanner(self.collector)
        
        # 默认配置
        self.default_symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']
        self.default_exchanges = ['binance', 'bitget']
    
    def render_scanner_config(self):
        """渲染扫描器配置"""
        st.sidebar.markdown("### ⚙️ 扫描配置")
        
        # 最小价差设置
        min_spread = st.sidebar.slider(
            "最小净利润 (%)",
            min_value=0.1,
            max_value=2.0,
            value=0.5,
            step=0.1,
            help="扣除手续费后的最小利润百分比"
        )
        self.scanner.min_spread_percent = min_spread
        
        # 最小成交量设置
        min_volume = st.sidebar.number_input(
            "最小24h成交量 (USD)",
            min_value=10000,
            max_value=10000000,
            value=100000,
            step=10000,
            help="确保有足够的流动性"
        )
        self.scanner.min_volume_24h = min_volume
        
        # 扫描间隔设置
        scan_interval = st.sidebar.slider(
            "扫描间隔 (秒)",
            min_value=10,
            max_value=120,
            value=30,
            step=10,
            help="自动扫描的时间间隔"
        )
        self.scanner.scan_interval = scan_interval
    
    def render_statistics(self):
        """渲染统计信息"""
        stats = self.scanner.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card info-card">
                <h4>总扫描次数</h4>
                <h2>{stats["total_scans"]}</h2>
                <p>自动扫描</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card success-card">
                <h4>发现机会</h4>
                <h2>{stats["opportunities_found"]}</h2>
                <p>套利机会总数</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            avg_opps = stats["avg_opportunities_per_scan"]
            st.markdown(f'''
            <div class="metric-card warning-card">
                <h4>平均机会数</h4>
                <h2>{avg_opps:.2f}</h2>
                <p>每次扫描</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            cache_size = stats["cache_size"]
            st.markdown(f'''
            <div class="metric-card info-card">
                <h4>当前机会</h4>
                <h2>{cache_size}</h2>
                <p>实时可用</p>
            </div>
            ''', unsafe_allow_html=True)
    
    def render_opportunities_table(self, opportunities):
        """渲染套利机会表格"""
        if not opportunities:
            st.info("🔍 暂无套利机会，继续扫描中...")
            return
        
        # 转换为DataFrame
        df = pd.DataFrame([opp.to_dict() for opp in opportunities])
        
        # 格式化显示
        df['buy_price'] = df['buy_price'].apply(lambda x: f"${x:,.2f}")
        df['sell_price'] = df['sell_price'].apply(lambda x: f"${x:,.2f}")
        df['spread_percent'] = df['spread_percent'].apply(lambda x: f"{x:.2f}%")
        df['profit_potential'] = df['profit_potential'].apply(lambda x: f"{x:.2f}%")
        df['volume_24h'] = df['volume_24h'].apply(lambda x: f"${x:,.0f}")
        
        # 置信度图标
        confidence_icons = {
            'high': '🟢',
            'medium': '🟡',
            'low': '🔴'
        }
        df['confidence'] = df['confidence'].apply(lambda x: f"{confidence_icons.get(x, '⚪')} {x.upper()}")
        
        # 重命名列
        df = df.rename(columns={
            'symbol': '交易对',
            'buy_exchange': '买入交易所',
            'sell_exchange': '卖出交易所',
            'buy_price': '买入价',
            'sell_price': '卖出价',
            'spread_percent': '价差',
            'profit_potential': '净利润',
            'volume_24h': '24h成交量',
            'confidence': '置信度'
        })
        
        # 选择显示的列
        display_cols = ['交易对', '买入交易所', '卖出交易所', '买入价', 
                       '卖出价', '价差', '净利润', '24h成交量', '置信度']
        
        st.dataframe(
            df[display_cols],
            use_container_width=True,
            height=400,
            hide_index=True
        )
    
    def render_opportunities_chart(self, opportunities):
        """渲染套利机会图表"""
        if not opportunities:
            return
        
        # 准备数据
        symbols = [opp.symbol for opp in opportunities]
        profits = [opp.profit_potential for opp in opportunities]
        confidences = [opp.confidence for opp in opportunities]
        
        # 颜色映射
        color_map = {
            'high': '#10b981',
            'medium': '#f59e0b',
            'low': '#ef4444'
        }
        colors = [color_map.get(c, '#6b7280') for c in confidences]
        
        # 创建柱状图
        fig = go.Figure(data=[
            go.Bar(
                x=symbols,
                y=profits,
                marker_color=colors,
                text=[f"{p:.2f}%" for p in profits],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>净利润: %{y:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="套利机会净利润分布",
            xaxis_title="交易对",
            yaxis_title="净利润 (%)",
            template="plotly_dark",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_confidence_distribution(self, opportunities):
        """渲染置信度分布"""
        if not opportunities:
            return
        
        # 统计置信度分布
        confidence_counts = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for opp in opportunities:
            confidence_counts[opp.confidence] += 1
        
        # 创建饼图
        fig = go.Figure(data=[
            go.Pie(
                labels=['高置信度', '中等置信度', '低置信度'],
                values=[confidence_counts['high'], 
                       confidence_counts['medium'], 
                       confidence_counts['low']],
                marker=dict(colors=['#10b981', '#f59e0b', '#ef4444']),
                hole=0.4,
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>数量: %{value}<br>占比: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="套利机会置信度分布",
            template="plotly_dark",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_auto_refresh(self):
        """渲染自动刷新控制"""
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col2:
            auto_refresh = st.checkbox("自动刷新", value=True, key="auto_refresh_arb")
        
        with col3:
            if st.button("🔄 立即扫描", key="manual_scan"):
                st.session_state.force_scan = True
                st.rerun()
        
        return auto_refresh
    
    def render_main(self):
        """渲染主界面"""
        st.subheader("🔍 智能套利机会扫描器")
        
        st.markdown("""
        <div class="verification-mode">
            <strong>💡 智能扫描模式</strong><br>
            系统自动扫描所有交易对和交易所，实时发现套利机会，无需手动选择！
        </div>
        """, unsafe_allow_html=True)
        
        # 配置扫描器
        self.render_scanner_config()
        
        # 自动刷新控制
        auto_refresh = self.render_auto_refresh()
        
        # 执行扫描
        with st.spinner('🔍 正在扫描套利机会...'):
            opportunities = self.scanner.continuous_scan(
                symbols=self.default_symbols,
                exchanges=self.default_exchanges
            )
        
        # 显示统计信息
        self.render_statistics()
        
        st.markdown("---")
        
        # 显示机会
        if opportunities:
            # 按置信度筛选
            confidence_filter = st.selectbox(
                "筛选置信度",
                options=['全部', '高置信度', '中等置信度', '低置信度'],
                index=0
            )
            
            if confidence_filter != '全部':
                confidence_map = {
                    '高置信度': 'high',
                    '中等置信度': 'medium',
                    '低置信度': 'low'
                }
                filtered_opps = self.scanner.filter_by_confidence(
                    confidence_map[confidence_filter]
                )
            else:
                filtered_opps = opportunities
            
            # 显示表格
            st.markdown("### 📊 套利机会列表")
            self.render_opportunities_table(filtered_opps)
            
            st.markdown("---")
            
            # 显示图表
            col1, col2 = st.columns(2)
            
            with col1:
                self.render_opportunities_chart(filtered_opps[:10])
            
            with col2:
                self.render_confidence_distribution(opportunities)
        
        # 自动刷新
        if auto_refresh:
            time.sleep(self.scanner.scan_interval)
            st.rerun()


def render_arbitrage_tab():
    """渲染套利标签页（用于集成到主仪表板）"""
    dashboard = ArbitrageDashboard()
    dashboard.render_main()


if __name__ == "__main__":
    # 独立运行测试
    st.set_page_config(
        page_title="智能套利扫描器",
        page_icon="🔍",
        layout="wide"
    )
    
    dashboard = ArbitrageDashboard()
    dashboard.render_main()
