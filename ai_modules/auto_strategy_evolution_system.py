"""
全自动策略进化系统
实现真正的AI驱动策略自动进化
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import threading
import time
from dataclasses import dataclass, asdict
import pickle
import hashlib

# 导入现有组件
from .strategy_evolution_tracker import StrategyEvolutionTracker
from .strategy_evolver import StrategyEvolver
from .ai_enhancer import AIEnhancer
from .daily_review_ai import DailyReviewAI
from .strategy_backtest_engine import StrategyBacktestEngine, BacktestResult

@dataclass
class EvolutionConfig:
    """进化配置"""
    # 进化参数
    population_size: int = 50
    generations: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_size: int = 5
    
    # 性能指标权重
    return_weight: float = 0.4
    risk_weight: float = 0.3
    sharpe_weight: float = 0.2
    drawdown_weight: float = 0.1
    
    # 进化触发条件
    min_performance_threshold: float = 0.6
    evolution_trigger_days: int = 7
    max_drawdown_threshold: float = 0.2
    
    # 策略参数范围
    param_ranges: Dict[str, Tuple[float, float]] = None
    
    def __post_init__(self):
        if self.param_ranges is None:
            self.param_ranges = {
                'position_size': (0.01, 0.5),
                'stop_loss': (0.01, 0.1),
                'take_profit': (0.02, 0.3),
                'rsi_period': (10, 30),
                'ma_short': (5, 20),
                'ma_long': (20, 100),
                'bollinger_period': (10, 30),
                'bollinger_std': (1.5, 3.0)
            }

class AutoStrategyEvolutionSystem:
    """
    全自动策略进化系统
    实现真正的AI驱动策略自动进化
    """
    
    def __init__(self, config: EvolutionConfig = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or EvolutionConfig()
        
        # 初始化组件
        self.evolution_tracker = StrategyEvolutionTracker()
        self.strategy_evolver = StrategyEvolver()
        self.ai_enhancer = AIEnhancer()
        self.daily_review_ai = DailyReviewAI()
        self.backtest_engine = StrategyBacktestEngine()
        
        # 进化状态
        self.evolution_state = {
            'current_generation': 0,
            'best_fitness': 0.0,
            'avg_fitness': 0.0,
            'evolution_history': [],
            'active_strategies': [],
            'performance_metrics': {},
            'last_evolution_date': None
        }
        
        # 数据存储
        self.data_dir = "data/evolution"
        self.models_dir = "models/evolution"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        # 自动进化线程
        self.evolution_thread = None
        self.is_running = False
        
        # 市场数据缓存
        self.market_data_cache = None
        self.last_market_data_update = None
        
        # 初始化系统
        self._initialize_system()
    
    def _initialize_system(self):
        """初始化系统"""
        try:
            self.logger.info("🔧 初始化全自动策略进化系统...")
            
            # 初始化AI组件
            try:
                self.ai_enhancer.initialize()
                self.strategy_evolver.initialize()
            except Exception as e:
                self.logger.warning(f"⚠️ AI组件初始化失败: {e}")
            
            # 加载现有进化数据
            self._load_evolution_state()
            
            # 初始化策略种群
            self._initialize_strategy_population()
            
            # 初始化性能指标
            if not self.evolution_state['performance_metrics']:
                self.evolution_state['performance_metrics'] = {
                    'avg_return': 0.0,
                    'avg_sharpe': 0.0,
                    'max_drawdown': 0.0,
                    'avg_win_rate': 0.0,
                    'avg_profit_factor': 0.0
                }
            
            self.logger.info("✅ 全自动策略进化系统初始化完成")
            
        except Exception as e:
            self.logger.error(f"❌ 系统初始化失败: {e}")
            raise
    
    def _load_evolution_state(self):
        """加载进化状态"""
        state_file = os.path.join(self.data_dir, "evolution_state.json")
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    self.evolution_state.update(json.load(f))
                self.logger.info("✅ 进化状态已加载")
            except Exception as e:
                self.logger.warning(f"⚠️ 加载进化状态失败: {e}")
    
    def _save_evolution_state(self):
        """保存进化状态"""
        try:
            state_file = os.path.join(self.data_dir, "evolution_state.json")
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.evolution_state, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"❌ 保存进化状态失败: {e}")
    
    def _initialize_strategy_population(self):
        """初始化策略种群"""
        if not self.evolution_state['active_strategies']:
            self.logger.info("🧬 初始化策略种群...")
            
            # 生成初始策略种群
            strategies = []
            for i in range(self.config.population_size):
                strategy = self._generate_random_strategy(f"strategy_{i}")
                strategies.append(strategy)
            
            self.evolution_state['active_strategies'] = strategies
            self.logger.info(f"✅ 策略种群初始化完成，共 {len(strategies)} 个策略")
        else:
            self.logger.info(f"✅ 策略种群已存在，共 {len(self.evolution_state['active_strategies'])} 个策略")
    
    def _generate_random_strategy(self, name: str) -> Dict[str, Any]:
        """生成随机策略"""
        try:
            strategy = {
                'id': hashlib.md5(f"{name}_{datetime.now().isoformat()}".encode()).hexdigest()[:8],
                'name': name,
                'type': np.random.choice(['trend_following', 'mean_reversion', 'arbitrage', 'grid_trading']),
                'parameters': {},
                'performance': {
                    'total_return': 0.0,
                    'sharpe_ratio': 0.0,
                    'max_drawdown': 0.0,
                    'win_rate': 0.0,
                    'profit_factor': 0.0
                },
                'fitness': 0.0,
                'generation': 0,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            
            # 生成随机参数
            for param_name, (min_val, max_val) in self.config.param_ranges.items():
                strategy['parameters'][param_name] = np.random.uniform(min_val, max_val)
            
            return strategy
            
        except Exception as e:
            self.logger.error(f"❌ 生成随机策略失败: {e}")
            # 返回默认策略
            return {
                'id': hashlib.md5(f"{name}_default".encode()).hexdigest()[:8],
                'name': name,
                'type': 'trend_following',
                'parameters': {
                    'position_size': 0.1,
                    'stop_loss': 0.05,
                    'take_profit': 0.1,
                    'rsi_period': 14,
                    'ma_short': 10,
                    'ma_long': 20,
                    'bollinger_period': 20,
                    'bollinger_std': 2.0
                },
                'performance': {
                    'total_return': 0.0,
                    'sharpe_ratio': 0.0,
                    'max_drawdown': 0.0,
                    'win_rate': 0.0,
                    'profit_factor': 0.0
                },
                'fitness': 0.0,
                'generation': 0,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
    
    def start_auto_evolution(self):
        """启动自动进化"""
        if self.is_running:
            self.logger.warning("⚠️ 自动进化系统已在运行")
            return False
        
        try:
            self.is_running = True
            self.evolution_thread = threading.Thread(target=self._evolution_loop, daemon=True)
            self.evolution_thread.start()
            
            self.logger.info("🚀 全自动策略进化系统已启动")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 启动自动进化系统失败: {e}")
            self.is_running = False
            return False
    
    def stop_auto_evolution(self):
        """停止自动进化"""
        if not self.is_running:
            self.logger.warning("⚠️ 自动进化系统已经停止")
            return False
        
        try:
            self.is_running = False
            if self.evolution_thread:
                self.evolution_thread.join(timeout=5)
                if self.evolution_thread.is_alive():
                    self.logger.warning("⚠️ 进化线程未能在5秒内停止")
            
            self.logger.info("🛑 全自动策略进化系统已停止")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 停止自动进化系统失败: {e}")
            return False
    
    def _evolution_loop(self):
        """进化循环"""
        self.logger.info("🔄 开始进化循环...")
        
        while self.is_running:
            try:
                # 检查是否需要进化
                if self._should_evolve():
                    self.logger.info("🧬 开始策略进化...")
                    self._evolve_strategies()
                
                # 评估当前策略性能
                self._evaluate_strategies()
                
                # 更新进化状态
                self._update_evolution_state()
                
                # 保存状态
                self._save_evolution_state()
                
                # 记录日志
                self.logger.info(f"📊 进化状态更新 - 代数: {self.evolution_state['current_generation']}, 最佳适应度: {self.evolution_state['best_fitness']:.3f}")
                
                # 等待下一次检查
                time.sleep(3600)  # 每小时检查一次
                
            except Exception as e:
                self.logger.error(f"❌ 进化循环错误: {e}")
                time.sleep(300)  # 错误后等待5分钟
    
    def _should_evolve(self) -> bool:
        """检查是否需要进化"""
        # 检查时间间隔
        if self.evolution_state['last_evolution_date']:
            try:
                last_evolution = datetime.fromisoformat(self.evolution_state['last_evolution_date'])
                days_since_evolution = (datetime.now() - last_evolution).days
                
                if days_since_evolution < self.config.evolution_trigger_days:
                    self.logger.debug(f"⏳ 距离上次进化仅 {days_since_evolution} 天，未达到触发条件")
                    return False
            except Exception as e:
                self.logger.warning(f"⚠️ 解析上次进化时间失败: {e}")
        
        # 检查性能阈值
        if self.evolution_state['best_fitness'] < self.config.min_performance_threshold:
            self.logger.info(f"🎯 最佳适应度 {self.evolution_state['best_fitness']:.3f} 低于阈值 {self.config.min_performance_threshold}，触发进化")
            return True
        
        # 检查最大回撤
        if self.evolution_state['performance_metrics'].get('max_drawdown', 0) > self.config.max_drawdown_threshold:
            self.logger.info(f"⚠️ 最大回撤 {self.evolution_state['performance_metrics']['max_drawdown']:.3f} 超过阈值 {self.config.max_drawdown_threshold}，触发进化")
            return True
        
        # 检查是否是新系统（没有进化历史）
        if self.evolution_state['current_generation'] == 0:
            self.logger.info("🚀 新系统初始化，开始首次进化")
            return True
        
        self.logger.debug("✅ 系统运行正常，无需进化")
        return False
    
    def _evolve_strategies(self):
        """进化策略"""
        try:
            self.logger.info(f"🧬 开始第 {self.evolution_state['current_generation'] + 1} 代进化...")
            
            # 1. 选择优秀个体
            elite_strategies = self._select_elite_strategies()
            self.logger.info(f"🏆 选择了 {len(elite_strategies)} 个精英策略")
            
            # 2. 交叉繁殖
            offspring_strategies = self._crossover_strategies(elite_strategies)
            self.logger.info(f"🔄 生成了 {len(offspring_strategies)} 个子代策略")
            
            # 3. 变异
            mutated_strategies = self._mutate_strategies(offspring_strategies)
            self.logger.info(f"🧬 生成了 {len(mutated_strategies)} 个变异策略")
            
            # 4. 生成新策略
            new_strategies = self._generate_new_strategies()
            self.logger.info(f"🆕 生成了 {len(new_strategies)} 个新策略")
            
            # 5. 合并种群
            total_strategies = elite_strategies + mutated_strategies + new_strategies
            self.evolution_state['active_strategies'] = total_strategies[:self.config.population_size]
            
            # 6. 更新进化状态
            self.evolution_state['current_generation'] += 1
            self.evolution_state['last_evolution_date'] = datetime.now().isoformat()
            
            self.logger.info(f"✅ 第 {self.evolution_state['current_generation']} 代进化完成，种群大小: {len(self.evolution_state['active_strategies'])}")
            
        except Exception as e:
            self.logger.error(f"❌ 策略进化失败: {e}")
            raise
    
    def _select_elite_strategies(self) -> List[Dict[str, Any]]:
        """选择优秀个体"""
        strategies = self.evolution_state['active_strategies']
        sorted_strategies = sorted(strategies, key=lambda x: x['fitness'], reverse=True)
        return sorted_strategies[:self.config.elite_size]
    
    def _crossover_strategies(self, elite_strategies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """交叉繁殖"""
        offspring = []
        
        for i in range(len(elite_strategies) - 1):
            for j in range(i + 1, len(elite_strategies)):
                if np.random.random() < self.config.crossover_rate:
                    child = self._crossover_two_strategies(elite_strategies[i], elite_strategies[j])
                    offspring.append(child)
        
        return offspring
    
    def _crossover_two_strategies(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """两个策略交叉"""
        child = parent1.copy()
        child['id'] = hashlib.md5(f"crossover_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        child['name'] = f"crossover_{parent1['name']}_{parent2['name']}"
        child['generation'] = self.evolution_state['current_generation'] + 1
        child['created_at'] = datetime.now().isoformat()
        child['last_updated'] = datetime.now().isoformat()
        
        # 参数交叉
        for param_name in self.config.param_ranges.keys():
            if np.random.random() < 0.5:
                child['parameters'][param_name] = parent1['parameters'].get(param_name, 0)
            else:
                child['parameters'][param_name] = parent2['parameters'].get(param_name, 0)
        
        return child
    
    def _mutate_strategies(self, strategies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """变异策略"""
        mutated = []
        
        for strategy in strategies:
            if np.random.random() < self.config.mutation_rate:
                mutated_strategy = strategy.copy()
                mutated_strategy['id'] = hashlib.md5(f"mutation_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
                mutated_strategy['name'] = f"mutation_{strategy['name']}"
                mutated_strategy['generation'] = self.evolution_state['current_generation'] + 1
                mutated_strategy['created_at'] = datetime.now().isoformat()
                mutated_strategy['last_updated'] = datetime.now().isoformat()
                
                # 参数变异
                for param_name, (min_val, max_val) in self.config.param_ranges.items():
                    if np.random.random() < 0.3:  # 30%概率变异
                        current_val = mutated_strategy['parameters'].get(param_name, min_val)
                        mutation_range = (max_val - min_val) * 0.1  # 10%的变异范围
                        new_val = current_val + np.random.uniform(-mutation_range, mutation_range)
                        mutated_strategy['parameters'][param_name] = np.clip(new_val, min_val, max_val)
                
                mutated.append(mutated_strategy)
        
        return mutated
    
    def _generate_new_strategies(self) -> List[Dict[str, Any]]:
        """生成新策略"""
        new_count = self.config.population_size - len(self.evolution_state['active_strategies'])
        new_strategies = []
        
        for i in range(new_count):
            strategy = self._generate_random_strategy(f"new_strategy_{i}")
            strategy['generation'] = self.evolution_state['current_generation'] + 1
            new_strategies.append(strategy)
        
        return new_strategies
    
    def _evaluate_strategies(self):
        """评估策略性能"""
        try:
            self.logger.info("📊 评估策略性能...")
            
            # 获取市场数据
            market_data = self._get_market_data()
            if market_data is None or market_data.empty:
                self.logger.warning("⚠️ 无法获取市场数据，使用模拟评估")
                self._evaluate_strategies_simulation()
                return
            
            evaluated_count = 0
            for strategy in self.evolution_state['active_strategies']:
                try:
                    # 使用真实回测评估策略性能
                    backtest_result = self.backtest_engine.backtest_strategy(
                        strategy, market_data, initial_capital=10000.0
                    )
                    
                    # 更新策略性能
                    strategy['performance'] = {
                        'total_return': backtest_result.total_return,
                        'sharpe_ratio': backtest_result.sharpe_ratio,
                        'max_drawdown': backtest_result.max_drawdown,
                        'win_rate': backtest_result.win_rate,
                        'profit_factor': backtest_result.profit_factor
                    }
                    
                    # 计算适应度
                    strategy['fitness'] = self._calculate_fitness(strategy['performance'])
                    strategy['last_updated'] = datetime.now().isoformat()
                    
                    # 保存回测结果
                    self.backtest_engine.save_backtest_result(strategy['name'], backtest_result)
                    
                    evaluated_count += 1
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ 评估策略 {strategy.get('name', 'unknown')} 失败: {e}")
                    # 使用模拟评估作为备用
                    strategy['performance'] = self._simulate_strategy_performance(strategy)
                    strategy['fitness'] = self._calculate_fitness(strategy['performance'])
                    strategy['last_updated'] = datetime.now().isoformat()
            
            # 更新进化状态
            fitness_scores = [s['fitness'] for s in self.evolution_state['active_strategies']]
            self.evolution_state['best_fitness'] = max(fitness_scores) if fitness_scores else 0.0
            self.evolution_state['avg_fitness'] = np.mean(fitness_scores) if fitness_scores else 0.0
            
            self.logger.info(f"✅ 策略性能评估完成，评估了 {evaluated_count} 个策略，最佳适应度: {self.evolution_state['best_fitness']:.3f}")
            
        except Exception as e:
            self.logger.error(f"❌ 策略性能评估失败: {e}")
            self._evaluate_strategies_simulation()
    
    def _evaluate_strategies_simulation(self):
        """模拟策略性能评估（备用方案）"""
        try:
            self.logger.info("🔄 使用模拟评估策略性能...")
            
            for strategy in self.evolution_state['active_strategies']:
                # 模拟策略性能评估
                performance = self._simulate_strategy_performance(strategy)
                strategy['performance'] = performance
                strategy['fitness'] = self._calculate_fitness(performance)
                strategy['last_updated'] = datetime.now().isoformat()
            
            # 更新进化状态
            fitness_scores = [s['fitness'] for s in self.evolution_state['active_strategies']]
            self.evolution_state['best_fitness'] = max(fitness_scores) if fitness_scores else 0.0
            self.evolution_state['avg_fitness'] = np.mean(fitness_scores) if fitness_scores else 0.0
            
            self.logger.info(f"✅ 模拟策略性能评估完成，最佳适应度: {self.evolution_state['best_fitness']:.3f}")
            
        except Exception as e:
            self.logger.error(f"❌ 模拟策略性能评估失败: {e}")
    
    def _simulate_strategy_performance(self, strategy: Dict[str, Any]) -> Dict[str, float]:
        """模拟策略性能"""
        # 基于策略类型和参数生成更真实的模拟性能
        strategy_type = strategy.get('type', 'trend_following')
        
        # 根据策略类型调整性能范围
        if strategy_type == 'trend_following':
            base_return = np.random.uniform(-0.1, 0.3)
            base_sharpe = np.random.uniform(0.5, 1.5)
        elif strategy_type == 'mean_reversion':
            base_return = np.random.uniform(-0.05, 0.25)
            base_sharpe = np.random.uniform(0.3, 1.2)
        elif strategy_type == 'arbitrage':
            base_return = np.random.uniform(0.05, 0.15)
            base_sharpe = np.random.uniform(1.0, 2.0)
        else:  # grid_trading
            base_return = np.random.uniform(-0.05, 0.2)
            base_sharpe = np.random.uniform(0.4, 1.3)
        
        return {
            'total_return': base_return,
            'sharpe_ratio': base_sharpe,
            'max_drawdown': np.random.uniform(0.02, 0.15),
            'win_rate': np.random.uniform(0.4, 0.7),
            'profit_factor': np.random.uniform(0.8, 1.8)
        }
    
    def _calculate_fitness(self, performance: Dict[str, float]) -> float:
        """计算适应度"""
        try:
            # 确保所有性能指标都在合理范围内
            total_return = max(-1.0, min(1.0, performance.get('total_return', 0.0)))
            sharpe_ratio = max(-3.0, min(3.0, performance.get('sharpe_ratio', 0.0)))
            max_drawdown = max(0.0, min(1.0, performance.get('max_drawdown', 0.0)))
            win_rate = max(0.0, min(1.0, performance.get('win_rate', 0.0)))
            profit_factor = max(0.0, min(5.0, performance.get('profit_factor', 0.0)))
            
            # 计算加权适应度
            fitness = (
                total_return * self.config.return_weight +
                (1 - max_drawdown) * self.config.risk_weight +
                max(0, sharpe_ratio) * self.config.sharpe_weight +
                (1 - max_drawdown) * self.config.drawdown_weight
            )
            
            # 添加额外的奖励因子
            if win_rate > 0.6:
                fitness += 0.1  # 高胜率奖励
            if profit_factor > 1.5:
                fitness += 0.1  # 高盈亏比奖励
            if sharpe_ratio > 1.0:
                fitness += 0.1  # 高夏普比率奖励
            
            # 确保适应度在合理范围内
            fitness = max(0.0, min(1.0, fitness))
            
            return fitness
            
        except Exception as e:
            self.logger.error(f"❌ 计算适应度失败: {e}")
            return 0.0
    
    def _update_evolution_state(self):
        """更新进化状态"""
        try:
            # 更新性能指标
            if self.evolution_state['active_strategies']:
                performances = [s['performance'] for s in self.evolution_state['active_strategies']]
                
                self.evolution_state['performance_metrics'] = {
                    'avg_return': np.mean([p.get('total_return', 0.0) for p in performances]),
                    'avg_sharpe': np.mean([p.get('sharpe_ratio', 0.0) for p in performances]),
                    'max_drawdown': max([p.get('max_drawdown', 0.0) for p in performances]),
                    'avg_win_rate': np.mean([p.get('win_rate', 0.0) for p in performances]),
                    'avg_profit_factor': np.mean([p.get('profit_factor', 0.0) for p in performances])
                }
            
            # 记录进化历史
            evolution_record = {
                'generation': self.evolution_state['current_generation'],
                'best_fitness': self.evolution_state['best_fitness'],
                'avg_fitness': self.evolution_state['avg_fitness'],
                'population_size': len(self.evolution_state['active_strategies']),
                'performance_metrics': self.evolution_state['performance_metrics'].copy(),
                'timestamp': datetime.now().isoformat()
            }
            
            self.evolution_state['evolution_history'].append(evolution_record)
            
            # 限制历史记录数量，避免内存占用过大
            if len(self.evolution_state['evolution_history']) > 100:
                self.evolution_state['evolution_history'] = self.evolution_state['evolution_history'][-50:]
            
            self.logger.debug(f"📊 进化状态已更新 - 代数: {self.evolution_state['current_generation']}, 种群大小: {len(self.evolution_state['active_strategies'])}")
            
        except Exception as e:
            self.logger.error(f"❌ 更新进化状态失败: {e}")
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """获取进化总结"""
        try:
            return {
                'current_generation': self.evolution_state['current_generation'],
                'best_fitness': self.evolution_state['best_fitness'],
                'avg_fitness': self.evolution_state['avg_fitness'],
                'population_size': len(self.evolution_state['active_strategies']),
                'performance_metrics': self.evolution_state['performance_metrics'],
                'last_evolution_date': self.evolution_state['last_evolution_date'],
                'evolution_history': self.evolution_state['evolution_history'][-10:],  # 最近10代
                'top_strategies': self._get_top_strategies(5)
            }
        except Exception as e:
            self.logger.error(f"❌ 获取进化总结失败: {e}")
            return {
                'current_generation': 0,
                'best_fitness': 0.0,
                'avg_fitness': 0.0,
                'population_size': 0,
                'performance_metrics': {},
                'last_evolution_date': None,
                'evolution_history': [],
                'top_strategies': []
            }
    
    def _get_top_strategies(self, top_k: int = 5) -> List[Dict[str, Any]]:
        """获取顶级策略"""
        strategies = self.evolution_state['active_strategies']
        sorted_strategies = sorted(strategies, key=lambda x: x['fitness'], reverse=True)
        return sorted_strategies[:top_k]
    
    def export_evolution_report(self, output_path: str = None) -> str:
        """导出进化报告"""
        if output_path is None:
            output_path = os.path.join(self.data_dir, f"evolution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        
        try:
            summary = self.get_evolution_summary()
            html_content = self._generate_evolution_report_html(summary)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"✅ 进化报告已导出: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"❌ 导出进化报告失败: {e}")
            return ""
    
    def _generate_evolution_report_html(self, summary: Dict[str, Any]) -> str:
        """生成进化报告HTML"""
        html_template = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>全自动策略进化报告</title>
            <style>
                body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
                .summary-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }
                .summary-card h3 { margin: 0 0 10px 0; font-size: 18px; }
                .summary-card .value { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
                .strategies-section { margin: 30px 0; }
                .strategy-card { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #3498db; }
                .evolution-history { margin: 30px 0; }
                .history-item { background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #ffc107; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧬 全自动策略进化报告</h1>
                
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>当前代数</h3>
                        <div class="value">{current_generation}</div>
                    </div>
                    <div class="summary-card">
                        <h3>最佳适应度</h3>
                        <div class="value">{best_fitness:.3f}</div>
                    </div>
                    <div class="summary-card">
                        <h3>平均适应度</h3>
                        <div class="value">{avg_fitness:.3f}</div>
                    </div>
                    <div class="summary-card">
                        <h3>种群大小</h3>
                        <div class="value">{population_size}</div>
                    </div>
                </div>
                
                <div class="strategies-section">
                    <h2>🏆 顶级策略</h2>
                    {strategies_html}
                </div>
                
                <div class="evolution-history">
                    <h2>📈 进化历史</h2>
                    {history_html}
                </div>
            </div>
        </body>
        </html>
        """
        
        # 生成策略HTML
        strategies_html = ""
        for strategy in summary.get('top_strategies', []):
            strategies_html += f"""
            <div class="strategy-card">
                <h4>{strategy['name']}</h4>
                <p>适应度: {strategy['fitness']:.3f}</p>
                <p>总收益: {strategy['performance']['total_return']:.2%}</p>
                <p>夏普比率: {strategy['performance']['sharpe_ratio']:.2f}</p>
                <p>最大回撤: {strategy['performance']['max_drawdown']:.2%}</p>
            </div>
            """
        
        # 生成历史HTML
        history_html = ""
        for record in summary.get('evolution_history', []):
            history_html += f"""
            <div class="history-item">
                <h4>第 {record['generation']} 代</h4>
                <p>最佳适应度: {record['best_fitness']:.3f}</p>
                <p>平均适应度: {record['avg_fitness']:.3f}</p>
                <p>时间: {record['timestamp']}</p>
            </div>
            """
        
        return html_template.format(
            current_generation=summary['current_generation'],
            best_fitness=summary['best_fitness'],
            avg_fitness=summary['avg_fitness'],
            population_size=summary['population_size'],
            strategies_html=strategies_html,
            history_html=history_html
        ) 
    
    def _get_market_data(self) -> Optional[pd.DataFrame]:
        """获取市场数据"""
        try:
            # 检查缓存是否有效（1小时内）
            if (self.market_data_cache is not None and 
                self.last_market_data_update and 
                (datetime.now() - self.last_market_data_update).seconds < 3600):
                return self.market_data_cache
            
            # 尝试从数据管理器获取市场数据
            try:
                from data.market_data_collector import MarketDataCollector
                collector = MarketDataCollector()
                
                # 使用正确的方法名
                market_data = collector.fetch_ohlcv(
                    exchange_name='binance',
                    symbol='BTC/USDT',
                    timeframe='1h',
                    limit=1000
                )
                
                if market_data is not None and not market_data.empty:
                    self.market_data_cache = market_data
                    self.last_market_data_update = datetime.now()
                    self.logger.info("✅ 市场数据已更新")
                    return market_data
                    
            except ImportError:
                self.logger.warning("⚠️ 市场数据收集器未找到")
            except Exception as e:
                self.logger.warning(f"⚠️ 获取市场数据失败: {e}")
            
            # 尝试从文件加载历史数据
            data_file = "data/market_data.csv"
            if os.path.exists(data_file):
                try:
                    market_data = pd.read_csv(data_file, index_col=0, parse_dates=True)
                    if not market_data.empty:
                        self.market_data_cache = market_data
                        self.last_market_data_update = datetime.now()
                        self.logger.info("✅ 从文件加载市场数据成功")
                        return market_data
                except Exception as e:
                    self.logger.warning(f"⚠️ 从文件加载市场数据失败: {e}")
            
            # 生成模拟市场数据
            self.logger.warning("⚠️ 无法获取真实市场数据，生成模拟数据")
            return self._generate_simulated_market_data()
            
        except Exception as e:
            self.logger.error(f"❌ 获取市场数据失败: {e}")
            return None
    
    def _generate_simulated_market_data(self) -> pd.DataFrame:
        """生成模拟市场数据"""
        try:
            # 生成时间序列
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            dates = pd.date_range(start=start_date, end=end_date, freq='1H')
            
            # 生成价格数据
            np.random.seed(42)  # 固定随机种子
            initial_price = 50000
            returns = np.random.normal(0, 0.02, len(dates))  # 2%的日波动率
            prices = [initial_price]
            
            for ret in returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(new_price)
            
            # 生成OHLCV数据
            data = pd.DataFrame({
                'open': prices,
                'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                'close': prices,
                'volume': np.random.uniform(1000, 10000, len(dates))
            }, index=dates)
            
            # 确保high >= max(open, close), low <= min(open, close)
            data['high'] = data[['open', 'close', 'high']].max(axis=1)
            data['low'] = data[['open', 'close', 'low']].min(axis=1)
            
            return data
            
        except Exception as e:
            self.logger.error(f"❌ 生成模拟市场数据失败: {e}")
            return pd.DataFrame() 