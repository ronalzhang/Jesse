#!/bin/bash

# 前端优化部署脚本
# 用于将最新的前端优化部署到服务器

echo "🚀 开始部署前端优化到服务器..."
echo "================================"

# 服务器信息（从.cursor/rules/server-ip-pem-rules.mdc读取）
SERVER_IP="47.236.101.47"
SERVER_USER="root"
PEM_FILE="$HOME/.ssh/aliyun-hk.pem"
PROJECT_DIR="/root/Jesse+"

echo "📡 服务器信息:"
echo "   IP: $SERVER_IP"
echo "   用户: $SERVER_USER"
echo "   项目目录: $PROJECT_DIR"
echo ""

# 检查PEM文件
if [ ! -f "$PEM_FILE" ]; then
    echo "❌ 错误: PEM文件不存在: $PEM_FILE"
    echo "💡 请确保PEM文件路径正确"
    exit 1
fi

echo "✅ PEM文件检查通过"
echo ""

# 连接到服务器并执行部署
echo "🔄 连接到服务器并拉取最新代码..."
ssh -i "$PEM_FILE" "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
    set -e
    
    echo "📂 进入项目目录..."
    cd /root/Jesse+
    
    echo "🔄 拉取最新代码..."
    git pull origin main
    
    echo "📦 检查依赖..."
    # 如果有新的Python依赖，可以在这里安装
    # pip install -r requirements.txt
    
    echo "🔍 检查新文件..."
    ls -la web/static/
    
    echo "🔄 重启Streamlit服务..."
    # 查找并停止现有的Streamlit进程
    pkill -f "streamlit run web/app.py" || true
    
    # 等待进程完全停止
    sleep 2
    
    # 启动新的Streamlit进程（后台运行）
    nohup streamlit run web/app.py --server.port 8501 --server.address 0.0.0.0 > /root/Jesse+/logs/streamlit.log 2>&1 &
    
    echo "✅ Streamlit服务已重启"
    
    # 显示进程状态
    echo ""
    echo "📊 服务状态:"
    ps aux | grep streamlit | grep -v grep || echo "⚠️ 未找到Streamlit进程"
    
    echo ""
    echo "✅ 部署完成！"
    echo "🌐 访问地址: http://47.236.101.47:8501"
ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ 部署成功完成！"
    echo ""
    echo "🌐 访问地址:"
    echo "   http://47.236.101.47:8501"
    echo ""
    echo "📋 查看日志:"
    echo "   ssh -i $PEM_FILE $SERVER_USER@$SERVER_IP 'tail -f /root/Jesse+/logs/streamlit.log'"
    echo ""
    echo "💡 提示:"
    echo "   - 刷新浏览器查看新的UI设计"
    echo "   - 访问'系统概览'页面查看翻牌效果"
    echo "   - 观察数字变化时的动画效果"
    echo ""
else
    echo ""
    echo "================================"
    echo "❌ 部署失败！"
    echo "💡 请检查:"
    echo "   1. 服务器连接是否正常"
    echo "   2. PEM文件权限是否正确"
    echo "   3. 服务器上的项目目录是否存在"
    echo ""
fi
