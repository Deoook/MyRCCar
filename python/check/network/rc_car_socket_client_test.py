# 이코드는 연결 확인을 체크하기 위한 코드
# client : 노트북
import socket
import json

class RCCarClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
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
            response = self.client.recv(1024).decode('utf-8')
            print(f"서버 응답: {response}")
            return response
        except Exception as e:
            print(f"명령어 전송 실패: {e}")
            
    def close(self):
        self.client.close()
        print("연결이 종료되었습니다.")

# 사용 예시
if __name__ == "__main__":
    # 서버 IP와 포트 설정
    SERVER_IP = "192.168.0.145"  # 실제 서버 IP로 변경하세요
    PORT = 5000
    
    # 클라이언트 생성 및 연결
    rc_car = RCCarClient(SERVER_IP, PORT)
    rc_car.connect()
    
    try:
        while True:
            # 예시 명령어
            command = input("명령어 입력 (forward/backward/left/right/stop): ")
            
            if command == "quit":
                break
                
            # 명령어와 추가 파라미터를 딕셔너리로 만들기
            command_data = {
                "command": command,
                "speed": 50  # 속도값 예시
            }
            
            # 명령어 전송
            response = rc_car.send_command(command_data)
            
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
    finally:
        rc_car.close()

