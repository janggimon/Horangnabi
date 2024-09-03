import tkinter as tk
import requests
import subprocess
import time
import os

# 기본 IP 주소 설정
LOCAL_IP = '127.0.0.1'
SERVER_URL = f'http://{LOCAL_IP}:5000/unlock'

# 파일 경로 설정
NOTES_FILE = "notes.txt"

def update_ip():
    """IP 주소를 업데이트하고 서버 URL을 변경하는 함수"""
    global LOCAL_IP, SERVER_URL
    LOCAL_IP = ip_entry.get()
    SERVER_URL = f'http://{LOCAL_IP}:5000/unlock'
    print(f"Updated IP to: {LOCAL_IP}")
    ip_entry.delete(0, tk.END)
    ip_entry.insert(0, '업데이트 완료!')
    root.after(1000, lambda: ip_entry.delete(0, tk.END))  # 1초 후 입력란 초기화

# 호스트로 회의실 참가하는 함수
def start_meeting_as_host():
    try:
        zoom_path = "/usr/bin/zoom"  # Zoom 애플리케이션의 실제 경로로 업데이트
        meeting_id = "8528776866"  # 호스트용 회의 ID (실제 회의 ID로 변경)
        zoom_url = f"zoommtg://zoom.us/start?confno={meeting_id}"

        # Zoom 애플리케이션을 회의 URL과 함께 시작
        subprocess.Popen([zoom_path, "--url=" + zoom_url])
        root.after(5000, handle_zoom_windows)  # Zoom 창이 열릴 때까지 5초 대기

    except Exception as e:
        print(f"Failed to start Zoom meeting as host: {e}")

# 줌 윈도우 위치 조정하는 함수
def handle_zoom_windows():
    try:
        subprocess.call("wmctrl -c 'Zoom Workplace - Free account'", shell=True)
        
        meeting_window_open = False
        for _ in range(10):  # 최대 10번 확인
            result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
            if 'Meeting' in result.stdout:
                meeting_window_open = True
                break
            time.sleep(1)
        
        if not meeting_window_open:
            print("Zoom meeting window not found.")
            return

        left_frame.update_idletasks()
        left_frame_width = left_frame.winfo_width()
        left_frame_height = left_frame.winfo_height()
        left_frame_x = left_frame.winfo_rootx()
        left_frame_y = left_frame.winfo_rooty()

        new_width = int(root.winfo_screenwidth() * 0.78)
        new_x = 0  # Zoom 창의 왼쪽 가장자리를 화면의 왼쪽 가장자리와 맞춤

        zoom_window_cmd = (f"wmctrl -r 'Meeting' -e 0,{new_x},{left_frame_y},{new_width},{left_frame_height}")
        subprocess.Popen(zoom_window_cmd, shell=True)
        
        # Zoom 회의 창을 항상 위에 있게 설정
        subprocess.Popen("wmctrl -r 'Meeting' -b add,above", shell=True)

    except Exception as e:
        print(f"Failed to handle Zoom windows: {e}")

# 서보 모터 잠금/잠금 해제 신호 전송 및 LED 색상 변경
def toggle_lock(prescription_id):
    try:
        led, notes = leds[prescription_id - 1]
        current_color = led["bg"]

        # 현재 LED 색상에 따라 잠금/잠금 해제 수행
        if current_color == "red":
            response = requests.post(SERVER_URL, data={'id': prescription_id, 'action': 'unlock'})
            if response.status_code == 200:
                print(f"Prescription {prescription_id} unlocked successfully.")
                led.config(bg="green")
            else:
                print(f"Failed to unlock prescription {prescription_id}.")
        else:
            response = requests.post(SERVER_URL, data={'id': prescription_id, 'action': 'lock'})
            if response.status_code == 200:
                print(f"Prescription {prescription_id} locked successfully.")
                led.config(bg="red")
            else:
                print(f"Failed to lock prescription {prescription_id}.")
    except Exception as e:
        print(f"Error sending request: {e}")

# 메모장 내용을 파일에 저장하는 함수
def save_notes():
    try:
        with open(NOTES_FILE, "w") as file:
            for _, notes in leds:
                file.write(notes.get("1.0", tk.END))
                file.write("\n---\n")
    except Exception as e:
        print(f"Error saving notes: {e}")

