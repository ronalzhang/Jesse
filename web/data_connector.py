#!/usr/bin/env python3
"""
实时数据连接器
连接后台AI系统和Web界面，提供实时数据更新
"""

import json
import time
import threading
import queue
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

class RealTimeDataConnector:
    """实时数据连接器"""
    
    def __init__(self):
        """初始化数据连接器"""
        self.data_queue = queue.Queue()
        self.is_running = False
        self.last_update = datetime.now()
        
        # 数据存储
        self.market_data = {}
        self.ai_analysis = {}
        self.trading_signals = []
        self.strategy_evolution = []
        self.system_status = {}
        
        # 启动数据监听线程
        self.start_data_listener()
    
    def start_data_listener(self):
        """启动数据监听线程"""
        self.is_running = True
        self.listener_thread = threading.Thread(target=self._data_listener, daemon=True)
        self.listener_thread.start()
    
    def _data_listener(self):
        """数据监听线程"""
        while self.is_running:
            try:
                # 监听数据文件变化
                self._check_data_files()
                
                # 生成模拟数据（实际环境中从后台系统获取）
                self._generate_mock_data()
                
                time.sleep(1)  # 每秒检查一次
                
            except Exception as e:
                print(f"数据监听错误: {e}")
                time.sleep(5)
    
    def _check_data_files(self):
        """检查数据文件变化"""
        data_dir = Path("data")
        if not data_dir.exists():
            return
        
        # 检查交易信号文件
        signals_dir = data_dir / "signals"
        if signals_dir.exists():
            for signal_file in signals_dir.glob("*.json"):
                if signal_file.stat().st_mtime > self.last_update.timestamp():
                    self._load_signal_data(signal_file)
        
        # 检查性能指标文件
        performance_dir = data_dir / "performance"
        if performance_dir.exists():
            for perf_file in performance_dir.glob("*.json"):
                if perf_file.stat().st_mtime > self.last_update.timestamp():
                    self._load_performance_data(perf_file)
    
    def _load_signal_data(self, signal_file: Path):
        """加载交易信号数据"""
        try:
            with open(signal_file, 'r', encoding='utf-8') as f:
                signal_data = json.load(f)
                self.trading_signals.append(signal_data)
                
                # 保持最近100条记录
                if len(self.trading_signals) > 100:
                    self.trading_signals = self.trading_signals[-100:]
                    
        except Exception as e:
            print(f"加载信号数据错误: {e}")
    
    def _load_performance_data(self, perf_file: Path):
        """加载性能数据"""
        try:
            with open(perf_file, 'r', encoding='utf-8') as f:
                perf_data = json.load(f)
                self.system_status.update(perf_data)
                
        except Exception as e:
            print(f"加载性能数据错误: {e}")
    
    def _generate_mock_data(self):
        """生成模拟数据"""
        current_time = datetime.now()
        
        # 生成市场数据
        self.market_data = {
            "BTC/USDT": {
                "price": 42000 + np.random.normal(0, 200),
                "volume": np.random.randint(1000, 5000),
                "change_24h": np.random.uniform(-5, 5),
                "timestamp": current_time
            }
        }
        
        # 生成多交易所价格数据
        exchanges = ['binance', 'okx', 'bybit', 'gate', 'kucoin', 'mexc']
        base_price = 42000
        
        self.multi_exchange_prices = {}
        for symbol in ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']:
            self.multi_exchange_prices[symbol] = {
                'exchanges': exchanges,
                'last_prices': [base_price + np.random.normal(0, 100) for _ in exchanges],
                'bid_prices': [base_price + np.random.normal(-50, 50) for _ in exchanges],
                'ask_prices': [base_price + np.random.normal(50, 50) for _ in exchanges],
                'volumes': [np.random.randint(1000, 10000) for _ in exchanges],
                'timestamp': current_time
            }
            base_price = 2500 if symbol == 'ETH/USDT' else 300 if symbol == 'BNB/USDT' else base_price
        
        # 生成AI分析数据
        self.ai_analysis = {
            "sentiment": {
                "news": np.random.uniform(0.4, 0.8),
                "social": np.random.uniform(0.5, 0.9),
                "technical": np.random.uniform(0.3, 0.7),
                "overall": np.random.uniform(0.5, 0.8)
            },
            "prediction": {
                "price_1h": 42000 + np.random.normal(0, 100),
                "price_4h": 42000 + np.random.normal(0, 200),
                "price_24h": 42000 + np.random.normal(0, 500),
                "confidence": np.random.uniform(0.6, 0.9)
            },
            "signals": {
                "action": np.random.choice(["buy", "sell", "hold"]),
                "strength": np.random.uniform(0.5, 1.0),
                "confidence": np.random.uniform(0.6, 0.9)
            }
        }
        
        # 生成策略进化数据
        if len(self.strategy_evolution) == 0 or (current_time - self.strategy_evolution[-1]["timestamp"]).seconds > 300:
            self.strategy_evolution.append({
                "generation": len(self.strategy_evolution) + 1,
                "best_fitness": np.random.uniform(0.6, 0.8),
                "avg_fitness": np.random.uniform(0.5, 0.7),
                "improvement": np.random.uniform(0.01, 0.05),
                "timestamp": current_time
            })
        
        # 更新系统状态
        self.system_status = {
            "is_running": True,
            "uptime": str(current_time - datetime(2024, 1, 1)),
            "active_strategies": 5,
            "total_trades": 156,
            "win_rate": np.random.uniform(0.6, 0.8),
            "total_return": np.random.uniform(0.15, 0.25),
            "max_drawdown": np.random.uniform(0.02, 0.08),
            "sharpe_ratio": np.random.uniform(1.0, 2.0)
        }
    
    def get_market_data(self) -> Dict[str, Any]:
        """获取市场数据"""
        return self.market_data
    
    def get_multi_exchange_prices(self, symbol: str = 'BTC/USDT') -> Dict[str, Any]:
        """获取多交易所价格数据"""
        return self.multi_exchange_prices.get(symbol, {})
    
    def get_ai_analysis(self) -> Dict[str, Any]:
        """获取AI分析数据"""
        return self.ai_analysis
    
    def get_trading_signals(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取交易信号"""
        return self.trading_signals[-limit:] if self.trading_signals else []
    
    def get_strategy_evolution(self) -> List[Dict[str, Any]]:
        """获取策略进化数据"""
        return self.strategy_evolution
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return self.system_status
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        return {
            "total_return": self.system_status.get("total_return", 0),
            "win_rate": self.system_status.get("win_rate", 0),
            "max_drawdown": self.system_status.get("max_drawdown", 0),
            "sharpe_ratio": self.system_status.get("sharpe_ratio", 0),
            "total_trades": self.system_status.get("total_trades", 0)
        }
    
    def get_ai_model_status(self) -> Dict[str, Any]:
        """获取AI模型状态"""
        return {
            "LSTM": {
                "status": "running",
                "accuracy": np.random.uniform(0.65, 0.75),
                "prediction_time": np.random.uniform(0.8, 1.5)
            },
            "Transformer": {
                "status": "running",
                "accuracy": np.random.uniform(0.60, 0.70),
                "prediction_time": np.random.uniform(0.5, 1.0)
            },
            "GARCH": {
                "status": "running",
                "accuracy": np.random.uniform(0.55, 0.65),
                "prediction_time": np.random.uniform(0.3, 0.8)
            },
            "Sentiment": {
                "status": "training" if np.random.random() < 0.1 else "running",
                "accuracy": np.random.uniform(0.65, 0.75),
                "prediction_time": np.random.uniform(1.0, 2.0)
            }
        }
    
    def get_decision_process(self) -> Dict[str, Any]:
        """获取决策过程数据"""
        return {
            "current_step": np.random.choice(["signal_generation", "risk_assessment", "position_sizing", "execution_confirmation"]),
            "signal": np.random.choice(["buy", "sell", "hold"]),
            "confidence": np.random.uniform(0.6, 0.9),
            "target_price": 42000 + np.random.normal(0, 200),
            "stop_loss": 42000 - np.random.uniform(100, 500),
            "position_size": np.random.uniform(0.05, 0.15),
            "risk_reward_ratio": np.random.uniform(1.5, 3.0)
        }
    
    def get_evolution_process(self) -> Dict[str, Any]:
        """获取进化过程数据"""
        return {
            "current_generation": len(self.strategy_evolution),
            "best_fitness": self.strategy_evolution[-1]["best_fitness"] if self.strategy_evolution else 0,
            "avg_fitness": self.strategy_evolution[-1]["avg_fitness"] if self.strategy_evolution else 0,
            "improvement": self.strategy_evolution[-1]["improvement"] if self.strategy_evolution else 0,
            "training_progress": np.random.uniform(0.5, 0.9),
            "exploration_rate": np.random.uniform(0.1, 0.2),
            "learning_rate": 0.001
        }
    
    def stop(self):
        """停止数据连接器"""
        self.is_running = False
        if hasattr(self, 'listener_thread'):
            self.listener_thread.join(timeout=5)

# 全局数据连接器实例
data_connector = RealTimeDataConnector()

def get_data_connector() -> RealTimeDataConnector:
    """获取数据连接器实例"""
    return data_connector 