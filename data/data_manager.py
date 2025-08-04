"""
数据管理器
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from pathlib import Path

from utils.logging_manager import LoggerMixin
from config.database_config import DatabaseConfig

class DataManager(LoggerMixin):
    """数据管理器"""
    
    def __init__(self):
        """初始化数据管理器"""
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据缓存
        self.cache = {}
        self.cache_expiry = {}
        
    def save_market_data(self, exchange: str, symbol: str, 
                        timeframe: str, data: pd.DataFrame) -> bool:
        """
        保存市场数据
        
        Args:
            exchange: 交易所
            symbol: 交易对
            timeframe: 时间框架
            data: 市场数据
            
        Returns:
            是否保存成功
        """
        try:
            filename = f"{exchange}_{symbol}_{timeframe}.csv"
            filepath = self.data_dir / 'market_data' / filename
            
            # 创建目录
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存数据
            data.to_csv(filepath, index=False)
            
            # 更新缓存
            cache_key = f"{exchange}_{symbol}_{timeframe}"
            self.cache[cache_key] = data
            self.cache_expiry[cache_key] = datetime.now() + timedelta(hours=1)
            
            self.logger.info(f"✅ 市场数据已保存: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存市场数据失败: {e}")
            return False
    
    def load_market_data(self, exchange: str, symbol: str, 
                        timeframe: str, days: int = 30) -> Optional[pd.DataFrame]:
        """
        加载市场数据
        
        Args:
            exchange: 交易所
            symbol: 交易对
            timeframe: 时间框架
            days: 天数
            
        Returns:
            市场数据
        """
        try:
            filename = f"{exchange}_{symbol}_{timeframe}.csv"
            filepath = self.data_dir / 'market_data' / filename
            
            # 检查缓存
            cache_key = f"{exchange}_{symbol}_{timeframe}"
            if cache_key in self.cache:
                cache_time = self.cache_expiry.get(cache_key)
                if cache_time and datetime.now() < cache_time:
                    data = self.cache[cache_key]
                    if days:
                        start_date = datetime.now() - timedelta(days=days)
                        data = data[data['timestamp'] >= start_date]
                    return data
            
            # 从文件加载
            if filepath.exists():
                data = pd.read_csv(filepath)
                data['timestamp'] = pd.to_datetime(data['timestamp'])
                
                # 过滤时间范围
                if days:
                    start_date = datetime.now() - timedelta(days=days)
                    data = data[data['timestamp'] >= start_date]
                
                # 更新缓存
                self.cache[cache_key] = data
                self.cache_expiry[cache_key] = datetime.now() + timedelta(hours=1)
                
                self.logger.info(f"✅ 市场数据已加载: {filename}")
                return data
            else:
                self.logger.warning(f"⚠️ 市场数据文件不存在: {filename}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ 加载市场数据失败: {e}")
            return None
    
    def save_trading_signals(self, signals: List[Dict[str, Any]]) -> bool:
        """
        保存交易信号
        
        Args:
            signals: 交易信号列表
            
        Returns:
            是否保存成功
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trading_signals_{timestamp}.json"
            filepath = self.data_dir / 'signals' / filename
            
            # 创建目录
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存信号
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(signals, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"✅ 交易信号已保存: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存交易信号失败: {e}")
            return False
    
    def load_trading_signals(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        加载交易信号
        
        Args:
            days: 天数
            
        Returns:
            交易信号列表
        """
        try:
            signals_dir = self.data_dir / 'signals'
            if not signals_dir.exists():
                return []
            
            signals = []
            start_date = datetime.now() - timedelta(days=days)
            
            for filepath in signals_dir.glob('trading_signals_*.json'):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_signals = json.load(f)
                    
                    # 过滤时间范围
                    filtered_signals = []
                    for signal in file_signals:
                        signal_time = datetime.fromisoformat(signal['timestamp'])
                        if signal_time >= start_date:
                            filtered_signals.append(signal)
                    
                    signals.extend(filtered_signals)
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ 加载信号文件失败: {filepath}, 错误: {e}")
            
            self.logger.info(f"✅ 加载了 {len(signals)} 个交易信号")
            return signals
            
        except Exception as e:
            self.logger.error(f"❌ 加载交易信号失败: {e}")
            return []
    
    def save_ai_model(self, model_name: str, model_data: Any, 
                     model_type: str = 'lstm') -> bool:
        """
        保存AI模型
        
        Args:
            model_name: 模型名称
            model_data: 模型数据
            model_type: 模型类型
            
        Returns:
            是否保存成功
        """
        try:
            model_dir = self.data_dir / 'models' / model_type
            model_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = model_dir / f"{model_name}.pkl"
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            self.logger.info(f"✅ AI模型已保存: {model_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存AI模型失败: {e}")
            return False
    
    def load_ai_model(self, model_name: str, model_type: str = 'lstm') -> Optional[Any]:
        """
        加载AI模型
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            AI模型
        """
        try:
            model_dir = self.data_dir / 'models' / model_type
            filepath = model_dir / f"{model_name}.pkl"
            
            if filepath.exists():
                with open(filepath, 'rb') as f:
                    model = pickle.load(f)
                
                self.logger.info(f"✅ AI模型已加载: {model_name}")
                return model
            else:
                self.logger.warning(f"⚠️ AI模型文件不存在: {filepath}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ 加载AI模型失败: {e}")
            return None
    
    def save_performance_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        保存性能指标
        
        Args:
            metrics: 性能指标
            
        Returns:
            是否保存成功
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"performance_metrics_{timestamp}.json"
            filepath = self.data_dir / 'performance' / filename
            
            # 创建目录
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存指标
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, ensure_ascii=False, indent=2, default=str)
            
            self.logger.info(f"✅ 性能指标已保存: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存性能指标失败: {e}")
            return False
    
    def get_data_info(self) -> Dict[str, Any]:
        """
        获取数据信息
        
        Returns:
            数据信息
        """
        info = {
            'data_directory': str(self.data_dir),
            'market_data_files': [],
            'signal_files': [],
            'model_files': [],
            'performance_files': []
        }
        
        # 市场数据文件
        market_data_dir = self.data_dir / 'market_data'
        if market_data_dir.exists():
            info['market_data_files'] = [f.name for f in market_data_dir.glob('*.csv')]
        
        # 信号文件
        signals_dir = self.data_dir / 'signals'
        if signals_dir.exists():
            info['signal_files'] = [f.name for f in signals_dir.glob('*.json')]
        
        # 模型文件
        models_dir = self.data_dir / 'models'
        if models_dir.exists():
            for model_type_dir in models_dir.iterdir():
                if model_type_dir.is_dir():
                    model_files = [f.name for f in model_type_dir.glob('*.pkl')]
                    info['model_files'].extend([f"{model_type_dir.name}/{f}" for f in model_files])
        
        # 性能指标文件
        performance_dir = self.data_dir / 'performance'
        if performance_dir.exists():
            info['performance_files'] = [f.name for f in performance_dir.glob('*.json')]
        
        return info
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """
        清理旧数据
        
        Args:
            days: 保留天数
            
        Returns:
            清理的文件数量
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cleaned_files = 0
            
            # 清理信号文件
            signals_dir = self.data_dir / 'signals'
            if signals_dir.exists():
                for filepath in signals_dir.glob('trading_signals_*.json'):
                    file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if file_time < cutoff_date:
                        filepath.unlink()
                        cleaned_files += 1
            
            # 清理性能指标文件
            performance_dir = self.data_dir / 'performance'
            if performance_dir.exists():
                for filepath in performance_dir.glob('performance_metrics_*.json'):
                    file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if file_time < cutoff_date:
                        filepath.unlink()
                        cleaned_files += 1
            
            self.logger.info(f"✅ 清理了 {cleaned_files} 个旧文件")
            return cleaned_files
            
        except Exception as e:
            self.logger.error(f"❌ 清理旧数据失败: {e}")
            return 0 