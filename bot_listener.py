'''
bot_listener.py

ウェイクワードを認識してサウンドを鳴らし、コマンド入力を待機する音声認識プログラムです。
ウェイクワードが入力されるとコマンド受付モードに入り、終了コマンドが入力されると待機モードに戻ります。
音声認識結果を返し、ChatGPTにデータを渡します。
'''

import json, time
from pathlib import Path

from vosk import Model, KaldiRecognizer
import pyaudio

from bot_motor_controller import neopixels_face, neopixels_hearing, neopixels_off
from bot_voice_synthesizer import notification


# Jsonファイルからウェイクワードとコマンドの配列を読み込む
with open(Path("data/command_data.json"), "rb") as f:
    data = json.load(f)

WAKE = data["wake"]
EXIT = data["exit"]

# Voskモデルの読み込み
model = Model(str(Path("vosk-model-small-ja-0.22").resolve()))
#model = Model(str(Path("vosk-model-ja-0.22").resolve()))

# マイクの初期化
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()

# voskの初期化
def engine():
    stream = mic.open(format=pyaudio.paInt16,
                       channels=1, 
                       rate=16000, 
                       input=True, 
                       frames_per_buffer=8192)
    
    while True:
        stream.start_stream()
        try:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                response_json = json.loads(result)
                print("🖥️ SYSTEM: ", response_json)
                response = response_json["text"].replace(" ","")
                return response
            else:
                pass
        except OSError:
            pass

# ウェイクワード待機をlistening コマンド待機をhearingと設定
listening = True
hearing = False

# listeningをループして音声認識 ウェイクワード認識でhearingループする
def bot_listen_hear():
    global listening, hearing
    
    # neopixelsの目を点灯
    neopixels_face()
    if hearing == True: print("🖥️ SYSTEM: ","-"*22, "GPTに話しかけてください","-"*22)
    else: print("🖥️ SYSTEM: ","-"*22, "ウェイクワード待機中","-"*22)
    
    while listening:
        response = engine()
        if response in WAKE:
            listening = False
            hearing = True
            neopixels_off()
            notification()
            time.sleep(0.5)
            neopixels_hearing()
            print("🖥️ SYSTEM: ","-"*22, "GPTに話しかけてください","-"*22)
        elif response.strip() == "":
            continue  # 空白の場合はループを続ける
        else:
            pass
    
    while hearing:
        response = engine()
        if response in EXIT:
            listening = True
            hearing = False
            neopixels_off()
            notification()
            time.sleep(0.5)
            neopixels_hearing()
        elif response.strip() == "":
            continue  # 空白の場合はループを続ける
        else:
            neopixels_off()
            notification()
            time.sleep(0.5)
            neopixels_hearing()
        return response 

if __name__ == "__main__":
    while True:
        response = bot_listen_hear()
        print("response: ",response)
