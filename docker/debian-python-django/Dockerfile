# 使用官方的 Debian 基础镜像
FROM debian

# Update the package list and install Python 3, pip, virtualenv, and other necessary tools
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Create a symbolic link to ensure `python3` and `pip3` point to Python 3.9 and pip3.9
#RUN ln -s /usr/bin/python3.9 /usr/bin/python3 && ln -s /usr/bin/pip3.9 /usr/bin/pip3

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv

# Upgrade pip in the virtual environment
RUN /opt/venv/bin/pip install --upgrade pip

# Install Django in the virtual environment
RUN /opt/venv/bin/pip install Django==4.1.*


# ============
# COPY 和 ADD 区别：COPY 只能复制本地文件，而 ADD 还可以复制远程文件或者解压缩本地文件。

# 添加宿主的文件到容器中，如当前data目录下添的文件加到home目录，除了目录本身
# ADD ./data /home

# 添加宿主的文件到容器中，如当前data目录下添的文件加到home目录，包含目录
#ADD ./data /home/data


# 该 COPY 指令将从构建上下文目录中 <源路径> 的文件/目录复制到新的一层的镜像内的 <目标路径> 位置。
# 如果 <目标路径> 以斜杠结尾，它将被视为目录，文件将被复制到该目录中。例如：COPY ./data /home
#COPY ./data /home

# =====================

# 如果应用程序使用环境变量，则可以使用该 ENV 指令在 Docker 构建中设置环境变量。例如：在容器shell中，设置itcast=python
ENV itcast=python



# 该 WORKDIR 指令为 Dockerfile 中的任何 RUN 、 CMD 、 ENTRYPOINT COPY 和 ADD 指令设置工作目录。如果不存在， WORKDIR 即使未在任何后续 Dockerfile 指令中使用，也会创建它。
# 例如：当你设置 WORKDIR /home    -->    docker /bin/bash进入的是/home为工作目录。
WORKDIR /home

#RUN source /opt/venv/bin/activate
RUN /opt/venv/bin/django-admin startproject mysite
#  CMD 指令设置用户基于此映像启动容器时运行的命令。

WORKDIR /home/mysite
# EXPOSE 指令通知 Docker 该容器在运行时将监听指定端口。例如：EXPOSE 80/udp 80/tcp
EXPOSE 12321

# 该 ENTRYPOINT 指令允许您配置一个容器，使其可执行。例如：ENTRYPOINT ["executable", "param1", "param2"]
ENTRYPOINT ["/opt/venv/bin/python", "manage.py", "runserver", "0.0.0.0:12321"]



