#!/usr/bin/env python3
"""
高频量化交易主运行脚本
目标：日化收益率3%-30%
特点：短持仓时间，高交易频率，AI每日复盘
"""

import os
import sys
import logging
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.exchange_config import ExchangeConfig
from strategies.high_frequency_strategy import HighFrequencyStrategy
from ai_modules.daily_review_ai import DailyReviewAI
from ai_modules.strategy_evolution_tracker import StrategyEvolutionTracker
from monitoring.system_monitor import SystemMonitor
from data.market_data_collector import MarketDataCollector

class HighFrequencyTradingSystem:
    """
    高频量化交易系统
    """
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("🚀 启动高频量化交易系统...")
        
        # 初始化组件
        self.exchange_config = ExchangeConfig()
        self.daily_review_ai = DailyReviewAI()
        self.evolution_tracker = StrategyEvolutionTracker()
        self.system_monitor = SystemMonitor()
        self.market_data_collector = MarketDataCollector()
        
        # 交易状态
        self.trading_active = False
        self.daily_trades = []
        self.daily_pnl = 0
        self.start_time = datetime.now()
        
        # 配置参数
        self.load_config()
        
    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/high_frequency_trading.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_config(self):
        """加载配置"""
        try:
            # 从环境变量加载配置
            self.config = {
                'exchanges': ['binance', 'okx', 'bitget'],
                'trading_pairs': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT'],
                'timeframes': ['1m', '5m', '15m'],
                'max_position_size': float(os.getenv('MAX_POSITION_SIZE', '0.3')),
                'stop_loss': float(os.getenv('STOP_LOSS_THRESHOLD', '0.05')),
                'take_profit': float(os.getenv('TAKE_PROFIT_THRESHOLD', '0.08')),
                'daily_target_min': float(os.getenv('DAILY_TARGET_MIN', '0.03')),
                'daily_target_max': float(os.getenv('DAILY_TARGET_MAX', '0.30')),
                'min_holding_time': int(os.getenv('MIN_HOLDING_TIME', '30')),
                'max_holding_time': int(os.getenv('MAX_HOLDING_TIME', '3600'))
            }
            
            self.logger.info("✅ 配置加载成功")
            self.logger.info(f"📊 交易对: {self.config['trading_pairs']}")
            self.logger.info(f"⏰ 时间框架: {self.config['timeframes']}")
            self.logger.info(f"🎯 日收益目标: {self.config['daily_target_min']:.1%} - {self.config['daily_target_max']:.1%}")
            
        except Exception as e:
            self.logger.error(f"❌ 配置加载失败: {e}")
            sys.exit(1)
    
    def start_trading(self):
        """开始交易"""
        self.logger.info("🎯 开始高频量化交易...")
        self.trading_active = True
        
        try:
            # 初始化交易所连接
            self._initialize_exchanges()
            
            # 启动市场数据收集
            self._start_market_data_collection()
            
            # 启动交易循环
            self._trading_loop()
            
        except KeyboardInterrupt:
            self.logger.info("⏹️ 收到停止信号，正在安全停止...")
            self.stop_trading()
        except Exception as e:
            self.logger.error(f"❌ 交易系统错误: {e}")
            self.stop_trading()
    
    def _initialize_exchanges(self):
        """初始化交易所连接"""
        self.logger.info("🔗 初始化交易所连接...")
        
        for exchange in self.config['exchanges']:
            try:
                config = self.exchange_config.get_exchange_config(exchange)
                self.logger.info(f"✅ {exchange} 连接成功")
            except Exception as e:
                self.logger.error(f"❌ {exchange} 连接失败: {e}")
    
    def _start_market_data_collection(self):
        """启动市场数据收集"""
        self.logger.info("📊 启动市场数据收集...")
        
        # 这里可以启动多线程数据收集
        # 暂时使用简单的数据收集
        pass
    
    def _trading_loop(self):
        """交易主循环"""
        self.logger.info("🔄 进入交易主循环...")
        
        while self.trading_active:
            try:
                # 检查交易时间
                if not self._is_trading_time():
                    time.sleep(60)
                    continue
                
                # 获取市场数据
                market_data = self._get_market_data()
                
                # 执行交易策略
                self._execute_trading_strategies(market_data)
                
                # 检查风险控制
                self._check_risk_controls()
                
                # 更新系统状态
                self._update_system_status()
                
                # 短暂休眠
                time.sleep(10)  # 10秒检查一次
                
            except Exception as e:
                self.logger.error(f"❌ 交易循环错误: {e}")
                time.sleep(30)
    
    def _is_trading_time(self) -> bool:
        """检查是否为交易时间"""
        now = datetime.now()
        
        # 24小时交易
        return True
    
    def _get_market_data(self) -> Dict:
        """获取市场数据"""
        market_data = {
            'timestamp': datetime.now(),
            'volatility': 0.02,  # 示例波动率
            'trend': 'neutral',
            'volume': 1000000
        }
        
        return market_data
    
    def _execute_trading_strategies(self, market_data: Dict):
        """执行交易策略"""
        for exchange in self.config['exchanges']:
            for pair in self.config['trading_pairs']:
                try:
                    # 创建策略实例
                    strategy = HighFrequencyStrategy()
                    
                    # 检查交易信号
                    if strategy.should_long():
                        self._execute_long_trade(exchange, pair, strategy)
                    elif strategy.should_short():
                        self._execute_short_trade(exchange, pair, strategy)
                    
                except Exception as e:
                    self.logger.error(f"❌ 策略执行错误 {exchange}/{pair}: {e}")
    
    def _execute_long_trade(self, exchange: str, pair: str, strategy):
        """执行做多交易"""
        try:
            # 模拟交易执行
            trade = {
                'timestamp': datetime.now(),
                'exchange': exchange,
                'pair': pair,
                'direction': 'LONG',
                'price': 50000,  # 示例价格
                'qty': 0.001,
                'pnl': 0,
                'holding_time': 0
            }
            
            self.daily_trades.append(trade)
            self.logger.info(f"📈 做多交易: {exchange}/{pair}")
            
        except Exception as e:
            self.logger.error(f"❌ 做多交易失败: {e}")
    
    def _execute_short_trade(self, exchange: str, pair: str, strategy):
        """执行做空交易"""
        try:
            # 模拟交易执行
            trade = {
                'timestamp': datetime.now(),
                'exchange': exchange,
                'pair': pair,
                'direction': 'SHORT',
                'price': 50000,  # 示例价格
                'qty': 0.001,
                'pnl': 0,
                'holding_time': 0
            }
            
            self.daily_trades.append(trade)
            self.logger.info(f"📉 做空交易: {exchange}/{pair}")
            
        except Exception as e:
            self.logger.error(f"❌ 做空交易失败: {e}")
    
    def _check_risk_controls(self):
        """检查风险控制"""
        # 检查日收益目标
        daily_return = self.daily_pnl / 10000  # 假设初始资金10000
        
        if daily_return >= self.config['daily_target_max']:
            self.logger.info(f"🎯 达到高收益目标: {daily_return:.2%}")
            # 可以考虑降低仓位或停止交易
        
        if daily_return <= -0.15:  # 日止损线
            self.logger.warning(f"⚠️ 达到日止损线: {daily_return:.2%}")
            self.stop_trading()
    
    def _update_system_status(self):
        """更新系统状态"""
        # 更新系统监控
        self.system_monitor.update_status({
            'trading_active': self.trading_active,
            'daily_trades': len(self.daily_trades),
            'daily_pnl': self.daily_pnl,
            'uptime': (datetime.now() - self.start_time).total_seconds()
        })
    
    def stop_trading(self):
        """停止交易"""
        self.logger.info("⏹️ 停止交易系统...")
        self.trading_active = False
        
        # 执行每日复盘
        self._perform_daily_review()
        
        self.logger.info("✅ 交易系统已安全停止")
    
    def _perform_daily_review(self):
        """执行每日复盘"""
        self.logger.info("🤖 开始每日AI复盘...")
        
        try:
            # 准备复盘数据
            market_data = self._get_market_data()
            
            # 执行AI复盘分析
            review_result = self.daily_review_ai.analyze_daily_performance(
                self.daily_trades, market_data
            )
            
            # 保存复盘结果
            self._save_daily_review(review_result)
            
            self.logger.info("✅ 每日复盘完成")
            
        except Exception as e:
            self.logger.error(f"❌ 每日复盘失败: {e}")
    
    def _save_daily_review(self, review_result: Dict):
        """保存每日复盘结果"""
        try:
            # 确保目录存在
            os.makedirs('data/reviews', exist_ok=True)
            
            # 保存复盘结果
            filename = f"data/reviews/daily_review_{datetime.now().date().isoformat()}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(review_result, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"📁 复盘结果已保存: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ 保存复盘结果失败: {e}")
    
    def schedule_daily_review(self):
        """安排每日复盘"""
        # 每天23:59执行复盘
        schedule.every().day.at("23:59").do(self._perform_daily_review)
        
        self.logger.info("📅 每日复盘已安排在23:59执行")
    
    def run_scheduler(self):
        """运行调度器"""
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """主函数"""
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data/reviews', exist_ok=True)
    
    # 创建交易系统实例
    trading_system = HighFrequencyTradingSystem()
    
    # 安排每日复盘
    trading_system.schedule_daily_review()
    
    # 启动交易系统
    trading_system.start_trading()

if __name__ == "__main__":
    main() 