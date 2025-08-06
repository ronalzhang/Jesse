#!/usr/bin/env python3
"""
Web界面启动脚本
直接启动完整的AI增强量化交易系统界面
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """主函数"""
    print("🚀 启动Jesse+ AI增强量化交易系统界面...")
    print("=" * 50)
    
    # 检查web目录是否存在
    web_dir = Path("web")
    if not web_dir.exists():
        print("❌ web目录不存在")
        return
    
    # 检查app.py是否存在
    app_file = web_dir / "app.py"
    if not app_file.exists():
        print("❌ web/app.py文件不存在")
        return
    
    print("✅ 启动完整的AI增强量化交易系统界面...")
    print("🌐 访问地址: http://0.0.0.0:8060")
    
    # 启动streamlit应用，添加WebSocket和CORS配置
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "web/app.py",
            "--server.port", "8060",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "true",
            "--server.enableXsrfProtection", "false",
            "--browser.gatherUsageStats", "false",
            "--client.showErrorDetails", "true",
            "--runner.magicEnabled", "true"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动失败: {e}")
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在停止...")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main() 