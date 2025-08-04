#!/usr/bin/env python3
"""
Jesse+ 安装脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """创建必要的目录"""
    directories = [
        'data',
        'models',
        'logs',
        'config',
        'strategies',
        'utils',
        'models/lstm',
        'models/transformer',
        'models/garch',
        'models/rl',
        'models/sentiment'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    return True

def setup_environment():
    """设置环境"""
    print("🔧 设置环境...")
    
    # 检查.env文件
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_file.exists() and env_example.exists():
        print("📝 创建环境配置文件...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        print("✅ 环境配置文件已创建 (.env)")
        print("⚠️  请编辑 .env 文件并填入实际的API密钥和配置")
    elif env_file.exists():
        print("✅ 环境配置文件已存在")
    else:
        print("⚠️  未找到环境配置文件模板")

def check_system_requirements():
    """检查系统要求"""
    print("🔍 检查系统要求...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查必要的系统包
    try:
        import numpy
        import pandas
        print("✅ 基础依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少基础依赖: {e}")
        return False
    
    return True

def main():
    """主安装函数"""
    print("🚀 开始安装Jesse+ AI增强量化交易系统")
    print("=" * 50)
    
    # 检查系统要求
    if not check_system_requirements():
        print("❌ 系统要求检查失败，安装终止")
        sys.exit(1)
    
    # 创建目录
    print("\n📁 创建项目目录...")
    create_directories()
    
    # 安装依赖
    print("\n📦 安装Python依赖...")
    if not install_dependencies():
        print("❌ 依赖安装失败，安装终止")
        sys.exit(1)
    
    # 设置环境
    print("\n🔧 设置环境配置...")
    setup_environment()
    
    print("\n" + "=" * 50)
    print("✅ Jesse+ 安装完成！")
    print("\n📋 下一步操作:")
    print("1. 编辑 .env 文件，填入您的API密钥")
    print("2. 配置数据库连接")
    print("3. 运行: python run_ai_enhanced_jesse.py")
    print("\n📚 更多信息请查看 README.md")

if __name__ == "__main__":
    main() 