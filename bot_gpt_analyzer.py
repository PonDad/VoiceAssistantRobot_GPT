'''
bot_gpt_analyzer.py

音声認識で受け取ったコマンドを解析し、適切な応答を行う解析プログラムです。
このプログラムは、さまざまなツールや関数を組み合わせて、音声チャットロボットを作成しています。
ユーザーがテキストに変換された音声を入力すると、GPT-3を使用してエージェントが応答を生成し、その結果が表示されます。
'''

import openai, os, json, dotenv, datetime
from pathlib import Path

# LagnChainのチャットモデルをOpenAiと指定してインポートする
from langchain.chat_models import ChatOpenAI
# LangChainのシステムメッセージを定義するライブラリをインポートする
from langchain.schema import SystemMessage

# エージェント カスタムプロンプト作成 のライブラリインポート
from langchain.agents import OpenAIFunctionsAgent
# エージェント ツールモジュール のライブラリインポート
from langchain.agents import tool
# from langchain.agents import load_tools
from langchain.agents import Tool
from langchain import LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
# エージェントのランタイムを作成するライブラリインポート
from langchain.agents import AgentExecutor
# プロンプトに記憶用の場所を追加するライブラリ
from langchain.prompts import MessagesPlaceholder
# メモリー 全ての会話履歴を保持する ライブラリインポート
from langchain.memory import ConversationBufferMemory

# 顔認証ツール
from bot_face_track_recognizer import face_recognize
# 物体認識ツール
from bot_object_detecter import object_detection
# WioNodeの温度と湿度を読み取るツール
from bot_wio_node import get_wio
# サーボモータを動かすツール
from bot_motor_controller import pan_tilt_slow, neopixels_face, neopixels_off

# .envファイルから環境変数をロード
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# エージェントの制御に使用する言語モデルをロード
llm = ChatOpenAI(temperature=0)

# 現在時刻を読み取るツール
@tool
def get_date_time() -> json:
    """datetime関数をつかい、「現在時刻」「今日の日付」を返します"""
    day_now = datetime.datetime.today().strftime("%-Y年%-m月%-d日")
    time_now = datetime.datetime.now().strftime("%-H時%-M分")
    date_time_data = {
        "day_now": day_now,
        "time_now": time_now,
    }
    return json.dumps(date_time_data)

@tool
def get_room_data() -> json:
    """
        IOT機器「WioNode」をつかって部屋のデータを返します
        「気温」「湿度」「不快指数」「照度」「鉢植えの湿度（水分比）」を返します
    """
    temprature, humidity, discomfort, lux, moisture = get_wio()
    room_data = {
        "temp": temprature,
        "humidity": humidity,
        "discomfort": discomfort,
        "lux": lux,
        "moisture": moisture
    }
    return  json.dumps(room_data)

@tool
def get_user_info() -> json:
    """カメラをつかって顔認証をおこない、「ユーザーID」、「ユーザー名」、「ユーザーカテゴリ」を返します"""
    # ユーザーIDをjsonファイルから読み込む
    with open(Path("data/user_data.json")) as file:
        load_user = json.load(file)
    
    # 顔認識を行いユーザー名を取得
    recognized_id = face_recognize()
    print("🖥️ SYSTEM: recognized_id: " + recognized_id )

    if recognized_id in load_user:
        user_name = load_user[recognized_id]["name"]
        user_category = load_user[recognized_id]["category"]
    else:
        recognized_id = "unknown"
        user_name = "ゲスト"
        user_category = "unknown"

    user_info = {
        "recognized_id": recognized_id,
        "user_name": user_name,
        "user_category": user_category 
    }

    return  json.dumps(user_info)

@tool
def look_around() -> json:
    """カメラをつかって物体認識をおこない、周りにある物体の認識結果の配列を返します"""
     # cocoデータセットの英語-日本語翻訳をjsonファイルから読み込む
    with open(Path("dnn_models/coco_en_ja.json")) as file:
        translation_dict = json.load(file)
    recognized_obj = object_detection()
    translated_words = [translation_dict.get(word, word) for word in recognized_obj]
    result_array = []
    for word in translated_words:
        result_array.append(word)

    arround_objects = {
        "result_objects": result_array,
    }
    return  json.dumps(arround_objects)

@tool
def turn_pan_tilt(pan, tilt):
    """
        ###目的###
        テキストで方向を指示された場合
        パラメータ "pan"（水平）、"tilt"（垂直）を数値化し、その値を返します

        ###数値化するパラメータ###
        - "pan": -90 < pan < 90
        - "tilt": -90 < tilt < 90

        ###出力の例###
        Q: "右を向いて"
        A: "pan": -90,"tilt": 0

        Q: "左を向いて"
        A: "pan": 90,"tilt": 0
        
        Q: "上を向いて"
        A: "pan": 0, "tilt": -90

        Q: "下を向いて"
        A: "pan": 0, "tilt": 90

        Q: "右上を向いて"
        A: "pan": -90, "tilt": -90
        
        Q: 左下を向いて
        A:
    """
    neopixels_off()
    neopixels_face()
    pan_tilt_slow(pan, tilt, 10)
    pan_tilt_slow(0, 0, 10)

    turn_degree = {
        "pan": pan,
        "tilt": tilt,
    }

    return  json.dumps(turn_degree)

# 計算ツールをロード
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
# 検索ツールを定義
search = DuckDuckGoSearchRun()

# 複数のツールを定義
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="数学に関する質問に答える必要がある場合に使用します"
    ),
    Tool(
        name="duckduckgo-search",
        func=search.run,
        description="""
            ###目的###
            必要な情報を得るためウェブ上の最新情報を検索します
            
            ###回答例###
            Q: 東京の今日の天気予報を教えて
            A: 東京都の本日の天気予報は晴れのち曇り最高気温32度最低気温25度 今日も暑くなるでしょう

            ###制限###
            回答は140文字以内でおこなってください
            """,
    ),
    get_date_time, 
    get_room_data,
    get_user_info,
    look_around,
    turn_pan_tilt
]

# プロンプトを作成 ヘルパー関数を使用して、OpenAIFunctionsAgent.create_promptプロンプトを自動的に作成
system_message = SystemMessage(content="""
                            あなたは垂直方向と水平方向に移動するカメラを搭載した音声チャットロボットです。
                            名前は「ゆっくり霊夢」です。
                            """)
                        
# プロンプトに記憶用の場所を追加 キーを使用してメッセージのプレースホルダーを追加
MEMORY_KEY = "chat_history"
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
) 

# メモリオブジェクトを作成
memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)

def chat_with_agent(text):
    result = None  # 初期化
    try:
        # これらの部分を組み合わせ、エージェントを作成
        agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

        # エージェントのランタイムである AgentExecutor を作成
        agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

        # ランタイムを実行
        result = agent_executor.run(text)
        #print(str(result))

        return str(result)

    except Exception as e:
        print(f"SYSTEM: エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    print("SYSTEM: チャットを開始します。終了するには '/exit' を入力してください。")

    while True:
        user_input = input("USER: ")
        if user_input == '/exit':
            print("SYSTEM: チャットを終了します。")
            break

        # GPT-3による応答を取得
        assistant_reply = chat_with_agent(user_input)

        # モデルの応答を表示
        print("GPT: " + assistant_reply)