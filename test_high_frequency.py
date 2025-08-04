#!/usr/bin/env python3
"""
高频量化交易系统测试脚本
"""

import os
import sys
import logging
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """测试配置"""
    print("🔧 测试配置...")
    
    # 测试环境变量
    required_env_vars = [
        'BINANCE_API_KEY', 'BINANCE_SECRET_KEY',
        'OKX_API_KEY', 'OKX_SECRET_KEY', 'OKX_PASSPHRASE',
        'BITGET_API_KEY', 'BITGET_SECRET_KEY', 'BITGET_PASSPHRASE'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {missing_vars}")
        return False
    else:
        print("✅ 环境变量配置正确")
        return True

def test_exchange_config():
    """测试交易所配置"""
    print("🔗 测试交易所配置...")
    
    try:
        from config.exchange_config import ExchangeConfig
        
        config = ExchangeConfig()
        exchanges = config.get_supported_exchanges()
        print(f"✅ 支持的交易所: {exchanges}")
        
        for exchange in exchanges:
            try:
                exchange_config = config.get_exchange_config(exchange)
                trading_pairs = config.get_trading_pairs(exchange)
                print(f"✅ {exchange}: {len(trading_pairs)} 个交易对")
            except Exception as e:
                print(f"❌ {exchange} 配置错误: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 交易所配置测试失败: {e}")
        return False

def test_strategy():
    """测试策略"""
    print("📈 测试交易策略...")
    
    try:
        from strategies.high_frequency_strategy import HighFrequencyStrategy
        
        strategy = HighFrequencyStrategy()
        print("✅ 高频交易策略加载成功")
        
        # 测试策略参数
        print(f"   最小持仓时间: {strategy.min_holding_time}秒")
        print(f"   最大持仓时间: {strategy.max_holding_time}秒")
        print(f"   最大仓位: {strategy.max_position_size*100}%")
        print(f"   止损: {strategy.stop_loss*100}%")
        print(f"   止盈: {strategy.take_profit*100}%")
        
        return True
    except Exception as e:
        print(f"❌ 策略测试失败: {e}")
        return False

def test_ai_review():
    """测试AI复盘系统"""
    print("🤖 测试AI复盘系统...")
    
    try:
        from ai_modules.daily_review_ai import DailyReviewAI
        
        ai = DailyReviewAI()
        print("✅ AI复盘系统加载成功")
        
        # 测试复盘功能
        test_trades = [
            {
                'timestamp': datetime.now(),
                'exchange': 'binance',
                'pair': 'BTC/USDT',
                'direction': 'LONG',
                'price': 50000,
                'qty': 0.001,
                'pnl': 50,
                'holding_time': 300
            }
        ]
        
        test_market_data = {
            'volatility': 0.02,
            'trend': 'neutral',
            'volume': 1000000
        }
        
        review_result = ai.analyze_daily_performance(test_trades, test_market_data)
        print("✅ AI复盘功能测试成功")
        
        return True
    except Exception as e:
        print(f"❌ AI复盘测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("📦 测试依赖包...")
    
    required_packages = [
        'jesse', 'ccxt', 'pandas', 'numpy', 
        'schedule', 'logging', 'datetime'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {missing_packages}")
        return False
    else:
        print("✅ 所有依赖包已安装")
        return True

def test_directories():
    """测试目录结构"""
    print("📁 测试目录结构...")
    
    required_dirs = [
        'config', 'strategies', 'ai_modules', 
        'data', 'monitoring', 'logs'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ 缺少目录: {missing_dirs}")
        return False
    else:
        print("✅ 目录结构正确")
        return True

def main():
    """主测试函数"""
    print("🧪 高频量化交易系统测试")
    print("=" * 50)
    
    tests = [
        ("依赖包", test_dependencies),
        ("目录结构", test_directories),
        ("配置", test_configuration),
        ("交易所配置", test_exchange_config),
        ("交易策略", test_strategy),
        ("AI复盘", test_ai_review)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以启动")
        print("\n🚀 启动命令:")
        print("  python3 run_high_frequency_trading.py")
        print("  或")
        print("  ./start_high_frequency.sh")
    else:
        print("⚠️ 部分测试失败，请检查配置")
        print("\n💡 建议:")
        print("  1. 检查环境变量配置")
        print("  2. 安装缺失的依赖包")
        print("  3. 检查API密钥是否正确")

if __name__ == "__main__":
    main() 