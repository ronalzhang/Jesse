#!/usr/bin/env python3
"""
机械翻牌计数器测试脚本
用于验证翻牌效果是否正常工作
"""

import os
import webbrowser
from pathlib import Path

def test_flip_counter():
    """测试翻牌计数器"""
    print("🎰 机械翻牌计数器测试")
    print("=" * 50)
    
    # 检查文件是否存在
    files_to_check = [
        'web/static/flip_counter.css',
        'web/static/flip_counter.js',
        'web/flip_counter_demo.html',
        'web/styles.py',
        'FLIP_COUNTER_GUIDE.md'
    ]
    
    print("\n📁 检查文件...")
    all_exist = True
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n❌ 部分文件缺失，请检查安装")
        return False
    
    print("\n✅ 所有文件检查通过")
    
    # 打开演示页面
    demo_path = Path('web/flip_counter_demo.html').absolute()
    demo_url = f'file://{demo_path}'
    
    print(f"\n🌐 打开演示页面...")
    print(f"📍 路径: {demo_url}")
    
    try:
        webbrowser.open(demo_url)
        print("\n✅ 演示页面已在浏览器中打开")
        print("\n💡 使用说明:")
        print("   1. 观察数字变化时的翻牌效果")
        print("   2. 点击按钮测试手动更新")
        print("   3. 查看自动更新的实时模拟")
        print("   4. 注意只有变化的数字位会翻转")
        print("\n📖 详细文档: FLIP_COUNTER_GUIDE.md")
        return True
    except Exception as e:
        print(f"\n❌ 打开浏览器失败: {e}")
        print(f"💡 请手动打开: {demo_url}")
        return False

def show_integration_example():
    """显示集成示例"""
    print("\n" + "=" * 50)
    print("📝 Streamlit集成示例")
    print("=" * 50)
    
    example_code = '''
# 在 web/app.py 中使用翻牌效果

# 1. 基础用法
self.render_metric_card(
    "AI预测准确率",
    68.5,  # 数字值
    "+2.1% 较昨日",
    "success",
    "目标: > 70%",
    use_flip=True,  # 启用翻牌效果
    flip_config={
        'decimals': 1,      # 小数位数
        'suffix': '%',      # 后缀
        'size': 'xlarge'    # 大小
    }
)

# 2. 货币格式
self.render_metric_card(
    "总资产",
    125430,
    "+$3,240 今日",
    "info",
    "+2.6% 增长",
    use_flip=True,
    flip_config={
        'decimals': 0,
        'prefix': '$',      # 前缀
        'separator': ',',   # 千位分隔符
        'size': 'xlarge'
    }
)

# 3. 整数计数
self.render_metric_card(
    "交易次数",
    15,
    "+3 今日新增",
    "info",
    "高频交易模式",
    use_flip=True,
    flip_config={
        'decimals': 0,
        'size': 'xlarge'
    }
)
'''
    
    print(example_code)
    print("\n💡 提示:")
    print("   - 只在关键指标上使用翻牌效果")
    print("   - 避免同时更新过多计数器")
    print("   - 选择合适的更新频率（建议2-5秒）")

def main():
    """主函数"""
    print("\n" + "🎰" * 25)
    print("   机械翻牌计数器 - 测试与演示")
    print("🎰" * 25 + "\n")
    
    # 测试翻牌计数器
    success = test_flip_counter()
    
    # 显示集成示例
    show_integration_example()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 测试完成！翻牌效果已准备就绪")
    else:
        print("⚠️ 测试完成，但存在一些问题")
    print("=" * 50 + "\n")
    
    print("📚 相关文档:")
    print("   - FLIP_COUNTER_GUIDE.md - 完整使用指南")
    print("   - WEB_UI_OPTIMIZATION_SUMMARY.md - UI优化总结")
    print("   - web/flip_counter_demo.html - 在线演示")
    print("\n🚀 现在可以启动 Streamlit 应用查看效果！")
    print("   命令: streamlit run web/app.py\n")

if __name__ == "__main__":
    main()
