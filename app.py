from flask import Flask, jsonify
import random
import os
from datetime import datetime
from waitress import serve

app = Flask(__name__)

# 定義運勢結果
fortune_levels = {
    "大吉": "⭐⭐⭐⭐⭐",
    "吉": "⭐⭐⭐⭐",
    "中吉": "⭐⭐⭐",
    "小吉": "⭐⭐",
    "末吉": "⭐",
    "凶": "⚡",
    "大凶": "💀"
}

@app.route('/fortune/<user_name>', methods=['GET'])
def get_fortune(user_name):
    # 讓運勢與使用者名字 + 當天日期綁定，確保一天內的結果固定
    today_date = datetime.today().strftime('%Y-%m-%d')  # 取得今天的日期
    seed = hash(user_name + today_date)  # 用當天日期作為種子
    random.seed(seed)  # 設定隨機種子，確保相同輸入產生相同結果
    fortune = random.choice(list(fortune_levels.keys()))  # 固定當日運勢
    stars = fortune_levels[fortune]

    return jsonify({
        "user": user_name,
        "fortune": fortune,
        "stars": stars
    })

# 使用 waitress 啟動伺服器
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render 會提供 PORT 環境變數
    serve(app, host='0.0.0.0', port=port)
