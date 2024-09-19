import pigpio
from flask import Flask, request

app = Flask(__name__)

servo_pins = [12, 13, 6]  # 서보모터 핀 번호
servo_positions = {1: 90, 2: 90, 3: 90}  # 서보모터 초기 각도는 90도

# pigpio 초기화
pi = pigpio.pi()

# 서보모터 각도를 설정하는 함수 (각도를 펄스 폭으로 변환)
def set_servo_angle(servo_id, angle):
    pulse_width = 500 + (angle / 180.0) * 2000  # 500us ~ 2500us 펄스폭 범위
    pi.set_servo_pulsewidth(servo_pins[servo_id - 1], pulse_width)
    servo_positions[servo_id] = angle  # 현재 각도 저장

# unlock: 서보모터를 130도 위치로 이동
def unlock_servo(servo_id):
    print(f"Unlocking Servo {servo_id}...")
    set_servo_angle(servo_id, 130)  # 130도 위치로 이동
    print(f"Servo {servo_id} unlocked at 130 degrees.")

# lock: 서보모터를 90도 위치로 이동
def lock_servo(servo_id):
    print(f"Locking Servo {servo_id}...")
    set_servo_angle(servo_id, 90)  # 90도 위치로 이동
    print(f"Servo {servo_id} locked at 90 degrees.")

@app.route('/servo', methods=['POST'])
def control_servo():
    servo_id = int(request.form['id'])  # 서보모터 ID (1, 2, 3)
    action = request.form.get('action', 'unlock')

    if servo_id not in [1, 2, 3]:
        return "Invalid servo ID", 400

    if action == 'unlock':
        unlock_servo(servo_id)
        return f"Servo {servo_id} unlocked", 200
    elif action == 'lock':
        lock_servo(servo_id)
        return f"Servo {servo_id} locked", 200
    else:
        return "Invalid action", 400

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        # 서버 종료 시 모든 서보모터의 펄스폭을 0으로 설정
        for pin in servo_pins:
            pi.set_servo_pulsewidth(pin, 0)
        pi.stop()
        print("Server shutting down, pigpio cleanup done.")
