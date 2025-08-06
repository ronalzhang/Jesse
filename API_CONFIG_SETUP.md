# API配置设置指南

## 📋 概述

本指南将帮助您正确配置Jesse+交易系统的API密钥，解决"交易所未配置"的问题。

## 🔧 配置步骤

### 1. 本地配置

#### 1.1 创建API密钥文件
- 确保 `api_keys.json` 文件已创建并包含正确的API密钥信息
- 文件位置：项目根目录下的 `api_keys.json`

#### 1.2 同步配置到数据库
```bash
# 运行配置同步脚本
python sync_api_config.py
```

#### 1.3 验证配置
- 启动Web界面：`python start_web_interface.py`
- 访问：`http://localhost:8060`
- 检查"系统配置"页面中的"交易所API"状态

### 2. 服务器配置

#### 2.1 上传配置文件
```bash
# 使用scp上传api_keys.json到服务器
scp api_keys.json root@156.236.74.200:/root/Jesse+/
```

#### 2.2 服务器端同步
```bash
# 登录服务器
sshpass -p 'Pr971V3j' ssh root@156.236.74.200

# 进入项目目录
cd /root/Jesse+

# 运行配置同步脚本
python sync_api_config.py
```

#### 2.3 重启应用
```bash
# 重启Web应用
pm2 restart high-frequency-trading
```

## 🛡️ 安全注意事项

### 1. 文件安全
- ✅ `api_keys.json` 已添加到 `.gitignore`
- ✅ 不会提交到Git仓库
- ✅ 本地和服务器分别配置

### 2. 访问控制
- 🔒 确保服务器文件权限正确
- 🔒 定期更换API密钥
- 🔒 监控API使用情况

## 🔍 故障排除

### 1. 配置未生效
```bash
# 检查配置文件是否存在
ls -la api_keys.json

# 检查配置同步是否成功
python sync_api_config.py

# 查看Web界面配置状态
# 访问：http://156.236.74.200:8060
```

### 2. 前端显示问题
- 清除浏览器缓存
- 检查浏览器控制台错误
- 确认Web应用已重启

### 3. 数据库连接问题
```bash
# 检查数据库配置
cat config/system_config.db

# 查看应用日志
pm2 logs high-frequency-trading --lines 50 --nostream
```

## 📊 配置验证

### 1. 检查项目
- [ ] `api_keys.json` 文件存在且格式正确
- [ ] 配置已同步到数据库
- [ ] Web界面显示"✅ 已配置"
- [ ] 交易所连接测试通过

### 2. 功能测试
- [ ] 多交易所价格显示正常
- [ ] 交易策略可以正常运行
- [ ] 风险控制功能正常
- [ ] 日志记录完整

## 🆘 支持

如遇到问题，请检查：
1. 配置文件格式是否正确
2. 网络连接是否正常
3. 服务器资源是否充足
4. 日志文件中的错误信息

## 📞 联系方式

如有问题，请查看：
- 项目文档：`README.md`
- 设置指南：`SETUP_GUIDE.md`
- 使用说明：`USAGE.md` 