# 파일에서 메모장 내용을 불러오는 함수
def load_notes():
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as file:
                notes_contents = file.read().split("\n---\n")
                for (led, notes), content in zip(leds, notes_contents):
                    notes.delete("1.0", tk.END)
                    notes.insert(tk.END, content)
    except Exception as e:
        print(f"Error loading notes: {e}")

# 프로그램 종료 함수
def exit_fullscreen():
    save_notes()  # 메모장 내용을 파일에 저장
    root.attributes('-fullscreen', False)
    root.quit()

root = tk.Tk()
root.title("의사 진료 인터페이스")

root.attributes('-fullscreen', True)
root.configure(bg='white')

left_frame = tk.Frame(root, bg='light sky blue', width=int(root.winfo_screenwidth() * 0.85), height=root.winfo_screenheight(), highlightbackground="black", highlightthickness=75)
left_frame.pack(side='left', fill='both')

info_label = tk.Label(left_frame, text="우측의 '진료 시작하기' 버튼을 눌러 화상 진료실로 입장할 수 있습니다.\n\n드론의 IP 주소를 환자에게서 확인 후, 좌측 입력란에 입력하여야 약품함 제어가 가능합니다.", 
                      font=("Arial", 20), fg='navy', bg='light sky blue')
info_label.place(relx=0.5, rely=0.5, anchor='center')

right_frame = tk.Frame(root, bg='white', width=int(root.winfo_screenwidth() * 0.2))
right_frame.pack(side='right', fill='y', padx=20, pady=20)

button_style = {"font": ("Arial", 14), "width": 18, "height": 1, "bg": "#f0f0f0", "fg": "#333", "relief": "raised", "bd": 2}

start_button = tk.Button(right_frame, text="진료 시작하기", command=start_meeting_as_host, font=("Arial", 20), width=15, height=2, bg="#4CAF50", fg="white", relief="groove", bd=3)
start_button.pack(pady=(20, 10))

# IP 주소 입력란과 버튼을 '진료 시작하기' 버튼 아래로 이동
ip_label = tk.Label(right_frame, text="IP 주소 입력:", font=("Arial", 12), bg='white')
ip_label.pack(pady=(20, 5))
ip_entry = tk.Entry(right_frame, font=("Arial", 12))
ip_entry.pack(pady=(0, 10))
ip_button = tk.Button(right_frame, text="IP 업데이트", command=update_ip, **button_style)
ip_button.pack(pady=(0, 20))

# 약품함 잠금해제 버튼과 LED 버튼을 포함할 프레임
leds_frame = tk.Frame(right_frame, bg='white')
leds_frame.pack(pady=20, fill='both', expand=True)

leds = []
for i in range(1, 4):
    frame = tk.Frame(leds_frame, bg='white')
    frame.pack(pady=10, fill='x')

    led = tk.Label(frame, bg="red", width=2, height=1, relief="sunken")
    led.pack(side="top", pady=(0, 10))  # LED를 버튼 상단에 위치시킵니다.

    btn = tk.Button(frame, text=f"{i}번 약품함 잠금해제", command=lambda i=i: toggle_lock(i), **button_style)
    btn.pack(side="top")

    # 약품 목록을 작성할 수 있는 메모장 추가
    notes = tk.Text(frame, width=button_style["width"], height=2, wrap=tk.WORD, font=("Arial", 12))
    notes.pack(side="top", pady=(5, 0), fill='x')
    notes.insert(tk.END, "약품 목록을 여기에 입력하세요")

    leds.append((led, notes))  # LED와 메모장을 튜플로 저장

# 프로그램 시작 시 메모장 내용 로드
load_notes()

logo_image = tk.PhotoImage(file="/home/sunyong/doctor_interface/horangnabi.png")

bottom_frame = tk.Frame(right_frame, bg='white')
bottom_frame.pack(side='bottom', fill='y', pady=(10, 20))

image_label = tk.Label(bottom_frame, image=logo_image, bg='white')
image_label.pack(pady=(0, 5))

exit_button = tk.Button(bottom_frame, text="프로그램 종료", command=exit_fullscreen, **button_style)
exit_button.pack(side='bottom', pady=(5, 10))

root.mainloop()
