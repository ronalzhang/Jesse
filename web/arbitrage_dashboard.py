
import streamlit as st
import pandas as pd
import time

def render_arbitrage_dashboard():
    """渲染全新的V2套利终端仪表板"""

    # --- 页面配置和样式 ---
    st.set_page_config(layout="wide", page_title="Jesse+ Arbitrage Terminal")
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;700&display=swap');
        body { font-family: 'Geist Mono', monospace; }
        .header-metric { background-color: #1a1a1a; border: 1px solid #333; padding: 0.5rem 1rem; border-radius: 0.5rem; }
        .price-matrix-card { background-color: #111; border: 1px solid #333; border-radius: 0.5rem; padding: 1rem; transition: all 0.3s ease; }
        .price-matrix-card:hover { border-color: #00aaff; }
        .price-value { font-size: 1.5rem; font-weight: 700; }
        .opportunity-highlight { background-color: #00aaff; color: #000; animation: pulse 1.5s infinite; }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 170, 255, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(0, 170, 255, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 170, 255, 0); }
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 模拟数据 (后续将替换为真实数据) ---
    if 'mock_data' not in st.session_state:
        st.session_state.mock_data = {
            'BTC/USDT': {
                'binance': { 'price': 68105.50, 'bid': 68105.40, 'ask': 68105.60 },
                'okx': { 'price': 68102.30, 'bid': 68102.20, 'ask': 68102.40 },
                'bitget': { 'price': 68106.80, 'bid': 68106.70, 'ask': 68106.90 },
            },
            'ETH/USDT': {
                'binance': { 'price': 3405.10, 'bid': 3405.00, 'ask': 3405.20 },
                'okx': { 'price': 3405.50, 'bid': 3405.40, 'ask': 3405.60 },
                'bitget': { 'price': 3404.90, 'bid': 3404.80, 'ask': 3405.00 },
            },
            'SOL/USDT': {
                'binance': { 'price': 165.20, 'bid': 165.18, 'ask': 165.22 },
                'okx': { 'price': 165.25, 'bid': 165.23, 'ask': 165.27 },
                'bitget': { 'price': 165.15, 'bid': 165.13, 'ask': 165.17 },
            },
        }

    # --- 渲染UI ---

    # Header
    header_cols = st.columns([3, 1, 1])
    with header_cols[0]:
        st.markdown('<h1 class="text-2xl font-bold text-cyan-400">Jesse+ Arbitrage Terminal</h1>', unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown('<div class="header-metric">Total Assets: <span class="font-bold text-white">$125,430</span> <span class="text-green-400">(+2.6%)</span></div>', unsafe_allow_html=True)
    with header_cols[2]:
        st.markdown('<div class="header-metric">AI Accuracy: <span class="font-bold text-white">72%</span></div>', unsafe_allow_html=True)

    st.divider()

    # Price Matrix
    matrix_container = st.container()
    footer_container = st.container()

    with matrix_container:
        crypto_pairs = list(st.session_state.mock_data.keys())
        cols = st.columns(len(crypto_pairs))

        for i, pair in enumerate(crypto_pairs):
            with cols[i]:
                st.markdown(f'<div class="price-matrix-card">'
                            f'<h2 class="text-xl font-bold mb-2">{pair}</h2>'
                            f'<div class="space-y-2">', unsafe_allow_html=True)
                
                pair_prices = []
                for ex, data in st.session_state.mock_data[pair].items():
                    pair_prices.append({'name': ex, **data})
                    st.markdown(f'<div class="flex justify-between items-center">
                                    <span class="text-gray-400">{ex.upper()}</span>
                                    <span class="price-value">${data["price"]:.2f}</span>
                                 </div>', unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)

    # Arbitrage Opportunities
    with footer_container:
        st.markdown("""<h3 class="text-lg font-bold mt-4">Arbitrage Opportunities</h3>""", unsafe_allow_html=True)
        placeholder = st.empty()

    # --- 模拟实时更新 ---
    while True:
        # Update mock data
        for pair in st.session_state.mock_data:
            for ex in st.session_state.mock_data[pair]:
                price_data = st.session_state.mock_data[pair][ex]
                change = (time.time() % 2 - 1) * (price_data['price'] * 0.0005)
                price_data['price'] += change
                price_data['bid'] += change
                price_data['ask'] += change
        
        # Rerender opportunities
        with placeholder.container():
            has_opp = False
            for pair, pair_data in st.session_state.mock_data.items():
                prices = []
                for ex, data in pair_data.items():
                    prices.append({'name': ex, **data})
                
                for i in range(len(prices)):
                    for j in range(len(prices)):
                        if i == j: continue
                        buy_ex = prices[i]
                        sell_ex = prices[j]

                        if sell_ex['bid'] > buy_ex['ask']:
                            spread = (sell_ex['bid'] - buy_ex['ask']) / buy_ex['ask']
                            if spread > 0.001:
                                has_opp = True
                                st.markdown(f'<div class="p-3 rounded-lg opportunity-highlight flex justify-between items-center">'
                                            f'<div>'
                                            f'<span class="font-bold">[${pair}] Arbitrage Opportunity! ({(spread * 100):.2f}%)</span>'
                                            f'<span class="text-sm ml-2">Buy on {buy_ex["name"].upper()} at ${buy_ex["ask"]:.2f} -> Sell on {sell_ex["name"].upper()} at ${sell_ex["bid"]:.2f}</span>'
                                            f'</div>'
                                            f'<button class="bg-black text-white px-3 py-1 rounded">Execute</button>'
                                            f'</div>', unsafe_allow_html=True)
            if not has_opp:
                st.info("No significant arbitrage opportunities at the moment.")

        time.sleep(2)

if __name__ == "__main__":
    render_arbitrage_dashboard()
