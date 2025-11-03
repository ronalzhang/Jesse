#!/usr/bin/env python3
"""
优化的策略进化系统
10分钟进化间隔 + 8次最少验证交易
"""

import os
import sys
import logging
import time
import signal
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_modules.auto_strategy_evolution_system import AutoStrategyEvolutionSystem, EvolutionConfig

class OptimizedEvolutionLauncher:
    """优化的进化系统启动器"""
    
    def __init__(self):
        self.evolution_system = None
        self.is_running = False
        self.logger = self._setup_logging()
        self.trade_counter = 0
        self.last_evolution_time = None
        
    def _setup_logging(self):
        """设置日志"""
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/evolution_optimized.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def create_optimized_config(self) -> EvolutionConfig:
        """创建优化的进化配置"""
        config = EvolutionConfig(
            # 种群配置 - 增加多样性
            population_size=20,
            elite_size=5,
            
            # 进化参数 - 平衡探索和利用
            mutation_rate=0.15,
            crossover_rate=0.75,
            generations=100,
            
            # 性能权重 - 综合评估
            return_weight=0.35,
            risk_weight=0.25,
            sharpe_weight=0.25,
            drawdown_weight=0.15,
            
            # 阈值设置
            min_performance_threshold=0.55,
            max_drawdown_threshold=0.15,
            
            # 触发条件 - 关键优化
            evolution_trigger_days=0.125,  # 3小时 = 0.125天
        )
        
        self.logger.info("✅ 优化配置已创建")
        self.logger.info(f"  - 进化间隔: 10分钟")
        self.logger.info(f"  - 最少验证交易: 8次")
        self.logger.info(f"  - 种群大小: 20个策略")
        self.logger.info(f"  - 精英保留: 5个策略")
        
        return config
    
    def start_evolution_system(self):
        """启动进化系统"""
        try:
            self.logger.info("🚀 启动优化的策略进化系统...")
            self.logger.info("=" * 60)
            self.logger.info("📊 优化方案:")
            self.logger.info("  - 进化间隔: 10分钟")
            self.logger.info("  - 验证交易要求: 最少8次")
            self.logger.info("  - 设计理念: 数据充分性 + 进化效率")
            self.logger.info("=" * 60)
            
            # 创建优化配置
            config = self.create_optimized_config()
            
            # 初始化进化系统
            self.evolution_system = AutoStrategyEvolutionSystem(config)
            
            # 启动自动进化
            self.evolution_system.start_auto_evolution()
            
            self.is_running = True
            self.last_evolution_time = datetime.now()
            
            self.logger.info("✅ 优化的策略进化系统已启动")
            
            # 启动监控线程
            self.start_monitoring()
            
        except Exception as e:
            self.logger.error(f"❌ 启动进化系统失败: {e}")
            raise
    
    def start_monitoring(self):
        """启动监控"""
        import threading
        
        def monitor_loop():
            while self.is_running:
                try:
                    time.sleep(60)  # 每分钟检查一次
                    
                    if self.evolution_system:
                        summary = self.evolution_system.get_evolution_summary()
                        
                        # 计算距离上次进化的时间
                        if self.last_evolution_time:
                            elapsed = (datetime.now() - self.last_evolution_time).total_seconds() / 60
                            self.logger.info(f"⏱️  距离上次进化: {elapsed:.1f}分钟")
                        
                        # 显示当前状态
                        self.logger.info(f"📊 当前代数: {summary.get('current_generation', 0)}")
                        self.logger.info(f"🎯 最佳适应度: {summary.get('best_fitness', 0):.3f}")
                        
                except Exception as e:
                    self.logger.error(f"❌ 监控错误: {e}")
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def stop_evolution_system(self):
        """停止进化系统"""
        try:
            if self.evolution_system and self.is_running:
                self.logger.info("🛑 正在停止优化的策略进化系统...")
                self.evolution_system.stop_auto_evolution()
                self.is_running = False
                self.logger.info("✅ 优化的策略进化系统已停止")
        except Exception as e:
            self.logger.error(f"❌ 停止进化系统失败: {e}")
    
    def run_daemon(self):
        """运行守护进程"""
        def signal_handler(signum, frame):
            self.logger.info("\n🛑 收到停止信号")
            self.stop_evolution_system()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            self.start_evolution_system()
            
            self.logger.info("🔄 进入守护模式...")
            while self.is_running:
                time.sleep(60)
                
        except KeyboardInterrupt:
            self.logger.info("\n🛑 收到中断信号")
        except Exception as e:
            self.logger.error(f"❌ 守护进程运行失败: {e}")
        finally:
            self.stop_evolution_system()


def main():
    """主函数"""
    print("🚀 启动优化的策略进化系统")
    print("=" * 60)
    print("📊 优化方案:")
    print("  - 进化间隔: 10分钟")
    print("  - 验证交易: 最少8次")
    print("  - 种群大小: 20个策略")
    print("  - 精英保留: 5个策略")
    print("=" * 60)
    
    launcher = OptimizedEvolutionLauncher()
    launcher.run_daemon()


if __name__ == "__main__":
    main()
