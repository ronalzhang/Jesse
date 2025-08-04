#!/usr/bin/env python3
"""
启动高频量化交易系统Web仪表板
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    required_packages = ['streamlit', 'plotly', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {missing_packages}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True

def create_dashboard_config():
    """创建仪表板配置"""
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.toml"
    config_content = """
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
address = "localhost"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print("✅ Streamlit配置已创建")

def start_dashboard():
    """启动仪表板"""
    print("🚀 启动高频量化交易系统Web仪表板...")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 创建配置
    create_dashboard_config()
    
    # 检查仪表板文件
    dashboard_file = "web/dashboard.py"
    if not os.path.exists(dashboard_file):
        print(f"❌ 仪表板文件不存在: {dashboard_file}")
        return
    
    # 启动Streamlit
    try:
        print("🌐 启动Web服务器...")
        print("📊 仪表板将在浏览器中自动打开")
        print("🔗 访问地址: http://localhost:8501")
        print("⏹️ 按 Ctrl+C 停止服务器")
        print()
        
        # 启动Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            dashboard_file, 
            "--server.port", "8501",
            "--server.address", "localhost"
        ]
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(3)
            webbrowser.open("http://localhost:8501")
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 运行Streamlit
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 高频量化交易系统Web仪表板")
    print("=" * 50)
    print()
    print("📊 功能特点:")
    print("  • 实时交易数据监控")
    print("  • 策略进化路径可视化")
    print("  • AI复盘分析展示")
    print("  • 风险指标监控")
    print("  • 进化里程碑记录")
    print()
    
    # 检查数据目录
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("📁 创建数据目录")
    
    # 启动仪表板
    start_dashboard()

if __name__ == "__main__":
    main() 