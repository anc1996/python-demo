let cons = {
  // 远程地址
  // apis:'http://192.168.20.2:8050/shop_admin'
  // 如果服务器部署，通过nginx代理，带跳转到8050（由于是uwsgi启动无法直接连接）
  apis:'http://192.168.20.2:8049/shop_admin'
}

export default cons
