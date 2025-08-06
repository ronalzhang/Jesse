#!/usr/bin/env python3
"""
Web界面启动脚本
直接启动完整的AI增强量化交易系统界面
"""

import sys
import os
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
    
    # 设置环境变量
    os.environ["STREAMLIT_SERVER_PORT"] = "8060"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # 直接导入并运行streamlit
    try:
        import streamlit.web.cli as stcli
        sys.argv = [
            "streamlit", "run", "web/app.py",
            "--server.port", "8060",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        stcli.main()
    except ImportError as e:
        print(f"❌ 导入streamlit失败: {e}")
    except KeyboardInterrupt:
        print("\n🛑 用户中断，正在停止...")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main() 