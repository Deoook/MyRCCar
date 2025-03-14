# sensors/ultrasonic.py
# test용 아직 실시간과 회피 기능이 넣어 있지 않음
import RPi.GPIO as GPIO
import time
import config

# 초음파 센서 핀 설정
TRIG = config.ULTRASONIC_PINS["trig"]
ECHO = config.ULTRASONIC_PINS["echo"]

# 초음파 센서 초기화
def init_ultrasonic():
   # GPIO 모드 설정 (이미 설정되어 있다고 가정)
   # 핀 설정
   GPIO.setup(TRIG, GPIO.OUT)
   GPIO.setup(ECHO, GPIO.IN)
   
   # 트리거 핀 초기화
   GPIO.output(TRIG, False)
   print("초음파 센서 초기화 중...")
   time.sleep(0.5)  # 센서 안정화 시간
   print("초음파 센서 초기화 완료")

# 거리 측정 함수
def measure_distance():
   # 트리거 신호 발생 (10us 펄스)
   GPIO.output(TRIG, True)
   time.sleep(0.00001)  # 10us
   GPIO.output(TRIG, False)
   
   # 에코 신호가 돌아올 때까지 대기
   pulse_start = time.time()
   timeout = pulse_start + 1  # 1초 타임아웃 설정
   
   # 에코 신호가 LOW에서 HIGH로 바뀔 때까지 대기
   while GPIO.input(ECHO) == 0:
       pulse_start = time.time()
       if pulse_start > timeout:
           return -1  # 타임아웃 발생
   
   # 에코 신호가 HIGH에서 LOW로 바뀔 때까지 대기
   pulse_end = time.time()
   timeout = pulse_end + 1  # 1초 타임아웃 설정
   
   while GPIO.input(ECHO) == 1:
       pulse_end = time.time()
       if pulse_end > timeout:
           return -1  # 타임아웃 발생
   
   # 펄스 지속 시간 계산
   pulse_duration = pulse_end - pulse_start
   
   # 거리 계산 (음속 = 343m/s, 왕복거리이므로 나누기 2)
   distance = pulse_duration * 34300 / 2
   
   # 측정 범위 확인 (일반적으로 2cm~400cm)
   if distance < 2 or distance > 400:
       return -1
   
   return round(distance, 2)  # 소수점 2자리까지 반올림

# 연속 측정 함수
def continuous_measure(interval=0.1, count=10):
   """
   일정 간격으로 연속 측정하고 평균값 반환
   interval: 측정 간격 (초)
   count: 측정 횟수
   """
   distances = []
   for _ in range(count):
       dist = measure_distance()
       if dist > 0:  # 유효한 측정값만 추가
           distances.append(dist)
       time.sleep(interval)
   
   # 유효한 측정값이 없으면 -1 반환
   if not distances:
       return -1
   
   # 평균값 계산
   return sum(distances) / len(distances)

# 장애물 감지 함수
def detect_obstacle(threshold=20):
   """
   장애물 감지 함수
   threshold: 장애물 감지 기준 거리 (cm)
   """
   distance = measure_distance()
   if distance > 0 and distance < threshold:
       return True, distance
   return False, distance

# 직접 실행 시 테스트 코드
if __name__ == "__main__":
   try:
       # GPIO 모드 설정
       if config.GPIO_MODE == "BCM":
           GPIO.setmode(GPIO.BCM)
       else:
           GPIO.setmode(GPIO.BOARD)
       
       init_ultrasonic()
       print("초음파 센서 테스트 (Ctrl+C로 종료)")
       
       while True:
           dist = measure_distance()
           if dist > 0:
               print(f"측정된 거리: {dist} cm")
           else:
               print("거리 측정 실패")
           
           # 장애물 감지 테스트
           obstacle, distance = detect_obstacle()
           if obstacle:
               print(f"경고: {distance}cm 거리에 장애물이 감지되었습니다!")
           
           time.sleep(1)  # 1초마다 측정
           
   except KeyboardInterrupt:
       print("\n프로그램을 종료합니다.")
   finally:
       GPIO.cleanup()