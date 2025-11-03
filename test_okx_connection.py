#!/usr/bin/env python3
"""
OKX API连接测试脚本
用于验证OKX API配置是否正确
"""

import ccxt
import json
from pathlib import Path

def test_okx_connection():
    """测试OKX连接"""
    print("=" * 60)
    print("🔍 OKX API连接测试")
    print("=" * 60)
    
    # 读取API配置
    try:
        with open('api_keys.json', 'r') as f:
            config = json.load(f)
            okx_config = config['exchanges']['okx']
        print("✅ 成功读取API配置")
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")
        return False
    
    # 显示配置信息（隐藏敏感信息）
    print("\n📋 配置信息:")
    print(f"  API Key: {okx_config['api_key'][:8]}...{okx_config['api_key'][-4:]}")
    print(f"  Secret: {'*' * 20}")
    print(f"  Passphrase: {'*' * len(okx_config['passphrase'])}")
    print(f"  Sandbox: {okx_config.get('sandbox', False)}")
    
    # 初始化OKX交易所
    try:
        okx = ccxt.okx({
            'apiKey': okx_config['api_key'],
            'secret': okx_config['secret_key'],
            'password': okx_config['passphrase'],
            'enableRateLimit': True,
            'timeout': 30000,
            'options': {
                'defaultType': 'spot',  # 现货交易
            }
        })
        
        if okx_config.get('sandbox', False):
            okx.set_sandbox_mode(True)
            print("⚠️  使用沙盒环境")
        
        print("✅ OKX交易所初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False
    
    # 测试1: 获取服务器时间
    print("\n🔍 测试1: 获取服务器时间")
    try:
        server_time = okx.fetch_time()
        print(f"✅ 服务器时间: {server_time}")
    except Exception as e:
        print(f"❌ 获取服务器时间失败: {e}")
        return False
    
    # 测试2: 获取市场信息
    print("\n🔍 测试2: 获取市场信息")
    try:
        markets = okx.load_markets()
        print(f"✅ 成功加载 {len(markets)} 个交易对")
        print(f"  示例: {list(markets.keys())[:5]}")
    except Exception as e:
        print(f"❌ 获取市场信息失败: {e}")
        return False
    
    # 测试3: 获取账户余额
    print("\n🔍 测试3: 获取账户余额")
    try:
        balance = okx.fetch_balance()
        print("✅ 成功获取账户余额")
        
        # 显示非零余额
        total = balance.get('total', {})
        non_zero = {k: v for k, v in total.items() if v > 0}
        
        if non_zero:
            print("  账户余额:")
            for currency, amount in non_zero.items():
                print(f"    {currency}: {amount}")
        else:
            print("  ⚠️  账户余额为空")
    except Exception as e:
        print(f"❌ 获取账户余额失败: {e}")
        print(f"  错误详情: {type(e).__name__}")
        
        # 检查常见错误
        error_msg = str(e).lower()
        if 'permission' in error_msg or 'unauthorized' in error_msg:
            print("\n💡 可能的原因:")
            print("  1. API权限不足，需要开启'读取'权限")
            print("  2. IP地址未加入白名单")
            print("  3. API密钥已过期或被禁用")
        elif 'invalid' in error_msg:
            print("\n💡 可能的原因:")
            print("  1. API Key、Secret或Passphrase错误")
            print("  2. 配置格式不正确")
        
        return False
    
    # 测试4: 获取BTC/USDT价格
    print("\n🔍 测试4: 获取BTC/USDT价格")
    try:
        ticker = okx.fetch_ticker('BTC/USDT')
        print("✅ 成功获取价格数据")
        print(f"  最新价: ${ticker['last']:,.2f}")
        print(f"  24h涨跌: {ticker.get('percentage', 0):.2f}%")
        print(f"  24h成交量: {ticker.get('baseVolume', 0):,.2f} BTC")
    except Exception as e:
        print(f"❌ 获取价格失败: {e}")
        return False
    
    # 测试5: 获取订单簿
    print("\n🔍 测试5: 获取订单簿")
    try:
        orderbook = okx.fetch_order_book('BTC/USDT', limit=5)
        print("✅ 成功获取订单簿")
        print(f"  最佳买价: ${orderbook['bids'][0][0]:,.2f}")
        print(f"  最佳卖价: ${orderbook['asks'][0][0]:,.2f}")
    except Exception as e:
        print(f"❌ 获取订单簿失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！OKX API配置正确")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        success = test_okx_connection()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
