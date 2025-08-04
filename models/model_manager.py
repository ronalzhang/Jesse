"""
AI模型管理器
"""

import os
import json
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from utils.logging_manager import LoggerMixin
from config.ai_config import AIConfig

class ModelManager(LoggerMixin):
    """AI模型管理器"""
    
    def __init__(self):
        """初始化模型管理器"""
        self.models_dir = Path('models')
        self.models_dir.mkdir(exist_ok=True)
        
        # 模型缓存
        self.model_cache = {}
        self.model_configs = {}
        
        # 加载模型配置
        self._load_model_configs()
    
    def _load_model_configs(self):
        """加载模型配置"""
        self.model_configs = {
            'lstm': AIConfig.get_lstm_config(),
            'transformer': AIConfig.get_transformer_config(),
            'garch': AIConfig.get_garch_config(),
            'rl': AIConfig.get_rl_config(),
            'sentiment': AIConfig.get_sentiment_config()
        }
    
    def save_model(self, model_name: str, model: Any, 
                  model_type: str = 'lstm', metadata: Dict[str, Any] = None) -> bool:
        """
        保存模型
        
        Args:
            model_name: 模型名称
            model: 模型对象
            model_type: 模型类型
            metadata: 模型元数据
            
        Returns:
            是否保存成功
        """
        try:
            model_dir = self.models_dir / model_type
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存模型文件
            model_file = model_dir / f"{model_name}.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(model, f)
            
            # 保存元数据
            metadata_file = model_dir / f"{model_name}_metadata.json"
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'model_name': model_name,
                'model_type': model_type,
                'created_at': datetime.now().isoformat(),
                'version': '1.0'
            })
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            # 更新缓存
            cache_key = f"{model_type}_{model_name}"
            self.model_cache[cache_key] = model
            
            self.logger.info(f"✅ 模型已保存: {model_name} ({model_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 保存模型失败: {e}")
            return False
    
    def load_model(self, model_name: str, model_type: str = 'lstm') -> Optional[Any]:
        """
        加载模型
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            模型对象
        """
        try:
            # 检查缓存
            cache_key = f"{model_type}_{model_name}"
            if cache_key in self.model_cache:
                self.logger.info(f"✅ 从缓存加载模型: {model_name}")
                return self.model_cache[cache_key]
            
            model_dir = self.models_dir / model_type
            model_file = model_dir / f"{model_name}.pkl"
            
            if not model_file.exists():
                self.logger.warning(f"⚠️ 模型文件不存在: {model_file}")
                return None
            
            # 加载模型
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
            
            # 更新缓存
            self.model_cache[cache_key] = model
            
            self.logger.info(f"✅ 模型已加载: {model_name} ({model_type})")
            return model
            
        except Exception as e:
            self.logger.error(f"❌ 加载模型失败: {e}")
            return None
    
    def get_model_metadata(self, model_name: str, model_type: str = 'lstm') -> Optional[Dict[str, Any]]:
        """
        获取模型元数据
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            模型元数据
        """
        try:
            model_dir = self.models_dir / model_type
            metadata_file = model_dir / f"{model_name}_metadata.json"
            
            if not metadata_file.exists():
                return None
            
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"❌ 获取模型元数据失败: {e}")
            return None
    
    def list_models(self, model_type: str = None) -> Dict[str, List[str]]:
        """
        列出所有模型
        
        Args:
            model_type: 模型类型（可选）
            
        Returns:
            模型列表
        """
        try:
            models = {}
            
            if model_type:
                model_types = [model_type]
            else:
                model_types = ['lstm', 'transformer', 'garch', 'rl', 'sentiment']
            
            for mt in model_types:
                model_dir = self.models_dir / mt
                if model_dir.exists():
                    model_files = []
                    for file in model_dir.glob('*.pkl'):
                        model_name = file.stem
                        model_files.append(model_name)
                    models[mt] = model_files
            
            return models
            
        except Exception as e:
            self.logger.error(f"❌ 列出模型失败: {e}")
            return {}
    
    def delete_model(self, model_name: str, model_type: str = 'lstm') -> bool:
        """
        删除模型
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            是否删除成功
        """
        try:
            model_dir = self.models_dir / model_type
            model_file = model_dir / f"{model_name}.pkl"
            metadata_file = model_dir / f"{model_name}_metadata.json"
            
            # 删除模型文件
            if model_file.exists():
                model_file.unlink()
            
            # 删除元数据文件
            if metadata_file.exists():
                metadata_file.unlink()
            
            # 从缓存中移除
            cache_key = f"{model_type}_{model_name}"
            if cache_key in self.model_cache:
                del self.model_cache[cache_key]
            
            self.logger.info(f"✅ 模型已删除: {model_name} ({model_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 删除模型失败: {e}")
            return False
    
    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """
        获取模型配置
        
        Args:
            model_type: 模型类型
            
        Returns:
            模型配置
        """
        return self.model_configs.get(model_type, {}).copy()
    
    def update_model_config(self, model_type: str, config: Dict[str, Any]) -> bool:
        """
        更新模型配置
        
        Args:
            model_type: 模型类型
            config: 新配置
            
        Returns:
            是否更新成功
        """
        try:
            if model_type in self.model_configs:
                self.model_configs[model_type].update(config)
                self.logger.info(f"✅ 模型配置已更新: {model_type}")
                return True
            else:
                self.logger.error(f"❌ 不支持的模型类型: {model_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ 更新模型配置失败: {e}")
            return False
    
    def get_model_info(self, model_name: str, model_type: str = 'lstm') -> Dict[str, Any]:
        """
        获取模型信息
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            模型信息
        """
        try:
            info = {
                'model_name': model_name,
                'model_type': model_type,
                'exists': False,
                'metadata': None,
                'config': self.get_model_config(model_type)
            }
            
            # 检查模型是否存在
            model_dir = self.models_dir / model_type
            model_file = model_dir / f"{model_name}.pkl"
            info['exists'] = model_file.exists()
            
            # 获取元数据
            if info['exists']:
                info['metadata'] = self.get_model_metadata(model_name, model_type)
                
                # 获取文件大小
                info['file_size'] = model_file.stat().st_size
                info['created_at'] = datetime.fromtimestamp(model_file.stat().st_ctime).isoformat()
            
            return info
            
        except Exception as e:
            self.logger.error(f"❌ 获取模型信息失败: {e}")
            return {}
    
    def cleanup_cache(self):
        """清理模型缓存"""
        self.model_cache.clear()
        self.logger.info("✅ 模型缓存已清理")
    
    def get_models_summary(self) -> Dict[str, Any]:
        """
        获取模型摘要
        
        Returns:
            模型摘要
        """
        try:
            summary = {
                'total_models': 0,
                'models_by_type': {},
                'cache_size': len(self.model_cache),
                'models_directory': str(self.models_dir)
            }
            
            models = self.list_models()
            for model_type, model_list in models.items():
                summary['models_by_type'][model_type] = len(model_list)
                summary['total_models'] += len(model_list)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ 获取模型摘要失败: {e}")
            return {} 