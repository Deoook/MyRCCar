# client_gui_pyside.py
import sys
import json
import socket
import threading
from PySide2.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                              QVBoxLayout, QHBoxLayout, QLabel, QWidget, 
                              QLineEdit, QGridLayout, QStatusBar, QTextEdit)
from PySide2.QtCore import Qt, QTimer, Signal, QObject

# 스레드와 메인 스레드 간 통신을 위한 신호 클래스
class Communicator(QObject):
    signal_log = Signal(str)
    signal_connected = Signal(bool, str)
    signal_command_result = Signal(bool, str)

class RCCarClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.client_socket = None
        self.connected = False
        self.communicator = Communicator()
        
        # 신호 연결
        self.communicator.signal_log.connect(self.append_log)
        self.communicator.signal_connected.connect(self.handle_connection_result)
        self.communicator.signal_command_result.connect(self.handle_command_result)
        
    def initUI(self):
        # 메인 윈도우 설정
        self.setWindowTitle('RC Car Controller')
        self.setGeometry(300, 300, 500, 500)
        
        # 중앙 위젯 및 레이아웃 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 연결 설정 부분
        connection_layout = QHBoxLayout()
        self.ip_input = QLineEdit('192.168.0.145')
        self.ip_input.setPlaceholderText('Server IP')
        self.port_input = QLineEdit('5000')
        self.port_input.setPlaceholderText('Port')
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.toggle_connection)
        
        connection_layout.addWidget(QLabel('Server IP:'))
        connection_layout.addWidget(self.ip_input)
        connection_layout.addWidget(QLabel('Port:'))
        connection_layout.addWidget(self.port_input)
        connection_layout.addWidget(self.connect_button)
        
        main_layout.addLayout(connection_layout)
        
        # 제어 버튼 그리드
        control_layout = QGridLayout()
        
        self.forward_btn = QPushButton('Forward')
        self.backward_btn = QPushButton('Backward')
        self.left_btn = QPushButton('Left')
        self.right_btn = QPushButton('Right')
        self.stop_btn = QPushButton('STOP')
        
        # 키 눌렀을 때와 뗐을 때 이벤트 처리
        self.forward_btn.pressed.connect(lambda: self.send_command("FORWARD"))
        self.forward_btn.released.connect(lambda: self.send_command("STOP"))
        
        self.backward_btn.pressed.connect(lambda: self.send_command("BACKWARD"))
        self.backward_btn.released.connect(lambda: self.send_command("STOP"))
        
        self.left_btn.pressed.connect(lambda: self.send_command("LEFT"))
        self.left_btn.released.connect(lambda: self.send_command("STOP"))
        
        self.right_btn.pressed.connect(lambda: self.send_command("RIGHT"))
        self.right_btn.released.connect(lambda: self.send_command("STOP"))
        
        self.stop_btn.clicked.connect(lambda: self.send_command("STOP"))
        
        # 버튼 비활성화 (연결 전)
        self.set_control_enabled(False)
        
        # 그리드에 버튼 배치
        control_layout.addWidget(self.forward_btn, 0, 1)
        control_layout.addWidget(self.left_btn, 1, 0)
        control_layout.addWidget(self.stop_btn, 1, 1)
        control_layout.addWidget(self.right_btn, 1, 2)
        control_layout.addWidget(self.backward_btn, 2, 1)
        
        main_layout.addLayout(control_layout)
        
        # 로그 출력용 텍스트 박스
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(QLabel("Log:"))
        main_layout.addWidget(self.log_text)
        
        # 상태 표시줄
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('Not Connected')
        
        # 키보드 이벤트 활성화
        self.setFocusPolicy(Qt.StrongFocus)
    
    def append_log(self, text):
        self.log_text.append(text)
        
    def handle_connection_result(self, success, message):
        if success:
            self.connected = True
            self.connect_button.setText('Disconnect')
            self.set_control_enabled(True)
        else:
            self.connected = False
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
        
        self.statusBar.showMessage(message)
        self.append_log(message)
    
    def handle_command_result(self, success, message):
        if not success:
            self.disconnect_from_server()
        self.statusBar.showMessage(message)
        self.append_log(message)
    
    def keyPressEvent(self, event):
        if not self.connected:
            return
            
        if event.key() == Qt.Key_Up:
            self.send_command("FORWARD")
        elif event.key() == Qt.Key_Down:
            self.send_command("BACKWARD")
        elif event.key() == Qt.Key_Left:
            self.send_command("LEFT")
        elif event.key() == Qt.Key_Right:
            self.send_command("RIGHT")
        elif event.key() == Qt.Key_Space:
            self.send_command("STOP")
    
    def keyReleaseEvent(self, event):
        if not self.connected:
            return
            
        if event.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            self.send_command("STOP")
    
    def toggle_connection(self):
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        
        # 연결 버튼 비활성화
        self.connect_button.setEnabled(False)
        self.statusBar.showMessage('Connecting...')
        self.append_log('연결 시도 중...')
        
        # 별도 스레드에서 연결 시도
        connection_thread = threading.Thread(
            target=self._connect_thread,
            args=(ip, port)
        )
        connection_thread.daemon = True
        connection_thread.start()
    
    def _connect_thread(self, ip, port):
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_obj.connect((ip, port))
            
            # 초기 연결 메시지 수신
            initial_msg = socket_obj.recv(1024).decode('utf-8')
            
            self.client_socket = socket_obj
            self.communicator.signal_connected.emit(True, f'Connected to server. Received: {initial_msg}')
            
        except Exception as e:
            self.communicator.signal_connected.emit(False, f'Connection failed: {str(e)}')
        finally:
            # 연결 버튼 다시 활성화
            self.connect_button.setEnabled(True)
    
    def disconnect_from_server(self):
        if self.client_socket:
            try:
                self.send_command("STOP")  # 연결 종료 전 정지 명령
                self.client_socket.close()
            except:
                pass
            finally:
                self.client_socket = None
                
        self.connected = False
        self.connect_button.setText('Connect')
        self.set_control_enabled(False)
        self.statusBar.showMessage('Disconnected from server')
        self.append_log('서버와 연결이 종료되었습니다.')
    
    def set_control_enabled(self, enabled):
        self.forward_btn.setEnabled(enabled)
        self.backward_btn.setEnabled(enabled)
        self.left_btn.setEnabled(enabled)
        self.right_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(enabled)
    
    def send_command(self, command):
        if not self.connected or not self.client_socket:
            return
            
        # 별도 스레드에서 명령 전송
        command_thread = threading.Thread(
            target=self._send_command_thread,
            args=(command,)
        )
        command_thread.daemon = True
        command_thread.start()
    
    def _send_command_thread(self, command):
        try:
            command_data = {
                "command": command,
                "speed": 50  # 기본 속도값
            }
            
            data = json.dumps(command_data).encode('utf-8')
            self.client_socket.send(data)
            
            self.communicator.signal_command_result.emit(True, f'Sent: {command}')
            
        except Exception as e:
            self.communicator.signal_command_result.emit(False, f'Command failed: {str(e)}')
    
    def closeEvent(self, event):
        self.disconnect_from_server()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RCCarClientGUI()
    window.show()
    sys.exit(app.exec_())