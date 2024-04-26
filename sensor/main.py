import threading
import time
from socket import *
import numpy as np
import requests

prev_sensor = np.zeros(8)

class ReceiveThread(threading.Thread):
    def __init__(self, PORT=12345):
        threading.Thread.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        # line information
        self.HOST = "127.0.0.1"
        self.PORT = PORT
        self.BUFSIZE = 1024
        self.ADDR = (gethostbyname(self.HOST), self.PORT)
        # bind
        self.udpServSock = socket(AF_INET, SOCK_DGRAM)
        self.udpServSock.bind(self.ADDR)
        self.received = False

    def get_data(self):
        data_ary = []
        for i in reversed(range(8)):
            num = int(str(self.data[i*8:(i+1)*8]))
            data_ary.append(num / 167.0 / 10000)
        self.received = False
        return data_ary
    
    def run(self):
        while True:
            try:
                data, self.addr = self.udpServSock.recvfrom(self.BUFSIZE)
                self.data = data.decode()
                self.received = True
            except:
                pass

if __name__ == '__main__':
    th = ReceiveThread()
    th.setDaemon(True)
    th.start()

    is_initial = True
    last_data = -1

    while True:
        if not th.data:
            break

        if th.received:
            sensor_data = th.get_data()[0] #TODO: 0番目のセンサデータを取得(センサーが差されている場所によって変更する)
            if is_initial:
                is_initial = False
                last_data = sensor_data
                time.sleep(1)
                continue

            if last_data < 0.05 and sensor_data > 0.05: # 明るい -> 暗いのとき
                requests.delete("https://xxxx.execute-api.ap-northeast-1.amazonaws.com/Prod") #TODO: API GatewayのURLを指定
            print(sensor_data)
            last_data = sensor_data

        time.sleep(1)