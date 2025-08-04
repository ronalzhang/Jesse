# 高频量化交易系统设置指南

## 🔐 敏感信息配置

为了保护您的敏感信息，以下文件已被添加到 `.gitignore` 中：

- `deploy_server.sh` - 部署脚本（包含服务器密码）
- `.env` - 环境变量文件
- `env_high_frequency.py` - 环境配置文件（包含API密钥）
- `API-KEY.md` - API密钥文档

## 📋 设置步骤

### 1. 创建部署脚本

复制部署脚本模板并填入您的服务器信息：

```bash
cp deploy_server_template.sh deploy_server.sh
```

编辑 `deploy_server.sh` 文件，修改以下配置：

```bash
SERVER_IP="your_server_ip"        # 您的服务器IP
SERVER_PASS="your_server_password" # 您的服务器密码
```

### 2. 创建环境配置文件

复制环境配置模板并填入您的API密钥：

```bash
cp env_high_frequency_template.py env_high_frequency.py
```

编辑 `env_high_frequency.py` 文件，填入您的实际配置：

- 数据库连接信息
- 交易所API密钥
- 交易参数
- 风险管理设置

### 3. 创建环境变量文件

创建 `.env` 文件（可选）：

```bash
cp env.example .env
```

编辑 `.env` 文件，添加必要的环境变量。

## 🚀 部署流程

### 本地开发

1. **配置环境**：
   ```bash
   cp env_high_frequency_template.py env_high_frequency.py
   # 编辑配置文件
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **运行测试**：
   ```bash
   python test_high_frequency.py
   ```

### 服务器部署

1. **准备部署脚本**：
   ```bash
   cp deploy_server_template.sh deploy_server.sh
   # 编辑服务器信息
   ```

2. **运行部署**：
   ```bash
   ./deploy_server.sh
   ```

## 📊 监控命令

### 本地监控

```bash
# 查看系统状态
pm2 status

# 查看日志
pm2 logs high-frequency-trading --lines 50 --nostream

# 重启应用
pm2 restart high-frequency-trading

# 停止应用
pm2 stop high-frequency-trading
```

### 远程监控

```bash
# 查看服务器状态
sshpass -p 'your_password' ssh root@your_server_ip 'pm2 status'

# 查看服务器日志
sshpass -p 'your_password' ssh root@your_server_ip 'pm2 logs high-frequency-trading --lines 50 --nostream'
```

## 🔧 配置文件说明

### deploy_server.sh
- 自动提交代码到GitHub
- 从服务器拉取最新代码
- 自动部署和重启应用

### env_high_frequency.py
- 数据库连接配置
- 交易所API配置
- 交易策略参数
- 风险管理设置
- 日志和监控配置

## ⚠️ 安全注意事项

1. **不要提交敏感文件**：
   - 确保 `deploy_server.sh` 和 `env_high_frequency.py` 不会被提交到Git
   - 这些文件包含密码和API密钥

2. **定期更新密钥**：
   - 定期更换交易所API密钥
   - 监控API使用情况

3. **备份配置**：
   - 定期备份配置文件
   - 使用安全的存储方式

## 🆘 故障排除

### 部署失败
1. 检查服务器连接
2. 验证GitHub仓库权限
3. 确认服务器上的Python环境

### 应用启动失败
1. 检查配置文件语法
2. 验证API密钥有效性
3. 查看pm2日志

### 交易异常
1. 检查交易所API状态
2. 验证账户余额
3. 查看交易日志

## 📞 支持

如有问题，请检查：
1. 配置文件是否正确
2. 网络连接是否正常
3. 服务器资源是否充足
4. 日志文件中的错误信息 