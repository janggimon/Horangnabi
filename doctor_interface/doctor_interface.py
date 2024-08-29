import tkinter as tk
import requests
import socket
import subprocess  # To launch the Zoom application

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

        # Meeting ID for the host (change to your actual meeting ID)
        meeting_id = "8528776866"
        zoom_url = f"zoommtg://zoom.us/start?confno={meeting_id}"

        # Start Zoom with the specific URL
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

# Make the window fullscreen
root.attributes('-fullscreen', True)
root.configure(bg='white')

# Create a frame for the black rectangle on the left side
left_frame = tk.Frame(root, bg='black', width=int(root.winfo_screenwidth() * 0.8), height=root.winfo_screenheight())
left_frame.pack(side='left', fill='both')

# Create a frame for the buttons on the right side
right_frame = tk.Frame(root, bg='white', width=int(root.winfo_screenwidth() * 0.2))
right_frame.pack(side='right', fill='y')

# Start meeting button
start_button = tk.Button(right_frame, text="진료 시작하기", command=start_meeting_as_host, font=("Arial", 24), width=15, height=2)
start_button.pack(pady=30)

# Prescription buttons
for i in range(1, 4):
    btn = tk.Button(right_frame, text=f"{i}번 약품함 잠금해제", command=lambda i=i: send_prescription(i), font=("Arial", 16), width=20, height=2)
    btn.pack(pady=10)

root.mainloop()
