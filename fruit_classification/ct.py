import socket
import os

sk = socket.socket()
print(sk)

address = ('127.0.0.1', 8000)
sk.connect(address)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

while True:
    inp = input('>>>>>>>>')  # post|test.png
    #cmd = "post"
    #cmd, path = inp.split('|')  # 拿到post，以及文件11.jpg
    path = inp

    path = os.path.join(BASE_DIR, path)

    filename = os.path.basename(path)

    file_size = os.stat(path).st_size

    file_info = 'post|%s|%s' % (filename, file_size)  # split获取字符串的信息       以此方式打包，依次为   cmd/name/size
    sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息

    f = open(path, 'rb')
    has_sent = 0
    while has_sent != file_size:
        data = f.read(1024)
        sk.sendall(data)  # 发送真实数据
        has_sent += len(data)

    f.close()
    print('上传成功')
    accept_data = sk.recv(1024)
    print(str(accept_data, encoding="utf8"))