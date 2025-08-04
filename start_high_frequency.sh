#!/bin/bash

# 高频量化交易系统启动脚本
# 目标：日化收益率3%-30%

echo "🚀 启动高频量化交易系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p logs data/reviews

# 检查环境配置文件
if [ ! -f ".env" ]; then
    echo "📋 复制环境配置文件..."
    cp env_high_frequency.py .env
    echo "✅ 环境配置文件已创建"
else
    echo "✅ 环境配置文件已存在"
fi

# 检查依赖包
echo "📦 检查依赖包..."
python3 -c "import jesse, ccxt, pandas, numpy, schedule" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖包..."
    pip3 install -r requirements.txt
else
    echo "✅ 依赖包已安装"
fi

# 检查配置文件
echo "🔧 检查配置文件..."
if [ ! -f "config/exchange_config.py" ]; then
    echo "❌ 配置文件不存在，请检查项目结构"
    exit 1
fi

# 启动系统
echo "🎯 启动高频量化交易系统..."
echo "📊 目标：日化收益率3%-30%"
echo "⏰ 持仓时间：30秒-1小时"
echo "🤖 AI每日复盘：23:59"
echo ""

# 启动交易系统
python3 run_high_frequency_trading.py

echo ""
echo "✅ 高频量化交易系统已启动"
echo "📊 查看日志：tail -f logs/high_frequency_trading.log"
echo "📁 查看复盘：ls data/reviews/" 