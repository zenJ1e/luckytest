from flask import Flask, request
import random
import os
from datetime import datetime
from waitress import serve
import json
import hashlib

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

@app.route('/fortune', methods=['GET'])
def get_fortune():
    # 取得發送者名稱（如果沒有提供名稱則使用預設值）
    user_name = request.args.get('user', '未知使用者')

    # 取得查詢的名字，若未提供則使用發送者的名稱
    queried_name = request.args.get('name', None)

    # 如果沒有提供查詢名字，就使用發送者的名字
    if queried_name is None:
        queried_name = user_name

    # 檢查是否有包含關鍵字 "綠茶的"，若有則無條件回傳大凶
    if "綠茶的" in queried_name:
        fortune = "大凶"
        fortune_text = fortune_levels[fortune]
    else:
        # 讓運勢與使用者名字 + 當天日期綁定，確保一天內的結果固定
        today_date = datetime.today().strftime('%Y-%m-%d')
        seed_str = queried_name + today_date
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)  # 轉換為整數
        random.seed(seed)
        fortune = random.choice(list(fortune_levels.keys()))
        fortune_text = fortune_levels[fortune]

    # 讓運勢顯示結果
    today_date = datetime.today().strftime('%Y-%m-%d')
    if queried_name == user_name:
        result_message = f"今天是 {today_date}， @{user_name} 的運勢是 <{fortune}>：{fortune_text}"
    else:
        result_message = f"今天是 {today_date}， @{user_name} {queried_name} 的運勢是 <{fortune}>：{fortune_text}"

    # 直接返回純文字訊息
    return result_message

# 使用 waitress 啟動伺服器
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 使用 Render 指定的 PORT
    serve(app, host='0.0.0.0', port=port)
