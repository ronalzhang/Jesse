#!/usr/bin/env python3
"""
高频量化交易系统综合启动脚本
包含交易系统和Web界面
"""

import os
import sys
import subprocess
import threading
import time
import signal
import psutil
from pathlib import Path

class CompleteSystem:
    """完整系统启动器"""
    
    def __init__(self):
        self.trading_process = None
        self.dashboard_process = None
        self.running = True
        
    def check_system_requirements(self):
        """检查系统要求"""
        print("🔍 检查系统要求...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("❌ 需要Python 3.8或更高版本")
            return False
        
        # 检查必要文件
        required_files = [
            "run_high_frequency_trading.py",
            "web/dashboard.py",
            "env_high_frequency.py",
            "config/exchange_config.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ 缺少必要文件: {missing_files}")
            return False
        
        # 检查依赖
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
        
        print("✅ 系统要求检查通过")
        return True
    
    def create_directories(self):
        """创建必要目录"""
        directories = [
            "data",
            "data/charts", 
            "data/reviews",
            "logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print("✅ 目录结构已创建")
    
    def start_trading_system(self):
        """启动交易系统"""
        print("🚀 启动高频交易系统...")
        
        try:
            # 启动交易系统
            self.trading_process = subprocess.Popen([
                sys.executable, "run_high_frequency_trading.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"✅ 交易系统已启动 (PID: {self.trading_process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ 启动交易系统失败: {e}")
            return False
    
    def start_dashboard(self):
        """启动Web仪表板"""
        print("🌐 启动Web仪表板...")
        
        try:
            # 启动Streamlit仪表板
            self.dashboard_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", 
                "web/dashboard.py",
                "--server.port", "8060",
                "--server.address", "0.0.0.0"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print(f"✅ Web仪表板已启动 (PID: {self.dashboard_process.pid})")
            print("🔗 访问地址: http://0.0.0.0:8060")
            return True
            
        except Exception as e:
            print(f"❌ 启动Web仪表板失败: {e}")
            return False
    
    def monitor_processes(self):
        """监控进程状态"""
        while self.running:
            try:
                # 检查交易系统
                if self.trading_process and self.trading_process.poll() is not None:
                    print("⚠️ 交易系统已停止，正在重启...")
                    self.start_trading_system()
                
                # 检查Web仪表板
                if self.dashboard_process and self.dashboard_process.poll() is not None:
                    print("⚠️ Web仪表板已停止，正在重启...")
                    self.start_dashboard()
                
                time.sleep(10)  # 每10秒检查一次
                
            except KeyboardInterrupt:
                self.stop_all()
                break
            except Exception as e:
                print(f"❌ 监控进程出错: {e}")
    
    def stop_all(self):
        """停止所有进程"""
        print("\n⏹️ 正在停止所有进程...")
        self.running = False
        
        # 停止交易系统
        if self.trading_process:
            try:
                self.trading_process.terminate()
                self.trading_process.wait(timeout=10)
                print("✅ 交易系统已停止")
            except:
                self.trading_process.kill()
                print("⚠️ 强制停止交易系统")
        
        # 停止Web仪表板
        if self.dashboard_process:
            try:
                self.dashboard_process.terminate()
                self.dashboard_process.wait(timeout=10)
                print("✅ Web仪表板已停止")
            except:
                self.dashboard_process.kill()
                print("⚠️ 强制停止Web仪表板")
        
        # 清理相关进程
        self.cleanup_processes()
    
    def cleanup_processes(self):
        """清理相关进程"""
        try:
            # 查找并终止相关进程
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'run_high_frequency_trading.py' in cmdline or 'streamlit' in cmdline:
                        proc.terminate()
                        print(f"✅ 清理进程: {proc.info['name']} (PID: {proc.info['pid']})")
                except:
                    pass
        except Exception as e:
            print(f"⚠️ 清理进程时出错: {e}")
    
    def show_status(self):
        """显示系统状态"""
        print("\n" + "=" * 50)
        print("📊 系统状态")
        print("=" * 50)
        
        # 交易系统状态
        if self.trading_process and self.trading_process.poll() is None:
            print("✅ 交易系统: 运行中")
        else:
            print("❌ 交易系统: 已停止")
        
        # Web仪表板状态
        if self.dashboard_process and self.dashboard_process.poll() is None:
            print("✅ Web仪表板: 运行中 (http://localhost:8501)")
        else:
            print("❌ Web仪表板: 已停止")
        
        # 数据文件状态
        data_files = [
            "data/strategy_evolution.json",
            "data/performance_history.json"
        ]
        
        print("\n📁 数据文件状态:")
        for file_path in data_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✅ {file_path} ({size} bytes)")
            else:
                print(f"  ❌ {file_path} (不存在)")
        
        print("\n💡 使用说明:")
        print("  • 访问 http://localhost:8501 查看Web界面")
        print("  • 查看 logs/ 目录获取系统日志")
        print("  • 按 Ctrl+C 停止所有服务")
        print("=" * 50)
    
    def run(self):
        """运行完整系统"""
        print("🚀 高频量化交易系统 - 完整启动")
        print("=" * 50)
        
        # 检查系统要求
        if not self.check_system_requirements():
            return
        
        # 创建目录
        self.create_directories()
        
        # 启动交易系统
        if not self.start_trading_system():
            print("❌ 无法启动交易系统，退出")
            return
        
        # 等待交易系统启动
        time.sleep(5)
        
        # 启动Web仪表板
        if not self.start_dashboard():
            print("❌ 无法启动Web仪表板")
            # 继续运行，只启动交易系统
        
        # 显示状态
        self.show_status()
        
        # 启动监控线程
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # 主循环
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ 收到停止信号")
        finally:
            self.stop_all()
            print("✅ 系统已完全停止")

def main():
    """主函数"""
    system = CompleteSystem()
    system.run()

if __name__ == "__main__":
    main() 