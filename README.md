# VoiceAssistantRobot_GPT

[![YouTube](https://github.com/PonDad/VoiceAssistantRobot_GPT/blob/main/images/image_3.jpg)](https://www.youtube.com/watch?v=703jyL2EDnk)

## ハードウェア・ソフトウェア

[PonDad/VoiceAssistantRobot](https://github.com/PonDad/VoiceAssistantRobot) に追加して以下のソフトウェアが必要になります。

- Python3.9.2: [requirements](https://github.com/PonDad/VoiceAssistantRobot_GPT/blob/main/requirements.txt)
- 生成AI: [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) / [openai](https://pypi.org/project/openai/)
- LLMフレームワーク: [LangChain](https://python.langchain.com/docs/get_started/installation)
- 検索エンジンAPI: [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)

> **Note**
> ChatGPT APIのAPIキーは`.env`ファイルに指定してください。

## 仕組み
![chart2](https://github.com/PonDad/VoiceAssistantRobot_GPT/blob/main/images/chart_2.png)

#### LangChain Agent

[VoiceAssistantRobot](https://github.com/PonDad/VoiceAssistantRobot) チャート図における`analize`をLangChainの「エージェント」機能を使って置き換えます。ドキュメントには以下のように書かれています。

>アプリケーションによっては、LLM/他のツール（`tools`）へのあらかじめ決められた呼び出しの連鎖（`chain`）だけでなく、ユーザーの入力に依存する未知の連鎖を必要とする可能性があります。このような連鎖では、一連のツールにアクセスできる "エージェント（`Agent`）"を活用できます。ユーザーの入力に応じて、エージェントはこれらのツールのうちどれを呼び出すかを決定することができます。
>引用: [Agent | 🦜️🔗 LangChain](https://docs.langchain.com/docs/components/agents/)

事前に定義した`tools`の順番や実行を「エージェント」が実行します。名前が似ていて少しややこしいのですが、「エージェント」の`Tool`モジュールを使うことで用途別のツールを利用することができます。例を挙げると、数学の計算を行う`llm-math`モジュールやGoogleカスタム検索を行う`google-serper`などがあります。

実験用に登録した`Tool`は以下の２つのモジュールです

- 複雑な計算を行うツール（`LLMMathChain`モジュール）
- DuckDuckGoで検索を行うツール（`DuckDuckGoSearchRun`モジュール）

検索モジュールはGoogle、Microsoftともに利用数に応じてAPIが有料となるため、無料で利用できるDuckDuckGo検索モジュールを選択しました。

「エージェント」はlangchainが用意したモジュールだけでなく、ChatGPTの`Function calling`（関数呼び出し）機能をツールとして利用することが出来ます。以下LangChainのドキュメント引用です、

> 特定のOpenAIモデル（gpt-3.5-turbo-0613やgpt-4-0613など）は、関数が呼び出されるタイミングを検出し、関数に渡されるべき入力を応答するように微調整されています。API呼び出しの中で、関数を記述し、モデルがそれらの関数を呼び出すための引数を含むJSONオブジェクトを出力するようにインテリジェントに選択することができます。OpenAI関数APIのゴールは、一般的なテキスト補完やチャットAPIよりも、より確実に有効で有用な関数呼び出しを返すことです。`OpenAI Functions Agent`は、これらのモデルで動作するように設計されています。
> 引用: [OpenAI functions | 🦜️🔗 LangChain](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent)

ChatGPTのプロンプトを定義する際、ヘルパー関数`OpenAIFunctionsAgent`を使うことで、ChatGPTの`Function calling`機能をツールに指定することが出来ます。`Function calling`をツールとして指定する際はデコレート関数`@tool`で定義します。

実験用に定義した`@tool`は以下の通りです

- 日時データ取得（`datetime`モジュール）
- WioNodeからのデータ取得(`requests`モジュールを利用したGETメソッド)
- 顔認証・物体認識（OpenCVとDNNモデルを使ったリアルタイム顔認識、物体認識）
- サーボモーター・LEDライト制御（PanTiltHATライブラリを利用）

テキストに変換された音声データをChatGPT API経由で送信すると、「エージェント」が自律的にに定義したツールを選択し、実行します。その際、ChatGPTの関数呼び出し機能を「エージェント」が適切に活用し、返される関数呼び出し結果を回答します。

## 使い方

[PonDad/VoiceAssistantRobot](https://github.com/PonDad/VoiceAssistantRobot) と同じですが、各ツールの選択をLangChain「エージェント」がおこなうため、`data/command_data.json`のコマンドワード設定は不要です。

```bash
python main.py
```
で実行してください。`ctrl + c`でウェイクワード待機のループが終了します。