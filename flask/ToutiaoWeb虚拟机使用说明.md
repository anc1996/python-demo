# ToutiaoWeb虚拟机使用说明

- CentOS7.2
- 黑窗口 无GNOME
- 虚拟机NAT   xshell 免费  windows远程连接工具
- ssh python@自己的ip地址
- 用户名 密码
  - 系统
    - root  -> chuanzhi
    - python -> chuanzhi
  - MySQL
    - root -> mysql
- 端口
  - MySQL (mariadb)
    - master -> 3306
    - slave -> 8306   (mysql -uroot -p -h 127.0.0.1 --port=8306)
  - Redis
    - cluster  -> 7000  7001 7002 7003 7004 7005
    - master & slave -> 6380 6381
    - sentinel -> 26380 26381 26382
  - Elasticsearch 5
    - 9200
- Python 虚拟环境 
  - workon toutiao
- 关机 sudo shutdown now
- 重启 reboot