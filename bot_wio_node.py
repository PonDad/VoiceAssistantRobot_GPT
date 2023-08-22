'''
bot_wio_node_weather.py

WioNode から温度と湿度のデータを取得し、不快指数を計算して返すボット用のスクリプトです
WioNodeは日本サーバーに接続し、WioNode1およびWioNode2のAPIトークンを使用して温湿度データを取得します
計算された温度、湿度、および不快指数はボットの応答に組み込まれることを想定しています
'''

import os, requests, json, math, dotenv

# .envファイルからAPI Tpkenをロード
dotenv.load_dotenv()
wio_access_token_1 = os.getenv("wio_access_token_1")
wio_access_token_2 = os.getenv("wio_access_token_2")

wio_jp_server = "https://wiolink.seeed.co.jp/v1/node/"  # WioNodeの日本サーバーアドレス

def get_temp():
    url_temp = wio_jp_server + "GroveTempHumiSHT35I2C0/temperature?access_token=" + wio_access_token_2
    response = requests.get(url_temp)
    data = json.loads(response.text)
    temp = round(data["temperature"],1)
    return temp

def get_hum():
    url_hum = wio_jp_server + "GroveTempHumiSHT35I2C0/humidity?access_token=" + wio_access_token_2
    response = requests.get(url_hum)
    data = json.loads(response.text)
    hum = round(data["humidity"],1)
    return hum

def get_lux():
    url_lux = wio_jp_server + "GroveDigitalLightI2C0/lux?access_token=" + wio_access_token_1
    response =requests.get(url_lux)
    data = json.loads(response.text)
    lux = data["lux"]
    return lux

def get_moist():
    url_moist = wio_jp_server + "GroveMoistureA0/moisture?access_token=" + wio_access_token_1
    response =requests.get(url_moist)
    data = json.loads(response.text)
    moist = data["moisture"]
    return moist

def get_wio():
    temprature = get_temp()
    humidity = get_hum()
    discomfort = math.floor(0.81 * temprature + 0.01 * humidity * (0.99 * temprature - 14.3) + 46.3)
    lux = get_lux()
    moisture = get_moist()
    return temprature, humidity, discomfort, lux, moisture

if __name__ == "__main__":
    wio =get_wio()
    print("SYSTEM: ", wio)
