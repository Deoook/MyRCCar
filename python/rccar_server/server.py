# server.py
import socket
import json
import threading
import signal
import sys
import time
import importlib
import config

# 설정에 따라 적절한 모터 제어 모듈 가져오기
if config.MODE == "FOUR_WHEEL":
   from motor_control.four_wheel import init_gpio, cleanup_gpio, execute_command, motor_stop
elif config.MODE == "TWO_WHEEL":
   from motor_control.two_wheel import init_gpio, cleanup_gpio, execute_command, motor_stop
else:
   raise ValueError(f"Unsupported mode: {config.MODE}")

# 시그널 핸들러 설정
def signal_handler(sig, frame):
   print("서버를 종료합니다...")
   motor_stop()
   cleanup_gpio()
   if server_socket:
       server_socket.close()
   sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# 클라이언트 연결 처리 함수
def handle_client(client_socket, client_address):
   print(f"클라이언트가 연결되었습니다: {client_address}")
   
   # 초기 연결 메시지 전송
   client_socket.send("GO".encode('utf-8'))
   
   try:
       while True:
           # 데이터 수신
           data = client_socket.recv(1024)
           if not data:
               print(f"클라이언트 연결이 종료되었습니다: {client_address}")
               break
           
           # JSON 데이터 파싱
           try:
               command_data = json.loads(data.decode('utf-8'))
               command = command_data.get("command", "").upper()
               speed = command_data.get("speed", 50)
               
               print(f"명령어 수신: {command}, 속도: {speed}")
               
               # 모터 제어 실행
               if command in ["FORWARD", "BACKWARD", "LEFT", "RIGHT", "STOP"]:
                   # 모터 동작 실행
                   execute_command(command, speed)
                   
                   # 클라이언트에 응답 전송
                   client_socket.send(command.encode('utf-8'))
               else:
                   client_socket.send("UNKNOWN_COMMAND".encode('utf-8'))
                   
           except json.JSONDecodeError:
               print("잘못된 JSON 형식입니다.")
               client_socket.send("INVALID_FORMAT".encode('utf-8'))
               
   except Exception as e:
       print(f"클라이언트 처리 중 오류 발생: {e}")
   finally:
       # 연결이 종료되면 모터 정지
       motor_stop()
       client_socket.close()

# 메인 서버 코드
def start_server():
   global server_socket
   
   # GPIO 초기화
   init_gpio()
   
   # 서버 소켓 생성
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
   # 서버 주소 설정
   server_address = ('0.0.0.0', config.SERVER_PORT)
   
   try:
       # 소켓 바인딩 및 리스닝
       server_socket.bind(server_address)
       server_socket.listen(5)
       print(f"서버가 시작되었습니다. {server_address}에서 연결을 기다리는 중...")
       
       while True:
           # 클라이언트 연결 수락
           client_socket, client_address = server_socket.accept()
           
           # 클라이언트 처리를 위한 새 스레드 시작
           client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
           client_thread.daemon = True
           client_thread.start()
           
   except Exception as e:
       print(f"서버 실행 중 오류 발생: {e}")
   finally:
       # 서버 종료 시 정리 작업
       motor_stop()
       cleanup_gpio()
       if server_socket:
           server_socket.close()

if __name__ == "__main__":
   start_server()