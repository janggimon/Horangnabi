from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# 서보모터 제어 핀 설정
servo_pins = [12, 13, 6]  # 1번 서보(무한회전), 2번 서보(180도), 3번 서보(180도)

# GPIO 설정 (현재 서보모터가 없으므로 주석 처리)
# GPIO.setmode(GPIO.BCM)
# for pin in servo_pins:
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, GPIO.LOW)

# 서보모터 PWM 객체 생성 (주석 처리)
# servo1 = GPIO.PWM(servo_pins[0], 50)  # 50Hz PWM 신호
# servo2 = GPIO.PWM(servo_pins[1], 50)  # 50Hz PWM 신호
# servo3 = GPIO.PWM(servo_pins[2], 50)  # 50Hz PWM 신호

# 서보모터 초기화 (주석 처리)
# servo1.start(0)
# servo2.start(0)
# servo3.start(0)

def unlock_servo(servo_id):
    if servo_id == 1:
        # 1번 서보모터 (무한회전 서보모터) 잠금 해제
        print("Unlocking continuous rotation servo motor (Servo 1)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo1.ChangeDutyCycle(7.5)  # 듀티 사이클을 7.5로 설정 (정지)
        # time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        # servo1.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
        print("Servo 1 unlocked.")

    elif servo_id == 2:
        # 2번 서보모터 (180도 서보모터) 잠금 해제
        print("Unlocking 180-degree servo motor (Servo 2)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo2.ChangeDutyCycle(7.5)  # 90도 위치로 이동 (중간 위치)
        # time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        # servo2.ChangeDutyCycle(5)  # 45도 위치로 이동
        # time.sleep(0.5)
        # servo2.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
        print("Servo 2 unlocked.")

    elif servo_id == 3:
        # 3번 서보모터 (180도 서보모터) 잠금 해제
        print("Unlocking 180-degree servo motor (Servo 3)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo3.ChangeDutyCycle(7.5)  # 90도 위치로 이동 (중간 위치)
        # time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        # servo3.ChangeDutyCycle(5)  # 45도 위치로 이동
        # time.sleep(0.5)
        # servo3.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
        print("Servo 3 unlocked.")

@app.route('/unlock', methods=['POST'])
def unlock():
    servo_id = int(request.form['id'])
    if 1 <= servo_id <= 3:
        unlock_servo(servo_id)
        return "Success", 200
    else:
        return "Invalid servo ID", 400

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        # GPIO 정리 (주석 처리)
        # servo1.stop()
        # servo2.stop()
        # servo3.stop()
        # GPIO.cleanup()
        print("Server shutting down, GPIO cleanup done.")
