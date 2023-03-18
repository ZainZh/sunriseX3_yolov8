# aiexpress_webserver

里面包含nginx服务以及与ai-express统一web客户端配套的web页面。

PC web页面基于web socket协议与X3侧WebDisplayPlugin通信，获得WebDisplayPlugin发送来的jpg图像与序列化后的感知结果，对感知结果进行反序列化，然后渲染显示。

# 使用
1、拷贝此文件夹到设备上
2、启动服务：./sbin/nginx -p .
3、访问：
    web展示端：http://IP
