"""
系统监控器
提供系统性能监控和错误处理功能
"""

import logging
import time
import psutil
import pandas as pd
from typing import Dict, Any

class SystemMonitor:
    """系统监控器"""
    
    def __init__(self):
        """初始化系统监控器"""
        self.logger = logging.getLogger(__name__)
        self.start_time = None
        self.error_count = 0
        self.performance_metrics = []
        
    def initialize(self):
        """初始化系统监控器"""
        try:
            self.logger.info("🔧 初始化系统监控器...")
            self.start_time = time.time()
            self.logger.info("✅ 系统监控器初始化完成")
        except Exception as e:
            self.logger.error(f"❌ 系统监控器初始化失败: {e}")
            raise
    
    def monitor_performance(self, trading_results: Dict[str, Any]):
        """监控系统性能"""
        try:
            # 获取系统资源使用情况
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # 记录性能指标
            metrics = {
                'timestamp': pd.Timestamp.now(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available / (1024**3),  # GB
                'disk_percent': disk.percent,
                'disk_free': disk.free / (1024**3),  # GB
                'uptime': time.time() - self.start_time if self.start_time else 0,
                'error_count': self.error_count,
                'trading_results_count': len(trading_results) if trading_results else 0
            }
            
            self.performance_metrics.append(metrics)
            
            # 检查系统健康状态
            self._check_system_health(metrics)
            
            self.logger.info(f"📊 系统性能监控: CPU {cpu_percent:.1f}%, 内存 {memory.percent:.1f}%")
            
        except Exception as e:
            self.logger.error(f"❌ 性能监控失败: {e}")
    
    def record_error(self, error: Exception):
        """记录错误"""
        try:
            self.error_count += 1
            self.logger.error(f"❌ 系统错误 #{self.error_count}: {error}")
            
            # 如果错误过多，可以考虑重启系统
            if self.error_count > 10:
                self.logger.warning("⚠️ 错误次数过多，建议检查系统状态")
                
        except Exception as e:
            self.logger.error(f"❌ 记录错误失败: {e}")
    
    def _check_system_health(self, metrics: Dict[str, Any]):
        """检查系统健康状态"""
        try:
            warnings = []
            
            # CPU使用率检查
            if metrics['cpu_percent'] > 80:
                warnings.append(f"CPU使用率过高: {metrics['cpu_percent']:.1f}%")
            
            # 内存使用率检查
            if metrics['memory_percent'] > 85:
                warnings.append(f"内存使用率过高: {metrics['memory_percent']:.1f}%")
            
            # 磁盘使用率检查
            if metrics['disk_percent'] > 90:
                warnings.append(f"磁盘使用率过高: {metrics['disk_percent']:.1f}%")
            
            # 错误次数检查
            if metrics['error_count'] > 5:
                warnings.append(f"错误次数过多: {metrics['error_count']}")
            
            # 输出警告
            for warning in warnings:
                self.logger.warning(f"⚠️ 系统健康警告: {warning}")
                
        except Exception as e:
            self.logger.error(f"❌ 系统健康检查失败: {e}")
    
    def update_status(self, status_data: Dict[str, Any]):
        """更新系统状态"""
        try:
            # 记录状态更新
            self.logger.info(f"📊 系统状态更新: {status_data}")
            
            # 这里可以添加状态持久化逻辑
            # 例如保存到数据库或文件
            
        except Exception as e:
            self.logger.error(f"❌ 状态更新失败: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        try:
            if not self.performance_metrics:
                return {'status': 'no_data'}
            
            latest_metrics = self.performance_metrics[-1]
            
            return {
                'status': 'healthy',
                'uptime_hours': latest_metrics['uptime'] / 3600,
                'cpu_percent': latest_metrics['cpu_percent'],
                'memory_percent': latest_metrics['memory_percent'],
                'disk_percent': latest_metrics['disk_percent'],
                'error_count': latest_metrics['error_count'],
                'total_metrics': len(self.performance_metrics)
            }
            
        except Exception as e:
            self.logger.error(f"❌ 获取性能摘要失败: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def cleanup(self):
        """清理系统监控器资源"""
        try:
            self.logger.info("🧹 清理系统监控器资源...")
            
            # 保存性能指标到文件（可选）
            if self.performance_metrics:
                df = pd.DataFrame(self.performance_metrics)
                df.to_csv('performance_metrics.csv', index=False)
                self.logger.info("📊 性能指标已保存到 performance_metrics.csv")
            
            self.logger.info("✅ 系统监控器清理完成")
            
        except Exception as e:
            self.logger.error(f"❌ 系统监控器清理失败: {e}") 