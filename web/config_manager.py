#!/usr/bin/env python3
"""
配置管理器
处理系统配置的持久化存储和实时更新
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config_dir = Path('config')
        self.config_dir.mkdir(exist_ok=True)
        
        self.db_path = self.config_dir / 'system_config.db'
        self.config_file = self.config_dir / 'system_config.json'
        
        # 初始化数据库
        self._init_database()
        
        # 加载默认配置
        self.default_config = self._get_default_config()
        
        # 加载当前配置
        self.current_config = self.load_config()
        
        self.logger = logging.getLogger(__name__)
    
    def _init_database(self):
        """初始化配置数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建配置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_key TEXT UNIQUE NOT NULL,
                    config_value TEXT NOT NULL,
                    config_type TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建配置历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    config_key TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT NOT NULL,
                    changed_by TEXT DEFAULT 'system',
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ 初始化配置数据库失败: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            # 数据库配置
            'db_host': 'localhost',
            'db_port': 27017,
            'db_name': 'jesse_plus',
            
            # 交易所配置
            'exchange': 'Binance',
            'api_key': '',
            'api_secret': '',
            
            # AI模型配置
            'lstm_units': 128,
            'transformer_layers': 6,
            'learning_rate': 0.001,
            
            # 风险控制配置
            'max_drawdown': 10.0,
            'daily_loss_limit': 5.0,
            'max_position_size': 15.0,
            'stop_loss_threshold': 5.0,
            
            # 系统配置
            'auto_refresh': True,
            'show_ai_process': True,
            'show_decision_process': True,
            'show_strategy_evolution': True,
            
            # 策略配置
            'active_strategies': ['AI增强策略', '移动平均线交叉策略', 'RSI策略'],
            'prediction_horizon': 24,
            'confidence_threshold': 0.7
        }
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            # 首先尝试从数据库加载
            config = self._load_from_database()
            
            # 如果数据库为空，使用默认配置
            if not config:
                config = self.default_config.copy()
                self._save_to_database(config)
            
            return config
            
        except Exception as e:
            self.logger.error(f"❌ 加载配置失败: {e}")
            return self.default_config.copy()
    
    def _load_from_database(self) -> Dict[str, Any]:
        """从数据库加载配置"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT config_key, config_value, config_type FROM system_config')
            rows = cursor.fetchall()
            
            config = {}
            for row in rows:
                key, value, config_type = row
                
                # 根据类型转换值
                if config_type == 'int':
                    config[key] = int(value)
                elif config_type == 'float':
                    config[key] = float(value)
                elif config_type == 'bool':
                    config[key] = value.lower() == 'true'
                elif config_type == 'list':
                    config[key] = json.loads(value)
                else:
                    config[key] = value
            
            conn.close()
            return config
            
        except Exception as e:
            self.logger.error(f"❌ 从数据库加载配置失败: {e}")
            return {}
    
    def _save_to_database(self, config: Dict[str, Any]):
        """保存配置到数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for key, value in config.items():
                # 确定值的类型
                if isinstance(value, bool):
                    config_type = 'bool'
                    value_str = str(value).lower()
                elif isinstance(value, int):
                    config_type = 'int'
                    value_str = str(value)
                elif isinstance(value, float):
                    config_type = 'float'
                    value_str = str(value)
                elif isinstance(value, list):
                    config_type = 'list'
                    value_str = json.dumps(value)
                else:
                    config_type = 'string'
                    value_str = str(value)
                
                # 插入或更新配置
                cursor.execute('''
                    INSERT OR REPLACE INTO system_config 
                    (config_key, config_value, config_type, updated_at) 
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (key, value_str, config_type))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"❌ 保存配置到数据库失败: {e}")
    
    def update_config(self, key: str, value: Any, user: str = 'web_interface') -> bool:
        """更新配置"""
        try:
            # 获取旧值
            old_value = self.current_config.get(key)
            
            # 更新当前配置
            self.current_config[key] = value
            
            # 保存到数据库
            self._save_to_database({key: value})
            
            # 记录历史
            self._log_config_change(key, old_value, value, user)
            
            self.logger.info(f"✅ 配置已更新: {key} = {value}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 更新配置失败: {e}")
            return False
    
    def _log_config_change(self, key: str, old_value: Any, new_value: Any, user: str):
        """记录配置变更历史"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO config_history 
                (config_key, old_value, new_value, changed_by) 
                VALUES (?, ?, ?, ?)
            ''', (key, str(old_value) if old_value is not None else None, str(new_value), user))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"❌ 记录配置变更失败: {e}")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.current_config.get(key, default)
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self.current_config.copy()
    
    def reset_config(self) -> bool:
        """重置为默认配置"""
        try:
            self.current_config = self.default_config.copy()
            self._save_to_database(self.current_config)
            self.logger.info("✅ 配置已重置为默认值")
            return True
        except Exception as e:
            self.logger.error(f"❌ 重置配置失败: {e}")
            return False
    
    def get_config_history(self, key: str = None, limit: int = 50) -> list:
        """获取配置变更历史"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if key:
                cursor.execute('''
                    SELECT config_key, old_value, new_value, changed_by, changed_at 
                    FROM config_history 
                    WHERE config_key = ? 
                    ORDER BY changed_at DESC 
                    LIMIT ?
                ''', (key, limit))
            else:
                cursor.execute('''
                    SELECT config_key, old_value, new_value, changed_by, changed_at 
                    FROM config_history 
                    ORDER BY changed_at DESC 
                    LIMIT ?
                ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            history = []
            for row in rows:
                history.append({
                    'config_key': row[0],
                    'old_value': row[1],
                    'new_value': row[2],
                    'changed_by': row[3],
                    'changed_at': row[4]
                })
            
            return history
            
        except Exception as e:
            self.logger.error(f"❌ 获取配置历史失败: {e}")
            return [] 