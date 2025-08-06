#!/usr/bin/env python3
"""
测试API配置是否正确加载
"""

import json
import sys
from pathlib import Path

def test_api_config():
    """测试API配置"""
    print("🔍 测试API配置...")
    
    # 测试1: 检查api_keys.json文件是否存在
    api_keys_file = Path('api_keys.json')
    if api_keys_file.exists():
        print("✅ api_keys.json 文件存在")
        
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 测试2: 检查配置结构
            if 'exchanges' in config:
                print("✅ 配置结构正确")
                
                exchanges = config['exchanges']
                for exchange_name, exchange_config in exchanges.items():
                    print(f"📊 {exchange_name.upper()}:")
                    
                    # 检查API Key
                    if exchange_config.get('api_key'):
                        print(f"  ✅ API Key: {'*' * 8}{exchange_config['api_key'][-4:]}")
                    else:
                        print(f"  ❌ API Key: 未配置")
                    
                    # 检查Secret Key
                    if exchange_config.get('secret_key'):
                        print(f"  ✅ Secret Key: {'*' * 8}{exchange_config['secret_key'][-4:]}")
                    else:
                        print(f"  ❌ Secret Key: 未配置")
                    
                    # 检查Passphrase（如果有）
                    if exchange_config.get('passphrase'):
                        print(f"  ✅ Passphrase: {'*' * 8}{exchange_config['passphrase'][-4:]}")
                    else:
                        print(f"  ℹ️ Passphrase: 未配置（可选）")
                    
                    print()
            else:
                print("❌ 配置结构错误：缺少 'exchanges' 字段")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON格式错误: {e}")
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
    else:
        print("❌ api_keys.json 文件不存在")
    
    # 测试3: 检查数据库配置
    config_dir = Path('config')
    db_path = config_dir / 'system_config.db'
    
    if db_path.exists():
        print("✅ 数据库配置文件存在")
        
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 检查是否有API配置
            cursor.execute("SELECT config_key, config_value FROM system_config WHERE config_key LIKE '%_api_key%' OR config_key LIKE '%_secret_key%'")
            api_configs = cursor.fetchall()
            
            if api_configs:
                print(f"✅ 数据库中有 {len(api_configs)} 个API配置项")
                for key, value in api_configs:
                    masked_value = '*' * 8 + value[-4:] if value else '未配置'
                    print(f"  📝 {key}: {masked_value}")
            else:
                print("⚠️ 数据库中没有API配置项")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
    else:
        print("⚠️ 数据库配置文件不存在")
    
    print("\n🎯 测试完成！")

if __name__ == "__main__":
    test_api_config() 