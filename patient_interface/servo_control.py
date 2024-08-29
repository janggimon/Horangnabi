from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# 서보모터 제어 핀 설정 (핀 번호는 실제 연결에 따라 조정)
servo_pins = [17, 27, 22]

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def unlock_servo(servo_id):
    # 서보모터 잠금 해제 (여기서는 1초 동안만 활성화)
    GPIO.output(servo_pins[servo_id - 1], GPIO.HIGH)
    time.sleep(1)
    GPIO.output(servo_pins[servo_id - 1], GPIO.LOW)

@app.route('/unlock', methods=['POST'])
def unlock():
    servo_id = int(request.form['id'])
    if 1 <= servo_id <= 3:
        unlock_servo(servo_id)
        return "Success", 200
    else:
        return "Invalid servo ID", 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
