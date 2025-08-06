#!/usr/bin/env python3
"""
完整全自动策略进化系统启动脚本
整合交易系统、Web界面和自动进化功能
"""

import os
import sys
import subprocess
import threading
import time
import signal
import psutil
from pathlib import Path
import logging
from datetime import datetime

class CompleteAutoEvolutionSystem:
    """完整全自动策略进化系统"""
    
    def __init__(self):
        self.trading_process = None
        self.web_process = None
        self.evolution_process = None
        self.running = True
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        # 创建日志目录
        os.makedirs("logs", exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/complete_system.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def check_system_requirements(self):
        """检查系统要求"""
        self.logger.info("🔍 检查系统要求...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            self.logger.error("❌ 需要Python 3.8或更高版本")
            return False
        
        # 检查必要文件
        required_files = [
            "start_auto_evolution_system.py",
            "web/app.py",
            "ai_modules/auto_strategy_evolution_system.py",
            "ai_modules/strategy_backtest_engine.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            self.logger.error(f"❌ 缺少必要文件: {missing_files}")
            return False
        
        # 检查依赖
        required_packages = ['streamlit', 'plotly', 'pandas', 'numpy', 'matplotlib', 'seaborn']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.logger.error(f"❌ 缺少依赖包: {missing_packages}")
            self.logger.info("请运行: pip install -r requirements.txt")
            return False
        
        self.logger.info("✅ 系统要求检查通过")
        return True
    
    def create_directories(self):
        """创建必要目录"""
        directories = [
            "data",
            "data/evolution", 
            "data/backtest",
            "data/charts",
            "data/reviews",
            "models",
            "models/evolution",
            "logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        self.logger.info("✅ 目录结构已创建")
    
    def start_auto_evolution_system(self):
        """启动全自动策略进化系统"""
        self.logger.info("🧬 启动全自动策略进化系统...")
        
        try:
            # 启动进化系统
            self.evolution_process = subprocess.Popen([
                sys.executable, "start_auto_evolution_system.py", "--mode", "daemon"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.logger.info(f"✅ 全自动策略进化系统已启动 (PID: {self.evolution_process.pid})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 启动全自动策略进化系统失败: {e}")
            return False
    
    def start_web_interface(self):
        """启动Web界面"""
        self.logger.info("🌐 启动Web界面...")
        
        try:
            # 启动Web界面
            self.web_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "web/app.py",
                "--server.port", "8060",
                "--server.headless", "true"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.logger.info(f"✅ Web界面已启动 (PID: {self.web_process.pid})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 启动Web界面失败: {e}")
            return False
    
    def start_trading_system(self):
        """启动交易系统"""
        self.logger.info("🚀 启动交易系统...")
        
        try:
            # 启动交易系统
            self.trading_process = subprocess.Popen([
                sys.executable, "run_high_frequency_trading.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.logger.info(f"✅ 交易系统已启动 (PID: {self.trading_process.pid})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 启动交易系统失败: {e}")
            return False
    
    def monitor_processes(self):
        """监控进程"""
        while self.running:
            try:
                # 检查进化系统进程
                if self.evolution_process and self.evolution_process.poll() is not None:
                    self.logger.warning("⚠️ 全自动策略进化系统进程已停止，正在重启...")
                    self.start_auto_evolution_system()
                
                # 检查Web界面进程
                if self.web_process and self.web_process.poll() is not None:
                    self.logger.warning("⚠️ Web界面进程已停止，正在重启...")
                    self.start_web_interface()
                
                # 检查交易系统进程
                if self.trading_process and self.trading_process.poll() is not None:
                    self.logger.warning("⚠️ 交易系统进程已停止，正在重启...")
                    self.start_trading_system()
                
                time.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                self.logger.error(f"❌ 进程监控错误: {e}")
                time.sleep(60)
    
    def stop_all(self):
        """停止所有进程"""
        self.logger.info("🛑 正在停止所有进程...")
        self.running = False
        
        # 停止进化系统
        if self.evolution_process:
            try:
                self.evolution_process.terminate()
                self.evolution_process.wait(timeout=10)
                self.logger.info("✅ 全自动策略进化系统已停止")
            except subprocess.TimeoutExpired:
                self.evolution_process.kill()
                self.logger.warning("⚠️ 强制停止全自动策略进化系统")
            except Exception as e:
                self.logger.error(f"❌ 停止全自动策略进化系统失败: {e}")
        
        # 停止Web界面
        if self.web_process:
            try:
                self.web_process.terminate()
                self.web_process.wait(timeout=10)
                self.logger.info("✅ Web界面已停止")
            except subprocess.TimeoutExpired:
                self.web_process.kill()
                self.logger.warning("⚠️ 强制停止Web界面")
            except Exception as e:
                self.logger.error(f"❌ 停止Web界面失败: {e}")
        
        # 停止交易系统
        if self.trading_process:
            try:
                self.trading_process.terminate()
                self.trading_process.wait(timeout=10)
                self.logger.info("✅ 交易系统已停止")
            except subprocess.TimeoutExpired:
                self.trading_process.kill()
                self.logger.warning("⚠️ 强制停止交易系统")
            except Exception as e:
                self.logger.error(f"❌ 停止交易系统失败: {e}")
    
    def cleanup_processes(self):
        """清理进程"""
        try:
            # 查找并清理相关进程
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if any(keyword in cmdline for keyword in ['streamlit', 'auto_evolution', 'high_frequency']):
                        if proc.pid != os.getpid():
                            proc.terminate()
                            self.logger.info(f"✅ 清理进程: {proc.info['name']} (PID: {proc.pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            self.logger.error(f"❌ 清理进程失败: {e}")
    
    def show_status(self):
        """显示系统状态"""
        self.logger.info("📊 系统状态:")
        
        # 进化系统状态
        if self.evolution_process:
            status = "运行中" if self.evolution_process.poll() is None else "已停止"
            self.logger.info(f"  - 全自动策略进化系统: {status} (PID: {self.evolution_process.pid})")
        else:
            self.logger.info("  - 全自动策略进化系统: 未启动")
        
        # Web界面状态
        if self.web_process:
            status = "运行中" if self.web_process.poll() is None else "已停止"
            self.logger.info(f"  - Web界面: {status} (PID: {self.web_process.pid})")
        else:
            self.logger.info("  - Web界面: 未启动")
        
        # 交易系统状态
        if self.trading_process:
            status = "运行中" if self.trading_process.poll() is None else "已停止"
            self.logger.info(f"  - 交易系统: {status} (PID: {self.trading_process.pid})")
        else:
            self.logger.info("  - 交易系统: 未启动")
    
    def run(self):
        """运行完整系统"""
        try:
            self.logger.info("🚀 启动完整全自动策略进化系统...")
            
            # 检查系统要求
            if not self.check_system_requirements():
                return False
            
            # 创建目录
            self.create_directories()
            
            # 清理现有进程
            self.cleanup_processes()
            
            # 启动各个组件
            success = True
            
            # 启动全自动策略进化系统
            if not self.start_auto_evolution_system():
                success = False
            
            # 启动Web界面
            if not self.start_web_interface():
                success = False
            
            # 启动交易系统
            if not self.start_trading_system():
                success = False
            
            if not success:
                self.logger.error("❌ 部分组件启动失败")
                return False
            
            self.logger.info("✅ 完整全自动策略进化系统启动成功")
            self.logger.info("🌐 Web界面地址: http://localhost:8060")
            self.logger.info("📊 系统监控: 每30秒检查一次进程状态")
            
            # 显示初始状态
            self.show_status()
            
            # 启动监控线程
            monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            monitor_thread.start()
            
            # 主循环
            try:
                while self.running:
                    time.sleep(60)  # 每分钟检查一次
                    
                    # 显示状态（每小时一次）
                    if datetime.now().minute == 0:
                        self.show_status()
                        
            except KeyboardInterrupt:
                self.logger.info("🛑 收到中断信号")
            except Exception as e:
                self.logger.error(f"❌ 主循环错误: {e}")
            finally:
                self.stop_all()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 系统运行失败: {e}")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='完整全自动策略进化系统')
    parser.add_argument('--cleanup', action='store_true', help='清理现有进程')
    parser.add_argument('--status', action='store_true', help='显示系统状态')
    
    args = parser.parse_args()
    
    # 创建系统实例
    system = CompleteAutoEvolutionSystem()
    
    if args.cleanup:
        system.cleanup_processes()
        print("✅ 进程清理完成")
        return
    
    if args.status:
        system.show_status()
        return
    
    # 运行完整系统
    success = system.run()
    
    if success:
        print("✅ 完整全自动策略进化系统运行完成")
    else:
        print("❌ 完整全自动策略进化系统运行失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 