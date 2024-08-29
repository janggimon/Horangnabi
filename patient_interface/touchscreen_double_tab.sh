#!/bin/bash

# 터치스크린 장치 ID 찾기
DEVICE_ID=$(xinput list | grep -i "touchscreen" | grep -o 'id=[0-9]*' | grep -o '[0-9]*')

# 더블탭을 감지하고 F11 키를 시뮬레이트
while true; do
    # 터치 이벤트 감지
    xinput test $DEVICE_ID | while read -r line; do
        if [[ $line == *"button press"* ]]; then
            # 버튼이 눌렸을 때 타이밍 확인
            sleep 0.2
            if xinput test $DEVICE_ID | grep -q "button press"; then
                echo "Double tap detected!"
                xdotool key F11
                sleep 1
            fi
        fi
    done
done
