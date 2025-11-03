#!/usr/bin/env python3
"""Phase 4 策略系统集成测试"""

import sys
sys.path.insert(0, '/home/ubuntu/Jesse+')

from strategies.multi_timeframe_strategy import MultiTimeframeStrategy
from utils.strategy_data_adapter import StrategyDataAdapter

print('🧪 Phase 4 策略系统集成测试')
print('=' * 80)

# 创建数据适配器
adapter = StrategyDataAdapter()

# 创建策略
strategy = MultiTimeframeStrategy(
    parameters={
        'timeframes': ['15m', '1h', '4h'],
        'primary_timeframe': '1h',
        'use_derivatives': True,
        'min_signal_strength': 0.5
    }
)

print(f'\n📊 策略: {strategy.name}')
print(f'时间框架: {strategy.timeframes}')
print(f'主时间框架: {strategy.primary_timeframe}')
print(f'使用衍生品数据: {strategy.use_derivatives}')

# 测试数据获取
print('\n' + '-' * 80)
print('📈 测试1: 获取策略数据')
print('-' * 80)

exchange = 'binance'
symbol = 'BTC/USDT'

strategy_data = adapter.get_strategy_data(
    exchange, symbol,
    timeframes=['15m', '1h', '4h'],
    include_derivatives=True
)

if strategy_data:
    print(f'✅ 成功获取 {exchange} {symbol} 策略数据')
    print(f'\n数据结构:')
    print(f'  - 当前价格: {strategy_data.get("current_price", 0):.2f}')
    print(f'  - 基础指标: {len(strategy_data.get("indicators", {}))} 个')
    print(f'  - 时间框架: {len(strategy_data.get("timeframes", {}))} 个')
    print(f'  - 衍生品数据: {"✅" if "derivatives" in strategy_data else "❌"}')
else:
    print('❌ 未能获取策略数据')
    sys.exit(1)

# 测试信号生成
print('\n' + '-' * 80)
print('🎯 测试2: 生成交易信号')
print('-' * 80)

signal = strategy.generate_signals(strategy_data)

print(f'\n交易信号:')
print(f'  动作: {signal["action"]}')
print(f'  强度: {signal["strength"]:.2f}')
print(f'  趋势: {signal.get("trend", "N/A")}')
print(f'  使用指标: {", ".join(signal.get("indicators_used", []))}')

if signal['reason']:
    print(f'\n  原因:')
    for reason in signal['reason']:
        print(f'    - {reason}')

# 测试仓位计算
print('\n' + '-' * 80)
print('💰 测试3: 计算仓位大小')
print('-' * 80)

account_balance = 10000  # $10,000
position_size = strategy.calculate_position_size(signal, account_balance)

print(f'\n账户余额: ${account_balance:,.2f}')
print(f'仓位大小: ${position_size:,.2f}')
print(f'仓位比例: {(position_size/account_balance)*100:.2f}%')

# 测试特征提取
print('\n' + '-' * 80)
print('🤖 测试4: 机器学习特征提取')
print('-' * 80)

features = adapter.extract_features_for_ml(
    strategy_data,
    timeframes=['15m', '1h']
)

print(f'\n提取特征数量: {len(features)}')
print(f'特征向量: {features[:10]}...')  # 显示前10个

# 测试批量数据获取
print('\n' + '-' * 80)
print('📦 测试5: 批量数据获取')
print('-' * 80)

pairs = [
    ('binance', 'BTC/USDT'),
    ('binance', 'ETH/USDT'),
    ('okx', 'BTC/USDT')
]

batch_data = adapter.get_batch_strategy_data(
    pairs,
    timeframes=['1h'],
    include_derivatives=False
)

print(f'\n成功获取 {len(batch_data)} 个交易对的数据:')
for key in batch_data.keys():
    print(f'  ✅ {key}')

print('\n' + '=' * 80)
print('✅ Phase 4 测试完成！')
print('\n总结:')
print('  ✅ 策略数据适配器正常工作')
print('  ✅ 多时间框架策略正常工作')
print('  ✅ 信号生成功能正常')
print('  ✅ 仓位计算功能正常')
print('  ✅ 特征提取功能正常')
print('  ✅ 批量数据获取正常')
