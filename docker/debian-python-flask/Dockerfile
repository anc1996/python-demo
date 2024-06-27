# 使用官方的 Debian 基础镜像
FROM debian:latest

# 更新包列表并安装 Python 3、pip、虚拟环境等必要工具
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# 创建并激活虚拟环境
RUN python3 -m venv /opt/venv

# 安装 Flask 和其他依赖
RUN /opt/venv/bin/pip install flask

# 设置工作目录
WORKDIR /home

# 将应用程序文件复制到容器中
COPY hello.py /home/

# 设置环境变量和启动命令
ENV FLASK_APP=hello
EXPOSE 18000
CMD ["/opt/venv/bin/flask", "run", "--host=0.0.0.0", "--port=18000"]


# docker build -t flask-demo .
# docker run -dit -p 18000:18000 --name flask-demo flask-demo
