# Jesse+ - AI增强的加密货币量化交易系统

## 🚀 项目简介

Jesse+ 是基于Jesse框架的AI增强加密货币量化交易系统，结合了Jesse的低资源占用、完全自动化优势，以及深度AI参与的市场分析、策略进化和预测能力。

## ✨ 核心特性

### 🎯 Jesse核心优势
- **低资源占用**: 优化的内存和CPU使用
- **完全自动化**: 无需人工干预的全自动运行
- **多交易所支持**: 支持100+加密货币交易所
- **专门优化**: 针对加密货币市场专门设计

### 🤖 AI增强功能
- **AI市场分析**: 深度学习驱动的市场情绪分析
- **AI策略进化**: 强化学习和遗传算法优化
- **AI市场预测**: LSTM和Transformer模型预测
- **AI决策制定**: 智能交易信号生成

## 🏗️ 系统架构

```
Jesse+/
├── 📄 README.md                    # 项目说明文档
├── 📄 requirements.txt             # Python依赖包
├── 📄 setup.py                    # 安装脚本
├── 📄 env.example                 # 环境变量示例
├── 📄 run_ai_enhanced_jesse.py   # 主运行文件
│
├── 📁 config/                     # 配置文件
│   ├── database_config.py         # 数据库配置
│   ├── exchange_config.py         # 交易所配置
│   └── ai_config.py              # AI模型配置
│
├── 📁 ai_modules/                 # AI增强模块
│   ├── ai_enhancer.py            # AI增强器主类
│   ├── market_analyzer.py        # 市场分析器
│   ├── price_predictor.py        # 价格预测器
│   ├── strategy_evolver.py       # 策略进化器
│   └── __init__.py
│
├── 📁 jesse_core/                 # Jesse核心模块
│   ├── jesse_manager.py          # Jesse管理器
│   └── __init__.py
│
├── 📁 strategies/                 # 交易策略
│   ├── base_strategy.py          # 基础策略类
│   ├── ma_crossover_strategy.py  # 移动平均线交叉策略
│   ├── rsi_strategy.py           # RSI策略
│   ├── macd_strategy.py          # MACD策略
│   ├── bollinger_strategy.py     # 布林带策略
│   ├── ai_enhanced_strategy.py   # AI增强策略
│   └── __init__.py
│
├── 📁 utils/                      # 工具模块
│   ├── logging_manager.py        # 日志管理
│   ├── data_processor.py         # 数据处理
│   ├── helpers.py                # 辅助工具
│   └── __init__.py
│
├── 📁 data/                       # 数据管理
│   ├── data_manager.py           # 数据管理器
│   ├── market_data_collector.py  # 市场数据收集器
│   └── __init__.py
│
├── 📁 models/                     # AI模型
│   ├── model_manager.py          # 模型管理器
│   ├── lstm_model.py             # LSTM模型
│   ├── transformer_model.py      # Transformer模型
│   ├── garch_model.py            # GARCH模型
│   └── __init__.py
│
├── 📁 monitoring/                 # 监控系统
│   ├── system_monitor.py         # 系统监控
│   └── __init__.py
│
├── 📁 tradingagents/              # 交易代理
│   ├── __init__.py
│   └── �� utils/
│       ├── __init__.py
│       └── logging_manager.py
│
├── 📁 data/                       # 数据存储目录
├── 📁 models/                     # 模型存储目录
├── 📁 logs/                       # 日志目录
└── 📁 config/                     # 配置目录
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 初始化配置
```bash
python setup.py
```

### 3. 运行系统
```bash
python run_ai_enhanced_jesse.py
```

核心功能
1. AI增强功能
✅ AI市场分析 - 深度学习驱动的市场情绪分析
✅ AI策略进化 - 强化学习和遗传算法优化
✅ AI市场预测 - LSTM和Transformer模型预测
✅ AI决策制定 - 智能交易信号生成
2. 交易策略
✅ 移动平均线交叉策略 - 经典技术分析策略
✅ RSI策略 - 相对强弱指数策略
✅ MACD策略 - 移动平均收敛发散策略
✅ 布林带策略 - 波动率策略
✅ AI增强策略 - 多策略集成+AI分析
3. 数据管理
✅ 市场数据收集 - 支持100+交易所
✅ 数据清洗处理 - 自动数据质量保证
✅ 技术指标计算 - 完整的TA-Lib指标库
✅ 数据存储管理 - 本地+数据库存储
4. AI模型
✅ LSTM模型 - 时间序列预测
✅ Transformer模型 - 注意力机制预测
✅ GARCH模型 - 波动率预测
✅ 模型管理器 - 训练、保存、加载
5. 系统监控
✅ 性能监控 - 实时策略性能跟踪
✅ 风险控制 - 自动风险管理系统
✅ 日志管理 - 彩色日志+文件记录
✅ 系统状态 - 健康检查和报警
🔧 配置系统
1. 数据库配置 (config/database_config.py)
Redis缓存配置
MongoDB数据存储配置
集合名称管理
2. 交易所配置 (config/exchange_config.py)
支持100+交易所
API密钥管理
速率限制控制
交易对配置
3. AI配置 (config/ai_config.py)
LSTM模型参数
Transformer模型参数
GARCH模型参数
强化学习配置
遗传算法配置


## 📊 功能对比

| 特性 | 原始Jesse | Jesse+ | 其他系统 |
|------|-----------|--------|----------|
| 资源占用 | ✅ 低 | ✅ 低 | ❌ 高 |
| 完全自动化 | ✅ 100% | ✅ 100% | ⚠️ 部分 |
| AI市场分析 | ❌ 无 | ✅ 深度 | ✅ 有 |
| AI策略进化 | ⚠️ 基础 | ✅ 高级 | ✅ 有 |
| AI市场预测 | ❌ 无 | ✅ 准确 | ✅ 有 |
| 多交易所支持 | ✅ 100+ | ✅ 100+ | ✅ 有 |
| 加密货币优化 | ✅ 专门 | ✅ 专门 | ⚠️ 通用 |

## 🤖 AI模块详解

### 1. AI市场分析器
- 新闻情绪分析
- 社交媒体情绪分析
- 技术指标分析
- 市场情绪综合评估

### 2. AI市场预测器
- LSTM价格预测
- Transformer趋势预测
- GARCH波动率预测
- 集成预测模型

### 3. AI策略进化器
- 遗传算法优化
- 强化学习优化
- 神经网络进化
- 多目标优化

## 📈 监控系统

- 实时性能监控
- 风险控制
- 策略评估
- 自动报警

## 🔧 配置说明

详细配置请参考 `config/` 目录下的配置文件。

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
