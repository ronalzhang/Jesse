#!/bin/bash

# 高频量化交易系统服务器部署脚本模板
# 请复制此文件为 deploy_server.sh 并填入您的服务器信息

# 服务器配置（请修改为您的实际信息）
SERVER_IP="156.236.74.200"
SERVER_PASS="Pr971V3j"
PROJECT_DIR="/root/Jesse+"
REPO_URL="https://github.com/ronalzhang/jesse.git"

echo "🚀 部署高频量化交易系统到服务器..."

# 检查本地文件
echo "📁 检查本地文件..."
if [ ! -f "run_high_frequency_trading.py" ]; then
    echo "❌ 主程序文件不存在"
    exit 1
fi

if [ ! -f "env_high_frequency.py" ]; then
    echo "❌ 环境配置文件不存在"
    exit 1
fi

echo "✅ 本地文件检查完成"

# 第一步：提交代码到GitHub仓库
echo "📤 提交代码到GitHub仓库..."
echo "🔍 检查Git状态..."
git status

echo "📝 添加所有更改..."
git add .

echo "💾 提交更改..."
read -p "请输入提交信息 (默认: 自动部署更新): " commit_message
commit_message=${commit_message:-"自动部署更新"}
git commit -m "$commit_message"

echo "📤 推送到GitHub仓库..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码已成功推送到GitHub仓库"
else
    echo "❌ 推送失败，请检查网络连接和SSH密钥配置"
    exit 1
fi

# 第二步：连接到服务器并部署
echo "🔗 连接到服务器..."
sshpass -p "$SERVER_PASS" ssh root@$SERVER_IP << 'EOF'

echo "📁 进入项目目录..."
cd /root/Jesse+

echo "🔍 检查Git状态..."
git status

echo "🧹 清理本地更改和未跟踪文件..."
# 备份重要文件
if [ -f "config/system_config.db" ]; then
    echo "📋 备份数据库配置..."
    cp config/system_config.db config/system_config.db.backup
fi

if [ -f "test_config.py" ]; then
    echo "📋 备份测试配置文件..."
    cp test_config.py test_config.py.backup
fi

# 重置本地更改
echo "🔄 重置本地更改..."
git reset --hard HEAD

# 清理未跟踪文件
echo "🗑️ 清理未跟踪文件..."
git clean -fd

# 设置上游分支
echo "🔗 设置上游分支..."
git branch --set-upstream-to=origin/main main

echo "📦 从GitHub仓库拉取最新代码..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ 代码更新成功"
else
    echo "❌ 代码更新失败"
    exit 1
fi


echo "🛑 停止现有进程..."
pm2 stop jesse-plus-system 2>/dev/null || true
pm2 delete jesse-plus-system 2>/dev/null || true

echo "🚀 启动Jesse+系统..."
# 使用轻量级依赖安装
source jesse_venv/bin/activate
pip install -r requirements.txt

echo "🚀 启动Jesse+系统..."
pm2 start start_web_interface.py --name "jesse-plus-system" --interpreter jesse_venv/bin/python

echo "📊 查看系统状态..."
pm2 status

echo "📝 查看启动日志..."
pm2 logs jesse-plus-system --lines 20 --nostream

echo "✅ 部署完成！"
echo ""
echo "📊 监控命令："
echo "  pm2 status                    # 查看状态"
echo "  pm2 logs jesse-plus-system --lines 50 --nostream  # 查看日志"
echo "  pm2 restart jesse-plus-system  # 重启"
echo "  pm2 stop jesse-plus-system     # 停止"
echo ""

EOF

echo "✅ 服务器部署完成！"
echo ""
echo "🌐 服务器信息："
echo "  IP: $SERVER_IP"
echo "  项目目录: $PROJECT_DIR"
echo "  应用名称: jesse-plus-system"
echo "  仓库地址: $REPO_URL"
echo ""
echo "📊 远程监控："
echo "  sshpass -p '$SERVER_PASS' ssh root@$SERVER_IP 'pm2 status'"
echo "  sshpass -p '$SERVER_PASS' ssh root@$SERVER_IP 'pm2 logs jesse-plus-system --lines 50 --nostream'" 