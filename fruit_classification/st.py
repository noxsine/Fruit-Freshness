import socket
import os
import Detect_Color as DC
import cv2
import retrain_model_classifier as rmc


#ima = "/home/heisenberg/桌面/py/s/test1.jpg"



sk = socket.socket()
print(sk)
address = ('0.0.0.0', 8000)
sk.bind(address)  # 将本地地址与一个socket绑定在一起
sk.listen(3)  # 最多允许有3个客户称呼
print('waiting........ ')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 26:11,当前目录
while 1:
    conn, addr = sk.accept()
    while 1:
        client = conn
        data = conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
        # client.send("HTTP/1.1 200 OK\r\n\r\n".encode("utf8"))


        cmd, filename, filesize = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
        # filesize = os.stat(data)
        path = os.path.join(BASE_DIR, 'test', filename)
        filesize = int(filesize)

        f = open(path, 'ab')
        has_receive = 0
        while has_receive != filesize:
            data = conn.recv(1024)  # 第二次获取请求，这次获取的就是传递的具体内容了，1024为文件发送的单位
            f.write(data)
            has_receive += len(data)

        f.close()
        print('Success')
        path = "/home/heisenberg/桌面/image_classification/test/test.jpg"
        result = rmc.fruit_c(path)  #调用识别函数
        client.send(result.encode("utf8"))  #发送结果到客户端
        if os.path.exists(path):
    #删除文件
            os.remove(path)
    #os.unlink(my_file)
        else:
            print ('no such file:%s'%path)
