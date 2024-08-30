from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

servo_pins = [12, 13, 6]  # 서보모터 핀 번호

# 서보모터 초기화
GPIO.setmode(GPIO.BCM)
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

servo1 = GPIO.PWM(servo_pins[0], 50)  # 50Hz PWM 신호
servo2 = GPIO.PWM(servo_pins[1], 50)  # 50Hz PWM 신호
servo3 = GPIO.PWM(servo_pins[2], 50)  # 50Hz PWM 신호

servo1.start(7.5)  # 무한 회전 서보모터 초기화
servo2.start(7.5)  # 180도 서보모터 초기화 (중간 위치)
servo3.start(7.5)  # 180도 서보모터 초기화 (중간 위치)

def unlock_servo(servo_id):
    if servo_id == 1:
        print("Unlocking continuous rotation servo motor (Servo 1)...")
        # 실제 서보모터 제어 코드 주석 처리
        servo1.ChangeDutyCycle(10)  # 시계방향으로 45도 이동 (가속)
        time.sleep(1)  # 모터가 회전하도록 잠시 대기
        servo1.ChangeDutyCycle(7.5)  # 정지 상태
        print("Servo 1 unlocked.")

    elif servo_id == 2:
        print("Unlocking 180-degree servo motor (Servo 2)...")
        servo2.ChangeDutyCycle(10)  # 시계방향으로 45도 이동
        time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        servo2.ChangeDutyCycle(7.5)  # 원래 위치로 돌아가도록 조정
        time.sleep(0.5)
        print("Servo 2 unlocked.")

    elif servo_id == 3:
        print("Unlocking 180-degree servo motor (Servo 3)...")
        servo3.ChangeDutyCycle(10)  # 시계방향으로 45도 이동
        time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        servo3.ChangeDutyCycle(7.5)  # 원래 위치로 돌아가도록 조정
        time.sleep(0.5)
        print("Servo 3 unlocked.")

def lock_servo(servo_id):
    if servo_id == 1:
        print("Locking continuous rotation servo motor (Servo 1)...")
        # 실제 서보모터 제어 코드 주석 처리
        servo1.ChangeDutyCycle(5)  # 반시계방향으로 45도 이동 (감속)
        time.sleep(1)  # 모터가 회전하도록 잠시 대기
        servo1.ChangeDutyCycle(7.5)  # 정지 상태
        print("Servo 1 locked.")

    elif servo_id == 2:
        print("Locking 180-degree servo motor (Servo 2)...")
        servo2.ChangeDutyCycle(5)  # 반시계방향으로 45도 이동
        time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        servo2.ChangeDutyCycle(7.5)  # 원래 위치로 돌아가도록 조정
        time.sleep(0.5)
        print("Servo 2 locked.")

    elif servo_id == 3:
        print("Locking 180-degree servo motor (Servo 3)...")
        servo3.ChangeDutyCycle(5)  # 반시계방향으로 45도 이동
        time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        servo3.ChangeDutyCycle(7.5)  # 원래 위치로 돌아가도록 조정
        time.sleep(0.5)
        print("Servo 3 locked.")

@app.route('/unlock', methods=['POST'])
def unlock():
    servo_id = int(request.form['id'])
    action = request.form.get('action', 'unlock')

    if action == 'unlock':
        unlock_servo(servo_id)
        return "Unlocked", 200
    elif action == 'lock':
        lock_servo(servo_id)
        return "Locked", 200
    else:
        return "Invalid action", 400

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        servo1.stop()
        servo2.stop()
        servo3.stop()
        GPIO.cleanup()
        print("Server shutting down, GPIO cleanup done.")
