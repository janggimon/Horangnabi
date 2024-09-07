import time
import pyautogui
import webbrowser
import pyperclip
import socket
import subprocess

# pyautogui FAILSAFE 비활성화
pyautogui.FAILSAFE = False

# 키보드 레이아웃을 영어로 전환
subprocess.run(['setxkbmap', 'us'])

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"IP 주소를 가져오는 데 실패했습니다: {e}")
        return None

url = 'file:///home/pi/drone/index.html'

# 현재 로컬 IP 주소를 가져오고 클립보드에 복사
ip_address = get_local_ip()
if ip_address:
    pyperclip.copy(ip_address)
    print(f"IP 주소 '{ip_address}'가 클립보드에 복사되었습니다.")
else:
    print("IP 주소를 가져오지 못했습니다.")

browser=webbrowser.get('chromium-browser')

# 웹 브라우저에서 URL 열기
browser.open(url)

# 브라우저가 완전히 로드될 때까지 기다리기
# time.sleep(0.3)

# 브라우저 창에 포커스를 맞추기 위해 클릭
pyautogui.click(x=500, y=500)  # 클릭 위치를 조정해 보세요.

# F11 키 누르기 (전체화면 모드로 전환)
# time.sleep(0.2)  # 클릭 후 약간의 지연을 추가
pyautogui.press('f11')
print("전체화면 모드로 전환되었습니다.")
