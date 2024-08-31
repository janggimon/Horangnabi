import time
import pyautogui
import webbrowser
import pyperclip
import socket

def get_local_ip():
    try:
        # 임시로 소켓을 열어 현재 IP 주소를 얻음
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 구글의 DNS 서버에 연결 시도
        ip_address = s.getsockname()[0]  # 로컬 IP 주소 반환
        s.close()
        return ip_address
    except Exception as e:
        print(f"IP 주소를 가져오는 데 실패했습니다: {e}")
        return None

# 웹 페이지 URL
url = 'file:///home/pi/drone/index.html'  # 파일 경로를 URL로 변환

# 현재 로컬 IP 주소를 가져오고 클립보드에 복사
ip_address = get_local_ip()
if ip_address:
    pyperclip.copy(ip_address)
    print(f"IP 주소 '{ip_address}'가 클립보드에 복사되었습니다.")
else:
    print("IP 주소를 가져오지 못했습니다.")

# 웹 브라우저에서 URL 열기
webbrowser.open(url)

# 브라우저가 완전히 로드될 때까지 기다리기
time.sleep(5)  # 로딩에 충분한 시간을 줍니다. 필요에 따라 조정하세요.

# 브라우저 창에 포커스를 맞추기 위해 클릭
pyautogui.click(x=200, y=200)  # 브라우저 창의 대략적인 위치에 클릭. 조정이 필요할 수 있음.

# F11 키 누르기 (전체화면 모드로 전환)
time.sleep(1)  # 클릭 후 약간의 지연을 추가
pyautogui.press('f11')
print("전체화면 모드로 전환되었습니다.")
