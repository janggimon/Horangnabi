import tkinter as tk
import requests
import socket
import subprocess
import time
import os

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
        zoom_path = "/usr/bin/zoom"  # Update this to the actual path of your Zoom application
        meeting_id = "8528776866"  # Meeting ID for the host (change to your actual meeting ID)
        zoom_url = f"zoommtg://zoom.us/start?confno={meeting_id}"

        # Start the Zoom application with the meeting URL
        subprocess.Popen([zoom_path, "--url=" + zoom_url])
        root.after(5000, handle_zoom_windows)  # Wait 5 seconds to ensure Zoom windows are open

    except Exception as e:
        print(f"Failed to start Zoom meeting as host: {e}")

def handle_zoom_windows():
    try:
        # Check for and close the 'Zoom Workplace - Free account' window
        subprocess.call("wmctrl -c 'Zoom Workplace - Free account'", shell=True)
        
        # Loop to check if the Zoom meeting window is open
        meeting_window_open = False
        for _ in range(10):  # Check up to 10 times
            result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
            if 'Meeting' in result.stdout:
                meeting_window_open = True
                break
            time.sleep(1)
        
        if not meeting_window_open:
            print("Zoom meeting window not found.")
            return

        # Get window dimensions and update position
        left_frame.update_idletasks()
        left_frame_width = left_frame.winfo_width()
        left_frame_height = left_frame.winfo_height()
        left_frame_x = left_frame.winfo_rootx()
        left_frame_y = left_frame.winfo_rooty()

        # Set new width to 78% of screen width
        new_width = int(root.winfo_screenwidth() * 0.78)
        new_x = 0  # Align the left edge of the Zoom meeting window with the left edge of the screen

        # Adjust the zoom meeting window position and size
        zoom_window_cmd = (f"wmctrl -r 'Meeting' -e 0,{new_x},{left_frame_y},{new_width},{left_frame_height}")
        subprocess.Popen(zoom_window_cmd, shell=True)

    except Exception as e:
        print(f"Failed to handle Zoom windows: {e}")

def send_prescription(prescription_id):
    try:
        response = requests.post(SERVER_URL, data={'id': prescription_id})
        if response.status_code == 200:
            print(f"Prescription {prescription_id} processed successfully.")
        else:
            print(f"Failed to process prescription {prescription_id}.")
    except Exception as e:
        print(f"Error sending request: {e}")

def exit_fullscreen():
    root.attributes('-fullscreen', False)
    root.quit()

root = tk.Tk()
root.title("의사 진료 인터페이스")

root.attributes('-fullscreen', True)
root.configure(bg='white')

left_frame = tk.Frame(root, bg='light sky blue', width=int(root.winfo_screenwidth() * 0.85), height=root.winfo_screenheight(), highlightbackground="black", highlightthickness=75)
left_frame.pack(side='left', fill='both')

info_label = tk.Label(left_frame, text="우측의 '진료하기' 버튼을 눌러 화상 진료실로 입장할 수 있습니다", 
                      font=("Arial", 20), fg='navy', bg='light sky blue')
info_label.place(relx=0.5, rely=0.5, anchor='center')

right_frame = tk.Frame(root, bg='white', width=int(root.winfo_screenwidth() * 0.2))
right_frame.pack(side='right', fill='y', padx=20, pady=20)

button_style = {"font": ("Arial", 16), "width": 20, "height": 2, "bg": "#f0f0f0", "fg": "#333", "relief": "raised", "bd": 2}

start_button = tk.Button(right_frame, text="진료 시작하기", command=start_meeting_as_host, font=("Arial", 24), width=15, height=2, bg="#4CAF50", fg="white", relief="groove", bd=3)
start_button.pack(pady=30)

for i in range(1, 4):
    btn = tk.Button(right_frame, text=f"{i}번 약품함 잠금해제", command=lambda i=i: send_prescription(i), **button_style)
    btn.pack(pady=10)

logo_image = tk.PhotoImage(file="horangnabi.png")  # Change the file path to your image

bottom_frame = tk.Frame(right_frame, bg='white')
bottom_frame.pack(side='bottom', fill='y', pady=(10, 20))

image_label = tk.Label(bottom_frame, image=logo_image, bg='white')
image_label.pack(pady=(0, 5))

exit_button = tk.Button(bottom_frame, text="프로그램 종료", command=exit_fullscreen, **button_style)
exit_button.pack(side='bottom', pady=(5, 10))

root.mainloop()
