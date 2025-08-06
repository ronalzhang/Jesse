#!/usr/bin/env python3
"""
全自动策略进化系统启动脚本
"""

import os
import sys
import logging
import time
import signal
import threading
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_modules.auto_strategy_evolution_system import AutoStrategyEvolutionSystem, EvolutionConfig

class AutoEvolutionSystemLauncher:
    """全自动策略进化系统启动器"""
    
    def __init__(self):
        self.evolution_system = None
        self.is_running = False
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
                logging.FileHandler('logs/auto_evolution_system.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def check_system_requirements(self) -> bool:
        """检查系统要求"""
        self.logger.info("🔍 检查系统要求...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            self.logger.error("❌ 需要Python 3.8或更高版本")
            return False
        
        # 检查必要目录
        required_dirs = ["data", "data/evolution", "data/backtest", "models", "logs"]
        for directory in required_dirs:
            os.makedirs(directory, exist_ok=True)
        
        # 检查依赖包
        required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn']
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
    
    def create_evolution_config(self) -> EvolutionConfig:
        """创建进化配置"""
        config = EvolutionConfig(
            population_size=50,
            generations=100,
            mutation_rate=0.1,
            crossover_rate=0.8,
            elite_size=5,
            return_weight=0.4,
            risk_weight=0.3,
            sharpe_weight=0.2,
            drawdown_weight=0.1,
            min_performance_threshold=0.6,
            evolution_trigger_days=7,
            max_drawdown_threshold=0.2
        )
        
        self.logger.info("✅ 进化配置已创建")
        return config
    
    def start_evolution_system(self):
        """启动进化系统"""
        try:
            self.logger.info("🚀 启动全自动策略进化系统...")
            
            # 创建配置
            config = self.create_evolution_config()
            
            # 初始化进化系统
            self.evolution_system = AutoStrategyEvolutionSystem(config)
            
            # 启动自动进化
            self.evolution_system.start_auto_evolution()
            
            self.is_running = True
            self.logger.info("✅ 全自动策略进化系统已启动")
            
        except Exception as e:
            self.logger.error(f"❌ 启动进化系统失败: {e}")
            raise
    
    def stop_evolution_system(self):
        """停止进化系统"""
        try:
            if self.evolution_system and self.is_running:
                self.logger.info("🛑 正在停止全自动策略进化系统...")
                self.evolution_system.stop_auto_evolution()
                self.is_running = False
                self.logger.info("✅ 全自动策略进化系统已停止")
        except Exception as e:
            self.logger.error(f"❌ 停止进化系统失败: {e}")
    
    def show_system_status(self):
        """显示系统状态"""
        if not self.evolution_system:
            self.logger.info("📊 系统状态: 未启动")
            return
        
        try:
            summary = self.evolution_system.get_evolution_summary()
            
            self.logger.info("📊 系统状态:")
            self.logger.info(f"  - 当前代数: {summary['current_generation']}")
            self.logger.info(f"  - 最佳适应度: {summary['best_fitness']:.3f}")
            self.logger.info(f"  - 平均适应度: {summary['avg_fitness']:.3f}")
            self.logger.info(f"  - 种群大小: {summary['population_size']}")
            self.logger.info(f"  - 最后进化时间: {summary['last_evolution_date']}")
            
            # 显示顶级策略
            if summary['top_strategies']:
                self.logger.info("🏆 顶级策略:")
                for i, strategy in enumerate(summary['top_strategies'][:3], 1):
                    self.logger.info(f"  {i}. {strategy['name']} (适应度: {strategy['fitness']:.3f})")
            
        except Exception as e:
            self.logger.error(f"❌ 获取系统状态失败: {e}")
    
    def export_evolution_report(self):
        """导出进化报告"""
        if not self.evolution_system:
            self.logger.warning("⚠️ 系统未启动，无法导出报告")
            return
        
        try:
            self.logger.info("📄 正在导出进化报告...")
            report_path = self.evolution_system.export_evolution_report()
            if report_path:
                self.logger.info(f"✅ 进化报告已导出: {report_path}")
            else:
                self.logger.error("❌ 导出进化报告失败")
        except Exception as e:
            self.logger.error(f"❌ 导出进化报告失败: {e}")
    
    def run_interactive_mode(self):
        """运行交互模式"""
        self.logger.info("🎮 进入交互模式")
        self.logger.info("可用命令:")
        self.logger.info("  status - 显示系统状态")
        self.logger.info("  report - 导出进化报告")
        self.logger.info("  stop - 停止系统")
        self.logger.info("  quit - 退出")
        
        while self.is_running:
            try:
                command = input("\n请输入命令: ").strip().lower()
                
                if command == 'status':
                    self.show_system_status()
                elif command == 'report':
                    self.export_evolution_report()
                elif command == 'stop':
                    self.stop_evolution_system()
                    break
                elif command == 'quit':
                    self.stop_evolution_system()
                    break
                elif command == 'help':
                    self.logger.info("可用命令: status, report, stop, quit, help")
                else:
                    self.logger.info("未知命令，输入 'help' 查看可用命令")
                    
            except KeyboardInterrupt:
                self.logger.info("\n🛑 收到中断信号")
                break
            except Exception as e:
                self.logger.error(f"❌ 命令执行失败: {e}")
    
    def run_daemon_mode(self):
        """运行守护进程模式"""
        self.logger.info("👻 进入守护进程模式")
        
        try:
            while self.is_running:
                # 每小时显示一次状态
                if datetime.now().minute == 0:
                    self.show_system_status()
                
                time.sleep(60)  # 每分钟检查一次
                
        except KeyboardInterrupt:
            self.logger.info("\n🛑 收到中断信号")
        except Exception as e:
            self.logger.error(f"❌ 守护进程运行失败: {e}")
        finally:
            self.stop_evolution_system()
    
    def setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            self.logger.info(f"🛑 收到信号 {signum}，正在停止系统...")
            self.stop_evolution_system()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def run(self, mode: str = 'interactive'):
        """运行系统"""
        try:
            # 检查系统要求
            if not self.check_system_requirements():
                return False
            
            # 设置信号处理器
            self.setup_signal_handlers()
            
            # 启动进化系统
            self.start_evolution_system()
            
            # 根据模式运行
            if mode == 'daemon':
                self.run_daemon_mode()
            else:
                self.run_interactive_mode()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 系统运行失败: {e}")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='全自动策略进化系统')
    parser.add_argument('--mode', choices=['interactive', 'daemon'], 
                       default='interactive', help='运行模式')
    parser.add_argument('--config', type=str, help='配置文件路径')
    
    args = parser.parse_args()
    
    # 创建启动器
    launcher = AutoEvolutionSystemLauncher()
    
    # 运行系统
    success = launcher.run(mode=args.mode)
    
    if success:
        print("✅ 系统运行完成")
    else:
        print("❌ 系统运行失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 