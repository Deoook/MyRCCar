# config.py

# 동작 모드 설정 (FOUR_WHEEL 또는 TWO_WHEEL)
MODE = "FOUR_WHEEL"

# 서버 설정
SERVER_PORT = 5000

# GPIO 모드 설정
GPIO_MODE = "BCM"  # "BCM" 또는 "BOARD"

# 4륜 모터 GPIO 핀 설정
FOUR_WHEEL_PINS = {
    "motor1A": 1,  # 좌하
    "motor1B": 2,
    "motor2A": 3,  # 우하
    "motor2B": 4,
    "motor3A": 5,  # 우상
    "motor3B": 6,
    "motor4A": 7,  # 좌상
    "motor4B": 8
}

# 2륜 모터 GPIO 핀 설정
TWO_WHEEL_PINS = {
    "leftA": 1,   # 왼쪽 모터
    "leftB": 2,
    "rightA": 3,  # 오른쪽 모터
    "rightB": 4
}

# 초음파 센서 GPIO 핀 설정
ULTRASONIC_PINS = {
    "trig": 23,
    "echo": 24
}

# 모터 속도 설정 (PWM 사용 시)
DEFAULT_SPEED = 50
MAX_SPEED = 100