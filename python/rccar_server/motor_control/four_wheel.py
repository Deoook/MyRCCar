# motor_control/four_wheel.py
import RPi.GPIO as GPIO
import time
import sys
import config

# 모터 핀 설정 가져오기
motor_pins = config.FOUR_WHEEL_PINS

# GPIO 초기화 함수
def init_gpio():
   # GPIO 모드 설정
   if config.GPIO_MODE == "BCM":
       GPIO.setmode(GPIO.BCM)
   else:
       GPIO.setmode(GPIO.BOARD)
   
   # 모터 핀 설정
   for pin in motor_pins.values():
       GPIO.setup(pin, GPIO.OUT)
       GPIO.output(pin, GPIO.LOW)
   
   print("GPIO 초기화 완료")

# GPIO 정리 함수
def cleanup_gpio():
   GPIO.cleanup()
   print("GPIO 정리 완료")

# 모터 정지 함수
def motor_stop():
   for pin in motor_pins.values():
       GPIO.output(pin, GPIO.LOW)

# 전진 함수
def forward(speed=config.DEFAULT_SPEED):
   # 전진: 앞바퀴 전진, 뒷바퀴 후진
   GPIO.output(motor_pins["motor1A"], GPIO.HIGH)    # 뒷바퀴 후진
   GPIO.output(motor_pins["motor1B"], GPIO.LOW)
   GPIO.output(motor_pins["motor2A"], GPIO.HIGH)
   GPIO.output(motor_pins["motor2B"], GPIO.LOW)
   GPIO.output(motor_pins["motor3A"], GPIO.LOW)     # 앞바퀴 전진
   GPIO.output(motor_pins["motor3B"], GPIO.HIGH)
   GPIO.output(motor_pins["motor4A"], GPIO.LOW)
   GPIO.output(motor_pins["motor4B"], GPIO.HIGH)

# 후진 함수
def backward(speed=config.DEFAULT_SPEED):
   # 후진: 앞바퀴 후진, 뒷바퀴 전진
   GPIO.output(motor_pins["motor1A"], GPIO.LOW)     # 뒷바퀴 전진
   GPIO.output(motor_pins["motor1B"], GPIO.HIGH)
   GPIO.output(motor_pins["motor2A"], GPIO.LOW)
   GPIO.output(motor_pins["motor2B"], GPIO.HIGH)
   GPIO.output(motor_pins["motor3A"], GPIO.HIGH)    # 앞바퀴 후진
   GPIO.output(motor_pins["motor3B"], GPIO.LOW)
   GPIO.output(motor_pins["motor4A"], GPIO.HIGH)
   GPIO.output(motor_pins["motor4B"], GPIO.LOW)

# 좌회전 함수
def left(speed=config.DEFAULT_SPEED):
   # 뒤 두바퀴 후진으로 좌회전
   GPIO.output(motor_pins["motor1A"], GPIO.HIGH)   # 좌하 후진
   GPIO.output(motor_pins["motor1B"], GPIO.LOW)
   GPIO.output(motor_pins["motor2A"], GPIO.HIGH)   # 우하 후진
   GPIO.output(motor_pins["motor2B"], GPIO.LOW)
   GPIO.output(motor_pins["motor3A"], GPIO.LOW)    # 앞바퀴는 정지
   GPIO.output(motor_pins["motor3B"], GPIO.LOW)
   GPIO.output(motor_pins["motor4A"], GPIO.LOW)
   GPIO.output(motor_pins["motor4B"], GPIO.LOW)

# 우회전 함수
def right(speed=config.DEFAULT_SPEED):
   # 앞 두바퀴 전진으로 우회전
   GPIO.output(motor_pins["motor1A"], GPIO.LOW)    # 뒷바퀴는 정지
   GPIO.output(motor_pins["motor1B"], GPIO.LOW)
   GPIO.output(motor_pins["motor2A"], GPIO.LOW)
   GPIO.output(motor_pins["motor2B"], GPIO.LOW)
   GPIO.output(motor_pins["motor3A"], GPIO.LOW)    # 우상 전진
   GPIO.output(motor_pins["motor3B"], GPIO.HIGH)
   GPIO.output(motor_pins["motor4A"], GPIO.LOW)    # 좌상 전진
   GPIO.output(motor_pins["motor4B"], GPIO.HIGH)

# 명령어에 따른 동작 실행 함수
def execute_command(command, speed=config.DEFAULT_SPEED):
   if command == "FORWARD":
       forward(speed)
   elif command == "BACKWARD":
       backward(speed)
   elif command == "LEFT":
       left(speed)
   elif command == "RIGHT":
       right(speed)
   elif command == "STOP":
       motor_stop()
   else:
       print(f"알 수 없는 명령어: {command}")

# 직접 실행 시 테스트 코드
if __name__ == "__main__":
   try:
       init_gpio()
       print("4륜 RC카 모터 테스트")
       print("명령어: forward, backward, left, right, stop, quit")
       
       while True:
           command = input("\n명령어 입력: ").upper()
           
           if command == "QUIT":
               break
               
           execute_command(command)
           
   except KeyboardInterrupt:
       print("\n프로그램을 종료합니다.")
   finally:
       motor_stop()
       cleanup_gpio()