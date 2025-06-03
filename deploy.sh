
### deploy.sh
```bash
#!/bin/bash
set -e

# 显示部署信息
echo "开始部署个人文件云存储系统..."
echo "系统要求："
echo " - Docker       ✓"
echo " - 4GB+ 内存    ✓"
echo " - 100GB+ 存储  ✓"
echo ""

# 定义环境变量文件路径
ENV_FILE=".env"

# 创建环境变量文件
if [ ! -f "$ENV_FILE" ]; then
  echo "创建环境变量文件..."
  cat > $ENV_FILE <<EOL
# 系统配置
# 管理员凭据
ADMIN_USER="admin"
ADMIN_PASSWORD=$(openssl rand -base64 12)

# API密钥
API_SECRET_KEY=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -base64 32)
FRONTEND_API_KEY=$(openssl rand -base64 32)

# 上传设置
MAX_FILE_SIZE=10737418240  # 10GB
CHUNK_SIZE=104857600      # 100MB
ALLOWED_EXTENSIONS="txt,pdf,png,jpg,jpeg,gif,doc,docx,zip,mp4,mov"

# 数据库配置 (可选)
DB_HOST="db"
DB_NAME="file_sharing"
DB_USER="fileadmin"
DB_PASSWORD=$(openssl rand -base64 16)
EOL
fi

# 加载环境变量
source $ENV_FILE

# 打印部署配置
echo "部署配置:"
echo " - 管理员用户: $ADMIN_USER"
echo " - 管理员密码: $ADMIN_PASSWORD"
echo " - API密钥: 已生成"
echo " - 最大文件大小: $(($MAX_FILE_SIZE/1024/1024/1024))GB"
echo " - 分片大小: $(($CHUNK_SIZE/1024/1024))MB"
echo ""

# 创建上传目录
echo "创建上传目录并设置权限..."
mkdir -p backend/uploads
sudo chown -R 1000:1000 backend/uploads
sudo chmod -R 770 backend/uploads

# 检查Docker服务状态
if ! systemctl is-active --quiet docker; then
  echo "启动Docker服务..."
  sudo systemctl start docker
fi

# 检查Docker权限
if ! docker ps &> /dev/null; then
  echo "当前用户($USER)无法运行Docker命令，请添加到docker组并退出重新登录"
  exit 1
fi

# 构建Docker镜像
echo "构建Docker镜像..."
docker-compose build --no-cache

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待服务初始化
echo "等待服务启动..."
sleep 15

# 检查服务状态
echo "服务状态检查:"
docker-compose ps

# 设置防火墙
echo "配置防火墙..."
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 创建备份脚本
echo "创建备份脚本..."
sudo tee /usr/local/bin/backup-files <<EOF > /dev/null
#!/bin/bash
DATE=\$(date +%Y%m%d)
BACKUP_DIR="/opt/backups"
TARGET_DIR="/opt/file-sharing/backend/uploads"

mkdir -p \$BACKUP_DIR
tar -czf "\$BACKUP_DIR/files-\$DATE.tar.gz" -C "\$TARGET_DIR" .
find \$BACKUP_DIR -name "files-*.tar.gz" -mtime +7 -delete
echo "文件备份完成: files-\$DATE.tar.gz"
EOF

sudo chmod +x /usr/local/bin/backup-files

# 添加每日备份任务
echo "添加每日备份任务..."
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-files") | crontab -

# 完成信息
echo ""
echo "🎉 部署成功！"
echo "访问地址: http://$(curl -s ifconfig.me)"
echo ""
echo "登录信息:"
echo " - 用户名: $ADMIN_USER"
echo " - 密码: $ADMIN_PASSWORD"
echo ""
echo "管理命令:"
echo " - 停止服务: docker-compose down"
echo " - 启动服务: docker-compose up -d"
echo " - 查看日志: docker-compose logs -f"
echo " - 备份文件: backup-files"
echo " - 轮换密钥: ./rotate-keys.sh"