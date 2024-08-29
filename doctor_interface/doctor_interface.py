import tkinter as tk
import requests
import socket  # IP 주소를 가져오기 위해 socket 라이브러리 추가

# 현재 노트북의 IP 주소를 가져오는 함수
def get_local_ip():
    try:
        # dummy socket connection을 사용해 노트북의 IP 주소를 가져옵니다.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('10.254.254.254', 1))  # 인터넷 연결이 필요하지 않습니다.
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Could not get local IP address: {e}")
        local_ip = '127.0.0.1'  # 로컬 호스트로 기본 설정
    finally:
        s.close()
    return local_ip

# 노트북의 IP 주소를 자동으로 가져와서 SERVER_URL을 업데이트
LOCAL_IP = get_local_ip()
SERVER_URL = f'http://{LOCAL_IP}:5000/unlock'

# Zoom 회의 URL
ZOOM_URL = 'https://zoom.us/wc/join/{MEETING_ID}'  # {MEETING_ID}를 실제 Zoom 회의 ID로 변경하세요.

def join_meeting():
    # Zoom 회의실에 입장
    import webbrowser
    webbrowser.open(ZOOM_URL, new=2)

def send_prescription(prescription_id):
    # 해당 서보모터를 제어하기 위해 라즈베리 파이에 요청 보내기
    try:
        response = requests.post(SERVER_URL, data={'id': prescription_id})
        if response.status_code == 200:
            print(f"Prescription {prescription_id} processed successfully.")
        else:
            print(f"Failed to process prescription {prescription_id}.")
    except Exception as e:
        print(f"Error sending request: {e}")

# Tkinter GUI 설정
root = tk.Tk()
root.title("의사 진료 인터페이스")
root.geometry("800x600")  # 전체 창 크기
root.configure(bg='white')

# Zoom 회의실 입장 버튼
join_button = tk.Button(root, text="진료하기", command=join_meeting, font=("Arial", 24), width=15, height=2)
join_button.pack(pady=30)

# 처방 버튼
for i in range(1, 4):
    btn = tk.Button(root, text=f"약 {i} 처방", command=lambda i=i: send_prescription(i), font=("Arial", 16), width=20, height=2)
    btn.pack(pady=10)

root.mainloop()
