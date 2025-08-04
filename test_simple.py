#!/usr/bin/env python3
"""
简化版高频量化交易系统测试
"""

import os
import sys
from datetime import datetime

def test_basic_structure():
    """测试基础结构"""
    print("📁 测试基础结构...")
    
    # 检查必要文件
    required_files = [
        'run_high_frequency_trading.py',
        'env_high_frequency.py',
        'config/exchange_config.py',
        'strategies/high_frequency_strategy.py',
        'ai_modules/daily_review_ai.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    else:
        print("✅ 所有必要文件存在")
        return True

def test_config_content():
    """测试配置内容"""
    print("🔧 测试配置内容...")
    
    try:
        # 测试交易所配置
        sys.path.append('config')
        from exchange_config import ExchangeConfig
        
        config = ExchangeConfig()
        exchanges = config.get_supported_exchanges()
        print(f"✅ 支持的交易所: {exchanges}")
        
        # 检查是否为三个交易所
        if len(exchanges) == 3 and 'binance' in exchanges and 'okx' in exchanges and 'bitget' in exchanges:
            print("✅ 交易所配置正确")
            return True
        else:
            print("❌ 交易所配置不正确")
            return False
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_strategy_structure():
    """测试策略结构"""
    print("📈 测试策略结构...")
    
    try:
        # 检查策略文件内容
        with open('strategies/high_frequency_strategy.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键类和方法
        if 'class HighFrequencyStrategy' in content:
            print("✅ 高频交易策略类存在")
        else:
            print("❌ 高频交易策略类不存在")
            return False
            
        if 'should_long' in content and 'should_short' in content:
            print("✅ 交易信号方法存在")
        else:
            print("❌ 交易信号方法不存在")
            return False
            
        if 'go_long' in content and 'go_short' in content:
            print("✅ 交易执行方法存在")
        else:
            print("❌ 交易执行方法不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 策略结构测试失败: {e}")
        return False

def test_ai_review_structure():
    """测试AI复盘结构"""
    print("🤖 测试AI复盘结构...")
    
    try:
        # 检查AI复盘文件内容
        with open('ai_modules/daily_review_ai.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键类和方法
        if 'class DailyReviewAI' in content:
            print("✅ AI复盘类存在")
        else:
            print("❌ AI复盘类不存在")
            return False
            
        if 'analyze_daily_performance' in content:
            print("✅ 复盘分析方法存在")
        else:
            print("❌ 复盘分析方法不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ AI复盘结构测试失败: {e}")
        return False

def test_environment_config():
    """测试环境配置"""
    print("🌍 测试环境配置...")
    
    try:
        # 检查环境配置文件
        with open('env_high_frequency.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查关键配置项
        required_configs = [
            'BINANCE_API_KEY',
            'OKX_API_KEY', 
            'BITGET_API_KEY',
            'DAILY_TARGET_MIN',
            'DAILY_TARGET_MAX'
        ]
        
        missing_configs = []
        for config in required_configs:
            if config not in content:
                missing_configs.append(config)
        
        if missing_configs:
            print(f"❌ 缺少配置项: {missing_configs}")
            return False
        else:
            print("✅ 环境配置文件完整")
            return True
            
    except Exception as e:
        print(f"❌ 环境配置测试失败: {e}")
        return False

def test_target_configuration():
    """测试目标配置"""
    print("🎯 测试目标配置...")
    
    try:
        with open('env_high_frequency.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查收益目标配置
        if 'DAILY_TARGET_MIN=0.03' in content and 'DAILY_TARGET_MAX=0.30' in content:
            print("✅ 日收益目标配置正确 (3%-30%)")
        else:
            print("❌ 日收益目标配置不正确")
            return False
            
        # 检查持仓时间配置
        if 'MIN_HOLDING_TIME=30' in content and 'MAX_HOLDING_TIME=3600' in content:
            print("✅ 持仓时间配置正确 (30秒-1小时)")
        else:
            print("❌ 持仓时间配置不正确")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 目标配置测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 简化版高频量化交易系统测试")
    print("=" * 50)
    
    tests = [
        ("基础结构", test_basic_structure),
        ("配置内容", test_config_content),
        ("策略结构", test_strategy_structure),
        ("AI复盘结构", test_ai_review_structure),
        ("环境配置", test_environment_config),
        ("目标配置", test_target_configuration)
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
        print("🎉 所有测试通过！系统配置正确")
        print("\n📋 系统特点:")
        print("  🎯 日化收益率目标: 3% - 30%")
        print("  ⏰ 持仓时间: 30秒 - 1小时")
        print("  🔄 高频交易策略")
        print("  🤖 AI每日复盘")
        print("  📊 三个交易所: Binance, OKX, Bitget")
        print("\n🚀 启动命令:")
        print("  python3 run_high_frequency_trading.py")
        print("  或")
        print("  ./start_high_frequency.sh")
        print("\n🌐 服务器部署:")
        print("  ./deploy_server.sh")
    else:
        print("⚠️ 部分测试失败，请检查配置")
        print("\n💡 建议:")
        print("  1. 检查文件结构")
        print("  2. 验证配置文件")
        print("  3. 确认API密钥配置")

if __name__ == "__main__":
    main() 