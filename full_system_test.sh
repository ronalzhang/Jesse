#!/bin/bash
# 完整系统测试脚本

echo "======================================================================"
echo "🧪 完整系统测试"
echo "======================================================================"

# 1. 测试OKX连接
echo ""
echo "1️⃣ 测试OKX连接..."
python3 test_okx_connection.py
if [ $? -eq 0 ]; then
    echo "✅ OKX连接测试通过"
else
    echo "❌ OKX连接测试失败"
fi

# 2. 诊断进化系统
echo ""
echo "2️⃣ 诊断进化系统..."
python3 diagnose_evolution_issue.py

# 3. 检查PM2进程
echo ""
echo "3️⃣ 检查PM2进程状态..."
pm2 list | grep jesse

# 4. 检查最新回测文件
echo ""
echo "4️⃣ 检查最新回测文件..."
ls -lht data/backtest/*.json | head -5

# 5. 检查进化状态文件
echo ""
echo "5️⃣ 检查进化状态..."
if [ -f "data/evolution/evolution_state.json" ]; then
    echo "✅ 进化状态文件存在"
    echo "当前代数: $(cat data/evolution/evolution_state.json | grep -o '"current_generation": [0-9]*' | grep -o '[0-9]*')"
    echo "最佳适应度: $(cat data/evolution/evolution_state.json | grep -o '"best_fitness": [0-9.]*' | grep -o '[0-9.]*')"
else
    echo "❌ 进化状态文件不存在"
fi

# 6. 检查交易系统日志
echo ""
echo "6️⃣ 检查交易系统最新日志..."
tail -5 logs/trading_error.log | grep "获取了"

# 7. 检查Dashboard
echo ""
echo "7️⃣ 检查Dashboard状态..."
curl -s http://localhost:8060 > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Dashboard正常运行"
else
    echo "❌ Dashboard无法访问"
fi

echo ""
echo "======================================================================"
echo "✅ 测试完成"
echo "======================================================================"
