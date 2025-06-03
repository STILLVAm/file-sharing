# 构建阶段
FROM node:18 as builder

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY package*.json ./
RUN npm install

# 复制源码
COPY . .

# 构建生产环境应用
RUN npm run build

# 运行阶段
FROM nginx:1.24-alpine

# 复制构建好的应用
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制自定义nginx配置
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]