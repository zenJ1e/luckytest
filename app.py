from flask import Flask, jsonify
import random
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
    # 根據用戶的名字來決定運勢，這裡我們使用隨機選擇的方式
    fortune = random.choice(list(fortune_levels.keys()))
    stars = fortune_levels[fortune]
    
    return jsonify({
        "user": user_name,
        "fortune": fortune,
        "stars": stars
    })

# 使用 waitress 啟動伺服器
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)