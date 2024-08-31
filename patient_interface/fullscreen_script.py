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
url = 'index.html'  # URL을 실제 웹사이트 주소로 변경하세요.

# 현재 로컬 IP 주소를 가져오고 클립보드에 복사
ip_address = get_local_ip()
if ip_address:
    pyperclip.copy(ip_address)
    print(f"IP 주소 '{ip_address}'가 클립보드에 복사되었습니다.")
else:
    print("IP 주소를 가져오지 못했습니다.")

# 웹 브라우저에서 URL 열기
webbrowser.open(url)

# 2초 대기
time.sleep(2)

# F11 키 누르기 (전체화면 모드로 전환)
pyautogui.press('f11')
