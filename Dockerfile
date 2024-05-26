# Sử dụng Node.js image chính thức từ Docker Hub
FROM node:18

# Đặt biến môi trường để không tạo thông báo chown (sẽ giải thích sau)
ENV NPM_CONFIG_LOGLEVEL warn

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Sao chép file package.json và package-lock.json vào thư mục làm việc
COPY package*.json ./

# Cài đặt các dependencies
RUN npm install

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng mà ứng dụng của bạn sẽ chạy
EXPOSE 3000

# Khởi chạy ứng dụng
CMD ["node", "server.js"]
