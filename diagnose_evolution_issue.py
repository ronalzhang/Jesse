#!/usr/bin/env python3
"""
进化系统诊断脚本
诊断为什么进化停在第17代
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def diagnose_evolution():
    """诊断进化系统问题"""
    print("=" * 70)
    print("🔍 进化系统诊断")
    print("=" * 70)
    
    # 1. 检查进化状态文件
    print("\n📋 1. 检查进化状态文件")
    print("-" * 70)
    
    state_file = Path("data/evolution/evolution_state.json")
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        print(f"✅ 状态文件存在")
        print(f"   当前代数: {state.get('current_generation', 0)}")
        print(f"   最佳适应度: {state.get('best_fitness', 0):.4f}")
        print(f"   平均适应度: {state.get('avg_fitness', 0):.4f}")
        
        # 检查进化历史
        history = state.get('evolution_history', [])
        if history:
            print(f"   进化历史记录: {len(history)} 条")
            last_evolution = history[-1]
            last_time = datetime.fromisoformat(last_evolution['timestamp'])
            time_since = datetime.now() - last_time
            print(f"   最后进化时间: {last_time}")
            print(f"   距今: {time_since.total_seconds() / 60:.1f} 分钟")
            
            if time_since.total_seconds() > 3600:  # 超过1小时
                print(f"   ⚠️  警告: 超过1小时未进化！")
    else:
        print(f"❌ 状态文件不存在: {state_file}")
    
    # 2. 检查回测文件
    print("\n📋 2. 检查回测文件")
    print("-" * 70)
    
    backtest_dir = Path("data/backtest")
    if backtest_dir.exists():
        files = list(backtest_dir.glob("*.json"))
        print(f"✅ 回测文件数量: {len(files)}")
        
        # 检查最新文件
        if files:
            latest = max(files, key=lambda x: x.stat().st_mtime)
            mtime = datetime.fromtimestamp(latest.stat().st_mtime)
            time_since = datetime.now() - mtime
            print(f"   最新文件: {latest.name}")
            print(f"   修改时间: {mtime}")
            print(f"   距今: {time_since.total_seconds() / 60:.1f} 分钟")
            
            # 读取最新文件内容
            with open(latest, 'r') as f:
                data = json.load(f)
            print(f"   策略名称: {data.get('strategy_name', 'N/A')}")
            print(f"   收益率: {data.get('total_return', 0):.4f}")
            print(f"   夏普比率: {data.get('sharpe_ratio', 0):.4f}")
            print(f"   胜率: {data.get('win_rate', 0):.2%}")
            print(f"   交易次数: {data.get('total_trades', 0)}")
    else:
        print(f"❌ 回测目录不存在: {backtest_dir}")
    
    # 3. 检查日志文件
    print("\n📋 3. 检查进化系统日志")
    print("-" * 70)
    
    log_file = Path("logs/evolution_optimized.log")
    if log_file.exists():
        print(f"✅ 日志文件存在")
        
        # 读取最后100行
        with open(log_file, 'r') as f:
            lines = f.readlines()[-100:]
        
        # 查找关键信息
        evolution_complete = [l for l in lines if '代进化完成' in l]
        trigger_conditions = [l for l in lines if '触发条件' in l]
        errors = [l for l in lines if 'ERROR' in l or '错误' in l]
        
        print(f"   最近进化完成记录: {len(evolution_complete)} 条")
        if evolution_complete:
            print(f"   最后一次: {evolution_complete[-1].strip()}")
        
        print(f"   触发条件检查记录: {len(trigger_conditions)} 条")
        if trigger_conditions:
            print(f"   最后一次: {trigger_conditions[-1].strip()}")
        
        print(f"   错误记录: {len(errors)} 条")
        if errors:
            print(f"   ⚠️  发现错误:")
            for err in errors[-3:]:
                print(f"      {err.strip()}")
    else:
        print(f"❌ 日志文件不存在: {log_file}")
    
    # 4. 检查交易数据
    print("\n📋 4. 检查交易数据")
    print("-" * 70)
    
    trading_log = Path("logs/trading_error.log")
    if trading_log.exists():
        with open(trading_log, 'r') as f:
            lines = f.readlines()[-200:]
        
        # 统计交易相关日志
        trades = [l for l in lines if '交易' in l or 'trade' in l.lower()]
        market_data = [l for l in lines if '获取了' in l and '数据' in l]
        
        print(f"✅ 交易日志存在")
        print(f"   交易相关记录: {len(trades)} 条")
        print(f"   市场数据采集: {len(market_data)} 条")
        
        if market_data:
            print(f"   最近数据采集: {market_data[-1].strip()}")
    else:
        print(f"⚠️  交易日志不存在: {trading_log}")
    
    # 5. 诊断结论
    print("\n" + "=" * 70)
    print("📊 诊断结论")
    print("=" * 70)
    
    issues = []
    recommendations = []
    
    # 检查进化停滞
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
        history = state.get('evolution_history', [])
        if history:
            last_time = datetime.fromisoformat(history[-1]['timestamp'])
            time_since = datetime.now() - last_time
            if time_since.total_seconds() > 3600:
                issues.append(f"进化已停滞 {time_since.total_seconds() / 3600:.1f} 小时")
                recommendations.append("检查进化系统是否正常运行")
                recommendations.append("查看日志中的错误信息")
                recommendations.append("考虑重启进化系统")
    
    # 检查回测文件
    if backtest_dir.exists():
        files = list(backtest_dir.glob("*.json"))
        if len(files) > 50:
            issues.append(f"回测文件过多 ({len(files)} 个)")
            recommendations.append("考虑清理旧的回测文件")
    
    # 输出结论
    if issues:
        print("\n⚠️  发现的问题:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\n✅ 未发现明显问题")
    
    if recommendations:
        print("\n💡 建议:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    print("\n" + "=" * 70)
    print("🔧 快速修复命令")
    print("=" * 70)
    print("\n# 重启进化系统")
    print("pm2 restart jesse-evolution-optimized")
    print("\n# 查看进化系统日志")
    print("pm2 logs jesse-evolution-optimized --lines 50")
    print("\n# 清理旧的回测文件（保留最新30个）")
    print("cd data/backtest && ls -t *.json | tail -n +31 | xargs rm -f")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        diagnose_evolution()
    except Exception as e:
        print(f"\n❌ 诊断过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
