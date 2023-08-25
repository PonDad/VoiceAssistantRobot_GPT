# VoiceAssistantRobot_RPi_GPT

[![YouTube](https://github.com/PonDad/VoiceAssistantRobot_RPi_GPT/blob/main/images/image_3.jpg)](https://www.youtube.com/watch?v=703jyL2EDnk)

## 仕組み
![chart2](https://github.com/PonDad/VoiceAssistantRobot_RPi_GPT/blob/main/images/chart_2.png)

音声発話（ユーザー） --> 音声認識（Vosk） --> テキスト化 --> 自動ツール選択（LangChain Agent） --> ChatGPT APIと通信 --> 音声合成（Aques Talk Pi）--> 合成音声発話（ロボット）

の様に動作します。LangChainのAgent機能によって、ChatGPTがユーザーの指示に対しどの様なツールを、どの順番で使うか自動的に選択します。

## ハードウェア・ソフトウェア

[PonDad/VoiceAssistantRobot_RPi](https://github.com/PonDad/VoiceAssistantRobot_RPi) に追加して以下のソフトウェアが必要になります。

- Python3.9.2: [requirements](https://github.com/PonDad/VoiceAssistantRobot_RPi_GPT/blob/main/requirements.txt)
- 生成AI: [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) / [openai](https://pypi.org/project/openai/)
- LLMフレームワーク: [LangChain](https://python.langchain.com/docs/get_started/installation)
- 検索エンジンAPI: [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)

> **Note**
> ChatGPT APIのAPIキーを`.env`にて指定してください

## 使い方

[PonDad/VoiceAssistantRobot_RPi](https://github.com/PonDad/VoiceAssistantRobot_RPi) と同じですが、各ツールの選択をAgentがおこなうため、`data/command_data.json`のコマンドワード設定は不要です。

```bash
python main.py
```
で実行してください。`ctrl + c`でウェイクワード待機のループが終了します。