import socket
import json

class RCCarClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clinet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print(f"서버 {self.host}:{self.port}에 연결되었습니다.")
        except Exception as e:
            print(f"연결 실패 : {e}")

    def send_command(self, command):
        try:
            # 명령어를 JSON 형식으로 변환
            data = json.dumps(command).encode('utf-8')
            self.client.send(data)

            # 서버로부터 응답 받기
            response = self.client