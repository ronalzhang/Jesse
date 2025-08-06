#!/usr/bin/env python3
"""
高频量化交易系统环境配置模板
请复制此文件为 env_high_frequency.py 并填入实际配置
"""

import os
from datetime import datetime

# ============================================================================
# 数据库配置
# ============================================================================

# Redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''  # 如果Redis设置了密码，请填入

# MongoDB配置
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'jesse_plus'
MONGODB_USERNAME = ''  # MongoDB用户名（可选）
MONGODB_PASSWORD = ''  # MongoDB密码（可选）

# ============================================================================
# 交易所API配置
# ============================================================================

# OKX交易所配置
OKX_API_KEY = 'your_okx_api_key_here'
OKX_SECRET_KEY = 'your_okx_secret_key_here'
OKX_PASSPHRASE = 'your_okx_passphrase_here'
OKX_SANDBOX = True  # 测试环境设为True，生产环境设为False

# Binance交易所配置
BINANCE_API_KEY = 'your_binance_api_key_here'
BINANCE_SECRET_KEY = 'your_binance_secret_key_here'
BINANCE_SANDBOX = True  # 测试环境设为True，生产环境设为False

# Bitget交易所配置
BITGET_API_KEY = 'your_bitget_api_key_here'
BITGET_SECRET_KEY = 'your_bitget_secret_key_here'
BITGET_PASSPHRASE = 'your_bitget_passphrase_here'
BITGET_SANDBOX = True  # 测试环境设为True，生产环境设为False

# ============================================================================
# 交易策略配置
# ============================================================================

# 交易对配置
TRADING_PAIRS = [
    'BTC/USDT',
    'ETH/USDT',
    'BNB/USDT',
    'SOL/USDT'
]

# 时间框架配置
TIMEFRAMES = ['1m', '5m', '15m', '1h']

# 高频交易参数
HIGH_FREQ_CONFIG = {
    'min_spread_threshold': 0.001,  # 最小价差 0.1%
    'max_position_size': 0.1,       # 最大仓位 10%
    'transaction_fee': 0.001,       # 手续费 0.1%
    'slippage': 0.0005,            # 滑点 0.05%
    'scan_interval': 300,           # 扫描间隔 5分钟
    'max_concurrent_trades': 3      # 最大并发交易数
}

# ============================================================================
# 风险控制配置
# ============================================================================

RISK_CONTROL = {
    'max_daily_loss': 0.05,         # 日最大损失 5%
    'max_drawdown': 0.1,            # 最大回撤 10%
    'stop_loss_threshold': 0.02,    # 止损阈值 2%
    'take_profit_threshold': 0.03,  # 止盈阈值 3%
    'max_position_per_trade': 0.05, # 单笔交易最大仓位 5%
    'min_balance_required': 100     # 最小余额要求 USDT
}

# ============================================================================
# AI模型配置
# ============================================================================

AI_CONFIG = {
    'lstm_units': 128,
    'transformer_layers': 6,
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 100,
    'validation_split': 0.2,
    'model_save_path': 'models/',
    'prediction_threshold': 0.7     # AI预测置信度阈值
}

# ============================================================================
# 监控和日志配置
# ============================================================================

MONITORING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'logs/high_frequency_trading.log',
    'max_log_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'alert_email': 'your_email@example.com',
    'webhook_url': 'your_webhook_url_here',
    'performance_metrics': {
        'track_sharpe_ratio': True,
        'track_max_drawdown': True,
        'track_win_rate': True,
        'track_profit_factor': True
    }
}

# ============================================================================
# 系统配置
# ============================================================================

SYSTEM_CONFIG = {
    'environment': 'development',  # development, staging, production
    'debug': True,
    'auto_restart': True,
    'health_check_interval': 60,  # 健康检查间隔（秒）
    'data_backup_interval': 3600, # 数据备份间隔（秒）
    'max_memory_usage': 0.8,      # 最大内存使用率 80%
    'max_cpu_usage': 0.9          # 最大CPU使用率 90%
}

# ============================================================================
# 环境变量设置
# ============================================================================

def setup_environment():
    """设置环境变量"""
    env_vars = {
        # 数据库配置
        'REDIS_HOST': REDIS_HOST,
        'REDIS_PORT': str(REDIS_PORT),
        'REDIS_DB': str(REDIS_DB),
        'REDIS_PASSWORD': REDIS_PASSWORD,
        'MONGODB_HOST': MONGODB_HOST,
        'MONGODB_PORT': str(MONGODB_PORT),
        'MONGODB_DATABASE': MONGODB_DATABASE,
        'MONGODB_USERNAME': MONGODB_USERNAME,
        'MONGODB_PASSWORD': MONGODB_PASSWORD,
        
        # 交易所API配置
        'OKX_API_KEY': OKX_API_KEY,
        'OKX_SECRET_KEY': OKX_SECRET_KEY,
        'OKX_PASSPHRASE': OKX_PASSPHRASE,
        'OKX_SANDBOX': str(OKX_SANDBOX).lower(),
        'BINANCE_API_KEY': BINANCE_API_KEY,
        'BINANCE_SECRET_KEY': BINANCE_SECRET_KEY,
        'BINANCE_SANDBOX': str(BINANCE_SANDBOX).lower(),
        'BITGET_API_KEY': BITGET_API_KEY,
        'BITGET_SECRET_KEY': BITGET_SECRET_KEY,
        'BITGET_PASSPHRASE': BITGET_PASSPHRASE,
        'BITGET_SANDBOX': str(BITGET_SANDBOX).lower(),
        
        # 系统配置
        'LOG_LEVEL': MONITORING_CONFIG['log_level'],
        'ENVIRONMENT': SYSTEM_CONFIG['environment'],
        'DEBUG': str(SYSTEM_CONFIG['debug']).lower(),
        'MONITORING_ENABLED': 'true',
        'ALERT_EMAIL': MONITORING_CONFIG['alert_email'],
        'ALERT_WEBHOOK': MONITORING_CONFIG['webhook_url']
    }
    
    # 设置环境变量
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ 环境变量设置完成")
    print(f"📅 配置时间: {datetime.now()}")
    print(f"🌍 环境: {SYSTEM_CONFIG['environment']}")
    print(f"🔧 调试模式: {SYSTEM_CONFIG['debug']}")

if __name__ == "__main__":
    setup_environment() 