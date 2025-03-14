import RPi.GPIO as GPIO
import time
import signal
import sys
import atexit

# 모터 드라이버 핀 설정
motor_pins = {
   "motor1A": 1,  # GPIO1  # 좌하
   "motor1B": 2,  # GPIO2  
   "motor2A": 3,  # GPIO3  # 우하
   "motor2B": 4,  # GPIO4
   "motor3A": 5,  # GPIO5 # 우상
   "motor3B": 6,  # GPIO6
   "motor4A": 7,  # GPIO7 # 좌상
   "motor4B": 8,  # GPIO8
}

# GPIO 설정
GPIO.setmode(GPIO.BCM)  # gpio 번호 사용
for pin in motor_pins.values():
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

def cleanup_handler(signum=None, frame=None):
   print("정리 작업 수행 중...")
   motor_stop()
   GPIO.cleanup()
   sys.exit(0)

# 종료 시 정리 작업을 위한 핸들러 등록
signal.signal(signal.SIGTERM, cleanup_handler)
signal.signal(signal.SIGINT, cleanup_handler)
atexit.register(cleanup_handler)

# 모터 제어 함수
def motor_stop():
   for pin in motor_pins.values():
       GPIO.output(pin, GPIO.LOW)

def test_motor(motor_name, direction):
    motor_stop()  # 먼저 모든 모터 정지
    
    if motor_name == "motor1":  # 좌하
        if direction == "forward":
            GPIO.output(motor_pins["motor1A"], GPIO.LOW)
            GPIO.output(motor_pins["motor1B"], GPIO.HIGH)
        else:  # backward
            GPIO.output(motor_pins["motor1A"], GPIO.HIGH)
            GPIO.output(motor_pins["motor1B"], GPIO.LOW)
    
    elif motor_name == "motor2":  # 우하
        if direction == "forward":
            GPIO.output(motor_pins["motor2A"], GPIO.LOW)
            GPIO.output(motor_pins["motor2B"], GPIO.HIGH)
        else:  # backward
            GPIO.output(motor_pins["motor2A"], GPIO.HIGH)
            GPIO.output(motor_pins["motor2B"], GPIO.LOW)
    
    elif motor_name == "motor3":  # 우상
        if direction == "forward":
            GPIO.output(motor_pins["motor3A"], GPIO.LOW)
            GPIO.output(motor_pins["motor3B"], GPIO.HIGH)
        else:  # backward
            GPIO.output(motor_pins["motor3A"], GPIO.HIGH)
            GPIO.output(motor_pins["motor3B"], GPIO.LOW)
    
    elif motor_name == "motor4":  # 좌상
        if direction == "forward":
            GPIO.output(motor_pins["motor4A"], GPIO.LOW)
            GPIO.output(motor_pins["motor4B"], GPIO.HIGH)
        else:  # backward
            GPIO.output(motor_pins["motor4A"], GPIO.HIGH)
            GPIO.output(motor_pins["motor4B"], GPIO.LOW)

# 메인 실행 코드
try:
    print("모터 테스트 프로그램")
    print("각 모터를 개별적으로 테스트합니다.")
    print("명령어: motor[번호]-[방향]")
    print("예: motor1-forward, motor2-backward")
    
    while True:
        command = input("\n테스트할 모터와 방향 (quit으로 종료): ")
        
        if command.lower() == "quit":
            break
        
        try:
            parts = command.split("-")
            motor = parts[0].strip()
            direction = parts[1].strip()
            
            if motor in ["motor1", "motor2", "motor3", "motor4"] and direction in ["forward", "backward"]:
                print(f"{motor}를 {direction} 방향으로 2초간 구동합니다...")
                test_motor(motor, direction)
                time.sleep(2)  # 2초 동안 실행
                motor_stop()
            else:
                print("잘못된 명령어입니다. 예: motor1-forward")
        except:
            print("명령어 형식이 잘못되었습니다. 예: motor1-forward")
            
except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
finally:
    motor_stop()
    GPIO.cleanup()