# motor_control/two_wheel.py
import RPi.GPIO as GPIO
import time
import sys
import config

# 모터 핀 설정 가져오기
motor_pins = config.TWO_WHEEL_PINS

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
   # 양쪽 모터 모두 전진
   GPIO.output(motor_pins["leftA"], GPIO.LOW)
   GPIO.output(motor_pins["leftB"], GPIO.HIGH)
   GPIO.output(motor_pins["rightA"], GPIO.LOW)
   GPIO.output(motor_pins["rightB"], GPIO.HIGH)

# 후진 함수
def backward(speed=config.DEFAULT_SPEED):
   # 양쪽 모터 모두 후진
   GPIO.output(motor_pins["leftA"], GPIO.HIGH)
   GPIO.output(motor_pins["leftB"], GPIO.LOW)
   GPIO.output(motor_pins["rightA"], GPIO.HIGH)
   GPIO.output(motor_pins["rightB"], GPIO.LOW)

# 좌회전 함수
def left(speed=config.DEFAULT_SPEED):
   # 우측 모터만 전진 (제자리 좌회전)
   GPIO.output(motor_pins["leftA"], GPIO.LOW)
   GPIO.output(motor_pins["leftB"], GPIO.LOW)    # 왼쪽 모터 정지
   GPIO.output(motor_pins["rightA"], GPIO.LOW)
   GPIO.output(motor_pins["rightB"], GPIO.HIGH)  # 오른쪽 모터 전진

# 우회전 함수
def right(speed=config.DEFAULT_SPEED):
   # 좌측 모터만 전진 (제자리 우회전)
   GPIO.output(motor_pins["leftA"], GPIO.LOW)
   GPIO.output(motor_pins["leftB"], GPIO.HIGH)   # 왼쪽 모터 전진
   GPIO.output(motor_pins["rightA"], GPIO.LOW)
   GPIO.output(motor_pins["rightB"], GPIO.LOW)   # 오른쪽 모터 정지

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
       print("2륜 RC카 모터 테스트")
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