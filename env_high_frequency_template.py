# 高频量化交易系统环境配置模板
# 请复制此文件为 env_high_frequency.py 并填入您的实际配置

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'jesse_trading',
    'user': 'your_db_user',
    'password': 'your_db_password'
}

# 交易所API配置
EXCHANGE_CONFIG = {
    'binance': {
        'api_key': 'your_binance_api_key',
        'api_secret': 'your_binance_api_secret',
        'sandbox': True  # 测试环境
    },
    'okx': {
        'api_key': 'your_okx_api_key',
        'api_secret': 'your_okx_api_secret',
        'passphrase': 'your_okx_passphrase',
        'sandbox': True  # 测试环境
    }
}

# 交易配置
TRADING_CONFIG = {
    'max_position_size': 0.1,  # 最大仓位比例
    'stop_loss_percentage': 0.02,  # 止损百分比
    'take_profit_percentage': 0.04,  # 止盈百分比
    'max_open_trades': 5,  # 最大同时开仓数
    'min_balance': 100  # 最小余额
}

# 策略配置
STRATEGY_CONFIG = {
    'high_frequency': {
        'enabled': True,
        'timeframe': '1m',
        'symbols': ['BTC/USDT', 'ETH/USDT'],
        'parameters': {
            'rsi_period': 14,
            'rsi_overbought': 70,
            'rsi_oversold': 30,
            'ma_fast': 10,
            'ma_slow': 20
        }
    },
    'arbitrage': {
        'enabled': True,
        'min_profit_threshold': 0.001,  # 最小利润阈值
        'max_execution_time': 30  # 最大执行时间（秒）
    }
}

# 风险管理配置
RISK_CONFIG = {
    'max_daily_loss': 0.05,  # 最大日损失
    'max_weekly_loss': 0.15,  # 最大周损失
    'max_monthly_loss': 0.30,  # 最大月损失
    'emergency_stop': True,  # 紧急停止
    'position_sizing': 'fixed'  # 仓位大小策略
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'file': 'logs/high_frequency_trading.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# 监控配置
MONITORING_CONFIG = {
    'enabled': True,
    'metrics_interval': 60,  # 指标收集间隔（秒）
    'alert_threshold': 0.05,  # 告警阈值
    'webhook_url': 'your_webhook_url'  # 告警webhook
}

# AI增强配置
AI_CONFIG = {
    'enabled': True,
    'model_path': 'models/',
    'prediction_confidence': 0.7,
    'retrain_interval': 24 * 60 * 60,  # 24小时
    'max_predictions': 100
}

# 系统配置
SYSTEM_CONFIG = {
    'debug_mode': False,
    'backtest_mode': False,
    'live_trading': True,
    'auto_restart': True,
    'restart_interval': 3600  # 1小时
} 