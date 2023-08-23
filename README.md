# VoiceAssistantGPT
![img1]()

## ハードウェア・ソフトウェア

[PonDad/VoiceAssistantBot](https://github.com/PonDad/VoiceAssistantBot/tree/main) に追加して以下のソフトウェアが必要になります。

- 生成AI: [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) / [openai](https://pypi.org/project/openai/)
- 大規模言語モデルフレームワーク: [LangChain](https://python.langchain.com/docs/get_started/installation)

ChatGPT APIのAPIキーを`.env`にて指定してください

## 仕組み
![img2]()

音声発話（ユーザー） --> 音声認識（Vosk） --> テキスト化 --> 自動ツール選択（LangChain Agent） --> ChatGPT APIと通信 --> 音声合成（Aques Talk Pi）--> 合成音声発話（ロボット）

の様に動作します。LangChainのAgent機能によって、ChatGPTがユーザーの指示に対しどの様なツールを、どの順番で使うか自動的に選択します。

## 使い方

[PonDad/VoiceAssistantBot](https://github.com/PonDad/VoiceAssistantBot/tree/main) と同じですが、各ツールの選択をAgentがおこなうため、`data/command_data.json`のコマンドワード設定は不要です。

```bash
python main.py
```
で実行してください。

## 実行動画

![video1]()

「ちょっと下を向いて」という指示をChatGPTが解釈して下30度にカメラを移動させています。