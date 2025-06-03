#!/bin/bash
set -e

# 显示密钥轮换信息
echo "开始轮换系统密钥..."
echo "注意：轮换密钥会需要所有当前用户重新登录"
echo ""

# 加载当前环境变量
source .env

# 生成新密钥
echo "生成新密钥..."
NEW_API_SECRET=$(openssl rand -base64 32)
NEW_JWT_SECRET=$(openssl rand -base64 32)
NEW_FRONTEND_API_KEY=$(openssl rand -base64 32)

# 停止服务
echo "停止服务..."
docker-compose stop

# 更新容器环境变量
echo "更新服务配置..."
docker-compose run --rm backend bash -c \
  "sed -i \"s/API_SECRET_KEY=.*/API_SECRET_KEY=$NEW_API_SECRET/\" .env && \
   sed -i \"s/JWT_SECRET=.*/JWT_SECRET=$NEW_JWT_SECRET/\" .env && \
   sed -i \"s/FRONTEND_API_KEY=.*/FRONTEND_API_KEY=$NEW_FRONTEND_API_KEY/\" frontend/.env.production"

# 更新环境变量文件
echo "更新环境变量文件..."
sed -i "s/API_SECRET_KEY=.*/API_SECRET_KEY=$NEW_API_SECRET/" .env
sed -i "s/JWT_SECRET=.*/JWT_SECRET=$NEW_JWT_SECRET/" .env
sed -i "s/FRONTEND_API_KEY=.*/FRONTEND_API_KEY=$NEW_FRONTEND_API_KEY/" .env

# 重新构建并启动服务
echo "重新启动服务..."
docker-compose up -d --build

# 完成信息
echo ""
echo "✅ 密钥轮换完成！"
echo "新API密钥: $NEW_API_SECRET"
echo "新JWT密钥: $NEW_JWT_SECRET"
echo "新前端API密钥: $NEW_FRONTEND_API_KEY"
echo ""
echo "服务已重新启动，所有用户需要重新登录。"