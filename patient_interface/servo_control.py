from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# 서보모터 제어 핀 설정
servo_pins = [12, 13, 6]

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def unlock_servo(servo_id):
    # 서보모터 잠금 해제 (잠금해제 15초 후 잠금)
    GPIO.output(servo_pins[servo_id - 1], GPIO.HIGH)
    time.sleep(15)
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
