#!/usr/bin/env python3
"""
配置管理器测试脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from web.config_manager import ConfigManager

def test_config_manager():
    """测试配置管理器"""
    print("🧪 开始测试配置管理器...")
    
    # 创建配置管理器实例
    config_manager = ConfigManager()
    
    # 测试1: 加载配置
    print("\n1. 测试加载配置...")
    config = config_manager.get_all_config()
    print(f"✅ 配置加载成功，共 {len(config)} 个配置项")
    
    # 测试2: 更新配置
    print("\n2. 测试更新配置...")
    test_key = 'test_config'
    test_value = 'test_value'
    
    success = config_manager.update_config(test_key, test_value)
    if success:
        print(f"✅ 配置更新成功: {test_key} = {test_value}")
    else:
        print("❌ 配置更新失败")
    
    # 测试3: 获取配置
    print("\n3. 测试获取配置...")
    retrieved_value = config_manager.get_config(test_key)
    if retrieved_value == test_value:
        print(f"✅ 配置获取成功: {test_key} = {retrieved_value}")
    else:
        print(f"❌ 配置获取失败: 期望 {test_value}, 实际 {retrieved_value}")
    
    # 测试4: 获取配置历史
    print("\n4. 测试配置历史...")
    history = config_manager.get_config_history(limit=5)
    print(f"✅ 配置历史获取成功，共 {len(history)} 条记录")
    
    # 测试5: 重置配置
    print("\n5. 测试重置配置...")
    success = config_manager.reset_config()
    if success:
        print("✅ 配置重置成功")
    else:
        print("❌ 配置重置失败")
    
    # 测试6: 验证默认配置
    print("\n6. 验证默认配置...")
    config_after_reset = config_manager.get_all_config()
    default_config = config_manager.default_config
    
    if config_after_reset == default_config:
        print("✅ 默认配置验证成功")
    else:
        print("❌ 默认配置验证失败")
    
    print("\n🎉 配置管理器测试完成!")

if __name__ == "__main__":
    test_config_manager() 