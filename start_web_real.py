#!/usr/bin/env python3
"""
Jesse+ 真实数据Web界面启动脚本
连接后端真实数据，状态持久化
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 启动Jesse+ 真实数据Web界面...")
    print("=" * 50)
    print("⚠️  验证模式: 使用真实市场数据，不进行真实资金交易")
    print("=" * 50)
    
    # 检查虚拟环境
    venv_python = Path("jesse_venv/bin/python")
    python_cmd = str(venv_python) if venv_python.exists() else sys.executable
    print(f"✅ Python: {python_cmd}")
    
    # 检查文件
    app_file = Path("web/dashboard_real.py")
    if not app_file.exists():
        print(f"❌ 文件不存在: {app_file}")
        return 1
    
    print(f"✅ 前端文件: {app_file}")
    print("\n🌐 启动Web界面...")
    print("📍 访问地址: http://0.0.0.0:8060")
    print("=" * 50)
    
    try:
        cmd = [
            python_cmd, "-m", "streamlit", "run",
            str(app_file),
            "--server.port=8060",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ]
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n⚠️  停止系统...")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
