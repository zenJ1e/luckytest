from flask import Flask, jsonify
import random
import os
from datetime import datetime
from waitress import serve
import json

app = Flask(__name__)

# 定義運勢結果
fortune_levels = {
    "大吉": "⭐⭐⭐⭐⭐。太帥啦麻吉！今天是你跟主播打倒黑大大的好日子！ greentea777",
    "吉": "⭐⭐⭐⭐。你好像有點幸運喔，路過彩券行就小買一張刮刮樂吧 greentea333",
    "中吉": "⭐⭐⭐。綠茶：唉呦，你中吉喔。中吉(不)一般喔 greentea555",
    "小吉": "⭐⭐。這運氣至少不會遇上壞天氣，抽空帶這隻寵物狗出門散散步吧！ greentea5551 (已嘎蛋) ",
    "末吉": "⭐。還行啦，小小的運氣也能招來好事發生的喔！ greentea506",
    "凶": "⚡。今天好像不太適合出門喔麻吉 greentea551 主播祝你出門上班上學順利 greentea405",
    "大凶": "💀。完蛋辣，你頭要禿啦老哥  greenteaTTBB ，找時間去祭改一下順便買瓶落建(後果請見 @標大郎 頭貼)"
}

@app.route('/fortune/<user_name>', methods=['GET'])
def get_fortune(user_name):
    # 讓運勢與使用者名字 + 當天日期綁定，確保一天內的結果固定
    today_date = datetime.today().strftime('%Y-%m-%d')  # 取得今天的日期
    seed = hash(user_name + today_date)  # 用當天日期作為種子
    random.seed(seed)  # 設定隨機種子，確保相同輸入產生相同結果
    fortune = random.choice(list(fortune_levels.keys()))  # 固定當日運勢
    fortune_text = fortune_levels[fortune]  # 取出運勢的完整內容

    # 正確的格式化輸出
    result = {
        "message": f"今天是 {today_date}，{user_name} 的運勢是 <{fortune}>：{fortune_text}"
    }

    # 使用 json.dumps 來避免 Unicode 轉義
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# 使用 waitress 啟動伺服器
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render 會提供 PORT 環境變數
    serve(app, host='0.0.0.0', port=port)