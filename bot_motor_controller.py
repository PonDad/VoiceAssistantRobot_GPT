'''
bot_motor_controller.py

パンチルトモーターおよびLEDランプの制御を行うモジュールです。
pantilthatモジュールを使用して、サーボモーターによる頭部のパン（左右）とチルト（上下）の向き調整を行います。
また、pantilthatモジュールを使用してLEDランプの点灯/消灯を制御します。
'''

import time, math
import pantilthat

################################
# NeoPixels のLEDランプ制御
################################

pantilthat.light_mode(pantilthat.WS2812) # NeoPixelsStick8はWS2812
pantilthat.light_type( 1 ) # RGBで設定初期化

# ネオピクセルLEDの制御 8つのLED全て指定
def neopixels_all(r, g, b):
    pantilthat.set_all(r, g, b)
    pantilthat.show()
    
# ネオピクセルLEDの制御 8つのLED一つづつ指定
def neopixels_set_pixel(index, r, g, b):
    pantilthat.set_pixel(index, r, g, b)
    pantilthat.show()

# ネオピクセルLEDの消灯
def neopixels_off():
    pantilthat.clear()
    pantilthat.show()

# 目の設定
def neopixels_face():
    pantilthat.set_pixel(1, 50, 50, 50)
    pantilthat.set_pixel(6, 50, 50, 50)
    pantilthat.show()

# speskコマンド実施中 目を点滅させる
def neopixels_speak_flash_timeout():
    time_start = time.perf_counter()
    time_end = 0

    while True:
        brightness = (math.sin(time_end*4)+1) /2 # sin波の波形をプラスのみ計算
        print(brightness)

        red, green, blue = 50, 50, 50  # ベースの色 (白)
        red = int(brightness * red)  # ベースの色に明るさを乗算
        green = int(brightness * green)
        blue = int(brightness * blue)

        pantilthat.set_pixel(1, red, green, blue)
        pantilthat.set_pixel(6, red, green, blue)
        pantilthat.show()

        time.sleep(0.1)  # 0.1秒ごとに明るさを更新
        pantilthat.clear()
        time_end = time.perf_counter() - time_start
        if time_end > 5:
            
            pantilthat.show()
            break

# speskコマンド実施中 目を点滅させる
def neopixels_speak_flash_loop():
    time_start = time.perf_counter()
    time_end = 0

    while True:
        brightness = (math.sin(time_end*4)+1) /2 # sin波の波形をプラスのみ計算

        red, green, blue = 50, 50, 50  # ベースの色 (白)
        red = int(brightness * red)  # ベースの色に明るさを乗算
        green = int(brightness * green)
        blue = int(brightness * blue)

        pantilthat.set_pixel(1, red, green, blue)
        pantilthat.set_pixel(6, red, green, blue)
        pantilthat.show()

        time.sleep(0.1)  # 0.1秒ごとに明るさを更新
        pantilthat.clear()
        time_end = time.perf_counter() - time_start

# 音声認識をした際、サウンドともに認識したことを表示する
def neopixels_notification():
    colors = [(0, 20, 50), (50, 50, 20),(50, 0, 20), (0, 50, 20)]
    leds = [7, 5, 3, 1]

    time_start = time.perf_counter()
    time_end = 0

    while True:
        for i, led in enumerate(leds):
            color = colors[i]
            pantilthat.set_pixel(led, color[0], color[1], color[2])

        pantilthat.show()

        leds = [(led - 1) % 8 for led in leds]
        time.sleep(0.1)
        pantilthat.clear()
        time_end = time.perf_counter() - time_start
        if time_end > 1:
            pantilthat.show()
            break

# 認識したあとコマンド入力待ちの状態を示す
def neopixels_hearing_flash():
    colors = [(0, 20, 50), (50, 50, 20), (50, 0, 20), (0, 50, 20)]
    leds = [7, 5, 3, 1]

    time_start = time.perf_counter()
    while True:
        time_elapsed = time.perf_counter() - time_start
        brightness = (math.sin(time_elapsed * 4) + 1) / 2

        for i, led in enumerate(leds):
            color = colors[i]
            red = int(brightness * color[0])
            green = int(brightness * color[1])
            blue = int(brightness * color[2])

            pantilthat.set_pixel(led, red, green, blue)

        pantilthat.show()
        time.sleep(0.1)

        if time_elapsed > 5:
            pantilthat.clear()
            pantilthat.show()
            break

def neopixels_hearing():
    colors = [(0, 20, 50), (50, 50, 20), (50, 0, 20), (0, 50, 20)]
    leds = [7, 5, 3, 1]

    for i in range(len(leds)):
        pantilthat.set_pixel(leds[i], colors[i][0], colors[i][1], colors[i][2])
    
    pantilthat.show()

################################
# PanTiltHAT のサーボモーター制御
################################

# パンチルトモーター制御 ｰpan tilt とも -90 ~ 90
def pan_tilt(pan, tilt):
    pantilthat.pan(pan)
    pantilthat.tilt(tilt)

# マイクロサーボSG90では60°動かすのに0.1秒
# パンチルトモーターをゆっくり動かす speed=10 前後で調整
def pan_tilt_slow(pan, tilt, speed):

    start_pan = pantilthat.get_pan()
    start_tilt = pantilthat.get_tilt()
    #print(start_pan, start_tilt)

    move_pan = (pan - start_pan) / 100
    move_tilt = (tilt - start_tilt)  / 100
    #print(move_pan, move_tilt)

    cnt = 0
    while True:
        pan_tilt(start_pan + move_pan*cnt, start_tilt + move_tilt*cnt)
        cnt += 1
        if cnt == 100:
            break
        else:
            pass
        time.sleep(0.001 * speed)

if __name__ == "__main__":
    pan_tilt(0, 90)
    time.sleep(0.5)
    pan_tilt(0, 0)
    time.sleep(0.5)
    pan_tilt_slow(0,90, 10)
    pan_tilt_slow(0,0,10)

    neopixels_face()
    time.sleep(3)
    neopixels_notification()
    neopixels_hearing()
    neopixels_speak_flash_loop()