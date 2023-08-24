'''
main.py

このプログラムはRaspberry Piを使用したボイスアシスタント・ロボットのメインプログラムです。
音声入力を受け取り、ウェイクワードとコマンドを認識して、対応する機能を実行します。
モジュールと連携してロボットの動作をChatGPTが制御します。

絵文字を表示させる場合は
https://gist.github.com/alhafoudh/b27870eb92542d3da6453b1a64652089
こちらを参考にインストールしてください
'''

import re
from bot_listener import bot_listen_hear
from bot_gpt_analyzer import chat_with_agent
from bot_motor_controller import neopixels_off, pan_tilt_slow, neopixels_face
from bot_voice_synthesizer import speak

if __name__ == "__main__":
    # 正規表現を使用して特殊文字、改行を削除する関数
    def remove_special_chars_with_regex(text):
        cleaned_text = re.sub(r'[!@#$^&*()_+{}\[\]:;<>,?\'"/\\|\-\n]', '', text)
        return cleaned_text

    # カメラを中央にする 
    pan_tilt_slow(0, 0, 10)
    # neopixelsの目を点灯
    neopixels_face()
    try:
        while True:
            user_input = bot_listen_hear()
            print("😀 USER: ",user_input)
            if user_input == "":
                continue
            else:
                pass

            robot_reply = chat_with_agent(user_input)
            if str(robot_reply) == "None": robot_reply = "データエラーです"
            cleaned_robot_reply = remove_special_chars_with_regex(str(robot_reply))
            print("🤖 GPT: ", cleaned_robot_reply)
            speak(str(cleaned_robot_reply), 1)
    except KeyboardInterrupt:
        # カメラを中央にする
        pan_tilt_slow(0, 0, 10)
        # neopixelsの目を消灯
        neopixels_off()