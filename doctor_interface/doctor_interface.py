import tkinter as tk
import requests

# Zoom 회의 URL
ZOOM_URL = 'https://zoom.us/wc/join/{MEETING_ID}'  # {MEETING_ID}를 실제 Zoom 회의 ID로 변경하세요.

# 서보모터 제어 서버 URL
SERVER_URL = 'http://[라즈베리파이_IP]:5000/unlock'  # [라즈베리파이_IP]를 실제 라즈베리 파이 IP로 변경하세요.

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
