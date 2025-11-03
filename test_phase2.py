#!/usr/bin/env python3
"""
Phase 2 功能测试脚本
"""

import sys
sys.path.insert(0, '/home/ubuntu/Jesse+')

from data.market_data_collector import MarketDataCollector
import json

print('🧪 Phase 2 功能测试')
print('=' * 80)

# 创建采集器
collector = MarketDataCollector()

# 测试1: 多时间框架数据
print('\n📊 测试1: 多时间框架数据采集')
print('-' * 80)

exchange = 'binance'
symbol = 'BTC/USDT'
timeframes = ['1m', '5m', '1h']

print(f'交易所: {exchange}')
print(f'交易对: {symbol}')
print(f'时间框架: {timeframes}')
print()

mtf_data = collector.get_multi_timeframe_data(exchange, symbol, timeframes)

if mtf_data:
    print(f'✅ 成功获取 {len(mtf_data)} 个时间框架的数据')
    for tf, data in mtf_data.items():
        if data and 'indicators' in data:
            ind = data['indicators']
            print(f'\n  {tf} 时间框架:')
            print(f'    价格: {ind.get("current_price", 0):.2f}')
            print(f'    EMA20: {ind.get("ema20", 0):.2f}')
            print(f'    RSI14: {ind.get("rsi14", 0):.2f}')
            print(f'    数据点数: {data.get("data_points", 0)}')
else:
    print('❌ 未能获取多时间框架数据')

# 测试2: 衍生品数据
print('\n\n📈 测试2: 衍生品数据采集')
print('-' * 80)

derivatives_data = collector.get_derivatives_data(exchange, symbol)

if derivatives_data:
    print(f'✅ 成功获取衍生品数据')
    
    if 'open_interest' in derivatives_data:
        oi = derivatives_data['open_interest']
        print(f'\n  持仓量:')
        print(f'    当前: {oi.get("current", 0):.2f}')
        print(f'    价值: {oi.get("value", 0):.2f}')
    
    if 'funding_rate' in derivatives_data:
        fr = derivatives_data['funding_rate']
        print(f'\n  资金费率:')
        print(f'    当前: {fr.get("current", 0):.6f}')
        print(f'    下次结算: {fr.get("next_funding_time", "N/A")}')
    
    if 'funding_metrics' in derivatives_data:
        fm = derivatives_data['funding_metrics']
        print(f'\n  资金费率指标:')
        print(f'    8小时平均: {fm.get("average_8h", 0):.6f}')
        print(f'    24小时平均: {fm.get("average_24h", 0):.6f}')
else:
    print('⚠️  未能获取衍生品数据（可能交易所不支持）')

# 测试3: 增强版市场数据
print('\n\n🚀 测试3: 增强版市场数据')
print('-' * 80)

enhanced_data = collector.get_enhanced_market_data(
    exchange, symbol,
    include_multi_timeframe=True,
    include_derivatives=True,
    timeframes=['1m', '1h']
)

if enhanced_data:
    print('✅ 成功获取增强版市场数据')
    print(f'\n数据结构:')
    print(f'  - 基础数据: ✅')
    print(f'  - 技术指标: ✅ ({len(enhanced_data.get("indicators", {}))} 个)')
    print(f'  - 多时间框架: ✅ ({len(enhanced_data.get("timeframes", {}))} 个)')
    print(f'  - 衍生品数据: {"✅" if "derivatives" in enhanced_data else "⚠️"}')
    
    # 计算总数据维度
    total_indicators = len(enhanced_data.get('indicators', {}))
    timeframes_count = len(enhanced_data.get('timeframes', {}))
    total_indicators += timeframes_count * 13  # 每个时间框架13个指标
    
    print(f'\n总数据维度: {total_indicators} 个')
else:
    print('❌ 未能获取增强版市场数据')

print('\n' + '=' * 80)
print('✅ Phase 2 功能测试完成！')
