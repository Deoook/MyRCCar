import socket
import json
import threading
import time

class RCCarServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.is_running = True
        
        # 모터 제어 함수들을 딕셔너리로 매핑 (실제 구현 시 GPIO 제어 코드로 대체)
        self.command_handlers = {
            "forward": self.move_forward,
            "backward": self.move_backward,
            "left": self.turn_left,
            "right": self.turn_right,
            "stop": self.stop
        }
    
    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"서버가 {self.host}:{self.port}에서 시작되었습니다.")
            
            # 클라이언트 연결 수락 스레드 시작
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # 메인 스레드는 사용자 입력을 기다림
            while self.is_running:
                command = input("서버 명령 (quit으로 종료): ")
                if command.lower() == "quit":
                    self.is_running = False
                    break
                    
        except Exception as e:
            print(f"서버 오류: {e}")
        finally:
            self.close()
    
    def accept_connections(self):
        while self.is_running:
            try:
                client_socket, client_address = self.server.accept()
                print(f"클라이언트 {client_address}가 연결되었습니다.")
                
                self.clients.append(client_socket)
                
                # 각 클라이언트를 위한 스레드 시작
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.is_running:
                    print(f"연결 수락 오류: {e}")
                break
    
    def handle_client(self, client_socket, client_address):
        try:
            while self.is_running:
                # 클라이언트로부터 데이터 수신
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"{client_address}로부터 수신: {data}")
                
                try:
                    # JSON 데이터 파싱
                    command_data = json.loads(data)
                    command = command_data.get("command")
                    speed = command_data.get("speed", 50)
                    
                    # 명령어 처리
                    response = self.process_command(command, speed)
                    
                    # 응답 전송
                    client_socket.send(response.encode('utf-8'))
                except json.JSONDecodeError:
                    client_socket.send("잘못된 명령 형식입니다.".encode('utf-8'))
                
        except Exception as e:
            print(f"클라이언트 처리 오류: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"클라이언트 {client_address} 연결이 종료되었습니다.")
    
    def process_command(self, command, speed):
        if command in self.command_handlers:
            return self.command_handlers[command](speed)
        else:
            return f"알 수 없는 명령: {command}"
    
    # 모터 제어 함수들 (실제로는 GPIO 핀을 제어하는 코드로 대체)
    def move_forward(self, speed):
        print(f"RC카가 전진합니다. 속도: {speed}")
        # 여기에 실제 모터 제어 코드 추가
        return f"전진 명령 처리됨, 속도: {speed}"
    
    def move_backward(self, speed):
        print(f"RC카가 후진합니다. 속도: {speed}")
        # 여기에 실제 모터 제어 코드 추가
        return f"후진 명령 처리됨, 속도: {speed}"
    
    def turn_left(self, speed):
        print(f"RC카가 좌회전합니다. 속도: {speed}")
        # 여기에 실제 모터 제어 코드 추가
        return f"좌회전 명령 처리됨, 속도: {speed}"
    
    def turn_right(self, speed):
        print(f"RC카가 우회전합니다. 속도: {speed}")
        # 여기에 실제 모터 제어 코드 추가
        return f"우회전 명령 처리됨, 속도: {speed}"
    
    def stop(self, speed=0):
        print("RC카가 정지합니다.")
        # 여기에 실제 모터 제어 코드 추가
        return "정지 명령 처리됨"
    
    def close(self):
        self.is_running = False
        
        # 모든 클라이언트 연결 종료
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        self.clients.clear()
        
        # 서버 소켓 종료
        try:
            self.server.close()
        except:
            pass
        
        print("서버가 종료되었습니다.")

if __name__ == "__main__":
    # 서버 생성 및 시작
    server = RCCarServer(port=5000)
    server.start()