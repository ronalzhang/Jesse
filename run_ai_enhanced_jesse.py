#!/usr/bin/env python3
"""
Jesse+ - AI增强的加密货币量化交易系统
主运行文件
"""

import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv(project_root / ".env", override=True)

# 导入Jesse+核心模块
from jesse_core.jesse_manager import JesseManager
from ai_modules.ai_enhancer import AIEnhancer
from monitoring.system_monitor import SystemMonitor
from utils.logging_manager import setup_logging, get_logger

def setup_logger():
    """设置Jesse+系统日志器"""
    setup_logging()
    return get_logger('jesse_plus')

class JessePlusSystem:
    """Jesse+ 主系统类"""
    
    def __init__(self):
        """初始化Jesse+系统"""
        # 设置日志
        self.logger = setup_logger()
        self.logger.info("🚀 启动Jesse+ AI增强量化交易系统")
        
        # 初始化核心组件
        self.jesse_manager = JesseManager()
        self.ai_enhancer = AIEnhancer()
        self.system_monitor = SystemMonitor()
        
        # 系统状态
        self.is_running = False
        self.start_time = None
        
    def initialize_system(self):
        """初始化系统"""
        try:
            self.logger.info("🔧 初始化系统组件...")
            
            # 初始化Jesse核心
            self.jesse_manager.initialize()
            
            # 初始化AI增强模块
            self.ai_enhancer.initialize()
            
            # 初始化监控系统
            self.system_monitor.initialize()
            
            self.logger.info("✅ 系统初始化完成")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 系统初始化失败: {e}")
            return False
    
    def run_ai_enhanced_trading(self):
        """运行AI增强的交易系统"""
        try:
            self.logger.info("🎯 开始AI增强交易循环")
            self.is_running = True
            self.start_time = time.time()
            
            while self.is_running:
                try:
                    # 1. 收集市场数据
                    market_data = self.jesse_manager.collect_market_data()
                    
                    # 2. AI市场分析
                    ai_analysis = self.ai_enhancer.analyze_market(market_data)
                    
                    # 3. AI策略进化
                    evolved_strategies = self.ai_enhancer.evolve_strategies(
                        market_data, ai_analysis
                    )
                    
                    # 4. 执行交易策略
                    trading_results = self.jesse_manager.execute_strategies(
                        evolved_strategies
                    )
                    
                    # 5. 监控系统性能
                    self.system_monitor.monitor_performance(trading_results)
                    
                    # 6. 检查是否需要停止
                    if self.should_stop():
                        self.logger.info("🛑 收到停止信号，正在关闭系统...")
                        break
                    
                    # 等待下一个循环
                    time.sleep(self.get_interval())
                    
                except Exception as e:
                    self.logger.error(f"⚠️ 交易循环中出现错误: {e}")
                    self.system_monitor.record_error(e)
                    time.sleep(10)  # 错误后等待10秒
                    continue
                    
        except KeyboardInterrupt:
            self.logger.info("🛑 收到键盘中断信号")
        except Exception as e:
            self.logger.error(f"❌ 系统运行错误: {e}")
        finally:
            self.cleanup()
    
    def should_stop(self):
        """检查是否应该停止系统"""
        # 检查停止信号文件
        stop_file = Path("stop_signal.txt")
        if stop_file.exists():
            stop_file.unlink()  # 删除信号文件
            return True
        
        # 检查运行时间（可选）
        if self.start_time and time.time() - self.start_time > 86400:  # 24小时
            self.logger.info("⏰ 达到最大运行时间，停止系统")
            return True
        
        return False
    
    def get_interval(self):
        """获取交易循环间隔"""
        return int(os.getenv("TRADING_INTERVAL", "60"))  # 默认60秒
    
    def cleanup(self):
        """清理系统资源"""
        self.logger.info("🧹 清理系统资源...")
        
        try:
            # 停止Jesse管理器
            self.jesse_manager.cleanup()
            
            # 停止AI增强器
            self.ai_enhancer.cleanup()
            
            # 停止监控系统
            self.system_monitor.cleanup()
            
            self.logger.info("✅ 系统清理完成")
            
        except Exception as e:
            self.logger.error(f"⚠️ 清理过程中出现错误: {e}")
    
    def start_web_interface(self):
        """启动Web界面"""
        try:
            self.logger.info("🌐 启动Web界面...")
            
            # 启动Streamlit Web界面
            import subprocess
            subprocess.run([
                "streamlit", "run", "web/app.py",
                "--server.port", "8060",
                "--server.address", "0.0.0.0"
            ])
            
        except Exception as e:
            self.logger.error(f"❌ Web界面启动失败: {e}")

def main():
    """主函数"""
    # 创建Jesse+系统实例
    jesse_plus = JessePlusSystem()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "web":
            # 启动Web界面
            jesse_plus.start_web_interface()
            return
        elif sys.argv[1] == "test":
            # 运行测试模式
            print("🧪 运行测试模式...")
            return
    
    # 初始化系统
    if not jesse_plus.initialize_system():
        print("❌ 系统初始化失败，退出程序")
        sys.exit(1)
    
    # 运行AI增强交易系统
    jesse_plus.run_ai_enhanced_trading()

if __name__ == "__main__":
    main() 