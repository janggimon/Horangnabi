from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

servo_pins = [12, 13, 6]  # 서보모터 핀 번호

def lock_servo(servo_id):
    if servo_id == 1:
        print("Locking continuous rotation servo motor (Servo 1)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo1.ChangeDutyCycle(7.5)  # 듀티 사이클을 7.5로 설정 (정지)
        # time.sleep(0.5)  # 모터가 회전하도록 잠시 대기
        # servo1.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
        print("Servo 1 locked.")

    elif servo_id == 2:
        print("Locking 180-degree servo motor (Servo 2)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo2.ChangeDutyCycle(5)  # 45도 위치로 이동
        # time.sleep(0.5)
        # servo2.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
        print("Servo 2 locked.")

    elif servo_id == 3:
        print("Locking 180-degree servo motor (Servo 3)...")
        # 실제 서보모터 제어 코드 주석 처리
        # servo3.ChangeDutyCycle(5)  # 45도 위치로 이동
        # time.sleep(0.5)
        # servo3.ChangeDutyCycle(0)  # 듀티 사이클을 0으로 설정하여 멈춤
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
        print("Server shutting down, GPIO cleanup done.")
