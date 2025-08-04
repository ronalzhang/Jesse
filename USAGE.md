# Jesse+ 使用指南

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目（如果从GitHub）
git clone <your-repo-url>
cd Jesse+

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑.env文件，配置API密钥等
```

### 2. 运行方式

#### 方式一：命令行运行（推荐）
```bash
# 运行主系统
python run_ai_enhanced_jesse.py

# 运行Web界面
python start_web.py
# 或
python run_ai_enhanced_jesse.py web
```

#### 方式二：直接运行Web界面
```bash
streamlit run web/app.py --server.port 8060
```

### 3. 访问Web界面

启动后访问：`http://localhost:8060`

## 📊 Web界面功能

### 主要功能模块

1. **📊 实时监控**
   - 价格走势图
   - 交易量统计
   - 策略性能对比
   - 实时市场数据
   - 系统运行状态

2. **💰 多交易所价格**
   - 多交易所价格对比图表
   - 实时价差分析
   - 套利机会检测
   - 详细价格信息表格
   - 跨交易所套利策略说明

3. **🤖 AI分析过程**
   - 分析步骤时间线
   - AI模型状态监控
   - 实时分析结果
   - 情绪分析雷达图
   - 模型准确率跟踪

4. **🧠 决策过程**
   - 决策流程可视化
   - 决策因素权重分析
   - 当前决策详情
   - 历史决策记录
   - 置信度分析

5. **🧬 策略进化**
   - 进化时间线
   - 遗传算法进化过程
   - 策略参数优化
   - 强化学习训练状态
   - 性能对比分析

6. **📈 交易记录**
   - 历史交易记录
   - 收益统计
   - 胜率分析
   - 风险指标
   - AI置信度分析

7. **⚙️ 系统配置**
   - 数据库配置
   - 交易所API配置
   - AI模型参数
   - 风险控制设置

8. **📋 日志**
   - 实时系统日志
   - 日志级别过滤
   - 日志搜索功能

### 侧边栏控制面板

- **系统控制**: 启动/停止系统
- **监控设置**: 显示AI分析过程、决策过程、策略进化
- **策略管理**: 选择活跃策略
- **AI配置**: 启用AI增强、预测周期、置信度阈值
- **风险控制**: 设置仓位和止损
- **自动刷新**: 实时数据更新

## 🔧 配置说明

### 环境变量配置 (.env)

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=27017
DB_NAME=jesse_plus

# 交易所API
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

# AI模型配置
LSTM_UNITS=128
TRANSFORMER_LAYERS=6
LEARNING_RATE=0.001

# 风险控制
MAX_DRAWDOWN=10
DAILY_LOSS_LIMIT=5
```

### 策略配置

系统包含以下策略：
- **AI增强策略**: 多策略集成+AI分析
- **移动平均线交叉策略**: 经典技术分析
- **RSI策略**: 相对强弱指数
- **MACD策略**: 移动平均收敛发散
- **布林带策略**: 波动率策略

## 📈 监控指标

### 关键指标
- **系统状态**: 运行/停止状态
- **活跃策略**: 当前运行的策略数量
- **今日收益**: 当日收益率
- **总资产**: 账户总资产价值

### 性能指标
- **收益率**: 各策略的收益率
- **胜率**: 交易成功率
- **最大回撤**: 最大亏损幅度
- **夏普比率**: 风险调整后收益

## 🛡️ 风险控制

### 自动风险控制
- **最大回撤限制**: 防止过度亏损
- **日损失限制**: 控制每日最大损失
- **仓位管理**: 自动调整仓位大小
- **止损机制**: 自动止损保护

### 手动风险控制
- **策略选择**: 可选择启用/禁用特定策略
- **参数调整**: 实时调整风险参数
- **紧急停止**: 一键停止所有交易

## 🔍 故障排除

### 常见问题

1. **Web界面无法启动**
   ```bash
   # 检查streamlit是否安装
   pip install streamlit
   
   # 检查端口是否被占用
   lsof -i :8080
   ```

2. **数据库连接失败**
   ```bash
   # 检查MongoDB服务
   sudo systemctl status mongod
   
   # 检查连接配置
   cat .env
   ```

3. **API连接失败**
   ```bash
   # 检查网络连接
   ping api.binance.com
   
   # 检查API密钥
   echo $BINANCE_API_KEY
   ```

### 日志查看

```bash
# 查看系统日志
tail -f logs/jesse_plus.log

# 查看错误日志
grep ERROR logs/jesse_plus.log
```

## 🚀 部署到服务器

### 使用PM2部署

```bash
# 安装PM2
npm install -g pm2

# 启动Web界面
pm2 start start_web.py --name jesse-plus-web --interpreter python3

# 启动主系统
pm2 start run_ai_enhanced_jesse.py --name jesse-plus-main --interpreter python3

# 查看状态
pm2 status

# 查看日志
pm2 logs jesse-plus-web
```

### 使用Docker部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["streamlit", "run", "web/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
```

## 📞 技术支持

- **GitHub Issues**: 提交问题和建议
- **文档**: 查看详细技术文档
- **社区**: 加入用户交流群

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✅ 基础AI增强功能
- ✅ Web界面开发
- ✅ 多策略支持
- ✅ 风险控制系统
- ✅ 实时监控功能 