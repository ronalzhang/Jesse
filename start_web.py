#!/usr/bin/env python3
"""
Jesse+ Web界面启动脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def start_web_interface():
    """启动Web界面"""
    try:
        print("🚀 启动Jesse+ Web界面...")
        print("📱 访问地址: http://localhost:8060")
        print("⏹️  按 Ctrl+C 停止服务")
        print("-" * 50)
        
        # 启动Streamlit
        subprocess.run([
            "streamlit", "run", "web/app.py",
            "--server.port", "8060",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Web界面已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请确保已安装streamlit: pip install streamlit")

if __name__ == "__main__":
    start_web_interface() 