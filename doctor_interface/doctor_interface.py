import tkinter as tk
import requests
import socket
import subprocess  # Zoom 애플리케이션 실행을 위한 라이브러리 추가

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Could not get local IP address: {e}")
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

LOCAL_IP = get_local_ip()
SERVER_URL = f'http://{LOCAL_IP}:5000/unlock'

def start_meeting_as_host():
    try:
        # 호스트로서 Zoom 회의 생성 (Windows 경로 예시)
        # Zoom 경로를 본인의 Zoom 설치 경로로 변경하세요.
        zoom_path = "/usr/bin/zoom"
        
        # 회의 ID와 패스워드를 설정합니다 (호스트의 Zoom 계정이 필요)
        meeting_id = "8528776866"  # 본인의 회의 ID로 변경하세요.
        zoom_url = f"zoommtg://zoom.us/start?confno={meeting_id}"
        
        subprocess.Popen([zoom_path, "--url=" + zoom_url])
    except Exception as e:
        print(f"Failed to start Zoom meeting as host: {e}")

def send_prescription(prescription_id):
    try:
        response = requests.post(SERVER_URL, data={'id': prescription_id})
        if response.status_code == 200:
            print(f"Prescription {prescription_id} processed successfully.")
        else:
            print(f"Failed to process prescription {prescription_id}.")
    except Exception as e:
        print(f"Error sending request: {e}")

root = tk.Tk()
root.title("의사 진료 인터페이스")
root.geometry("800x600")
root.configure(bg='white')

# 회의 시작 버튼 (호스트로서)
start_button = tk.Button(root, text="진료 시작하기", command=start_meeting_as_host, font=("Arial", 24), width=15, height=2)
start_button.pack(pady=30)

for i in range(1, 4):
    btn = tk.Button(root, text=f"약 {i} 처방", command=lambda i=i: send_prescription(i), font=("Arial", 16), width=20, height=2)
    btn.pack(pady=10)

root.mainloop()
