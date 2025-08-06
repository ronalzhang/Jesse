#!/usr/bin/env python3
"""
Web界面启动脚本
可以选择启动不同的Web界面
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """主函数"""
    print("🚀 Jesse+ Web界面启动器")
    print("=" * 50)
    print("请选择要启动的Web界面：")
    print("1. app.py - 完整的AI增强量化交易系统界面")
    print("2. dashboard.py - 高频量化交易系统仪表板")
    print("3. 退出")
    
    while True:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            print("启动完整的AI增强量化交易系统界面...")
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "web/app.py",
                "--server.port", "8060",
                "--server.address", "0.0.0.0",
                "--server.headless", "true"
            ])
            break
        elif choice == "2":
            print("启动高频量化交易系统仪表板...")
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "web/dashboard.py",
                "--server.port", "8061",
                "--server.address", "0.0.0.0",
                "--server.headless", "true"
            ])
            break
        elif choice == "3":
            print("退出启动器")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main() 