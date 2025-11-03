#!/usr/bin/env python3
"""Phase 3 衍生品数据优化测试"""

import sys
sys.path.insert(0, '/home/ubuntu/Jesse+')

from data.market_data_collector import MarketDataCollector

print('🧪 Phase 3 衍生品数据优化测试')
print('=' * 80)

collector = MarketDataCollector()

# 测试不同交易所
test_cases = [
    ('binance', 'BTC/USDT'),
    ('okx', 'BTC/USDT'),
    ('bitget', 'BTC/USDT')
]

for exchange, symbol in test_cases:
    print(f'\n📊 测试 {exchange} - {symbol}')
    print('-' * 80)
    
    derivatives = collector.get_derivatives_data(exchange, symbol)
    
    if not derivatives:
        print(f'⚠️  {exchange} 不支持衍生品数据')
        continue
    
    # 持仓量数据
    if 'open_interest' in derivatives:
        oi = derivatives['open_interest']
        print(f'✅ 持仓量:')
        print(f'  当前: {oi.get("current", 0):,.0f}')
        print(f'  期货合约: {oi.get("futures_symbol", "N/A")}')
    
    # 持仓量指标
    if 'oi_metrics' in derivatives:
        metrics = derivatives['oi_metrics']
        print(f'\n✅ 持仓量指标:')
        print(f'  平均值: {metrics.get("average", 0):,.0f}')
        print(f'  24h变化: {metrics.get("change_24h", 0):.2f}%')
        print(f'  趋势: {metrics.get("trend", "N/A")}')
        print(f'  标准差: {metrics.get("std_24h", 0):,.0f}')
    
    # 资金费率
    if 'funding_rate' in derivatives:
        fr = derivatives['funding_rate']
        print(f'\n✅ 资金费率:')
        print(f'  当前: {fr.get("current", 0):.6f}')
    
    # 资金费率指标
    if 'funding_metrics' in derivatives:
        fm = derivatives['funding_metrics']
        print(f'\n✅ 资金费率指标:')
        print(f'  8h平均: {fm.get("average_8h", 0):.6f}')
        print(f'  24h平均: {fm.get("average_24h", 0):.6f}')
        print(f'  市场情绪: {fm.get("sentiment", "N/A")}')
        print(f'  趋势: {fm.get("trend", "N/A")}')

print('\n' + '=' * 80)
print('✅ Phase 3 测试完成！')
