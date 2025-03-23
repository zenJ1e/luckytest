from flask import Flask, request, jsonify
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

@app.route('/fortune', methods=['GET'])
def get_fortune():
    # 從 Nightbot 取得發送者名稱（當沒有提供名稱時）
    user_name = request.args.get('user', '未知使用者')
    queried_name = request.args.get('name', '').strip()  # 提取名字，並移除兩端的空格

    # 如果沒有指定名字，則顯示發送者名稱，不加「」符號
    if not queried_name:
        queried_name = user_name  # 使用發送指令者的名字
    else:
        # 如果有提供名字，才加上「」符號
        queried_name = f"「{queried_name}」"

    # 讓運勢與使用者名字 + 當天日期綁定，確保一天內的結果固定
    today_date = datetime.today().strftime('%Y-%m-%d')
    seed = hash(queried_name + today_date)
    random.seed(seed)
    fortune = random.choice(list(fortune_levels.keys()))
    fortune_text = fortune_levels[fortune]

    # 檢查傳送訊息的名稱與指定名稱是否一致，避免重複顯示名字
    if queried_name == f"「{user_name}」":  # 如果查詢名字就是發送者的名字，則不加重複的名字
        result = f"今天是 {today_date}， @{user_name} 的運勢是 <{fortune}>：{fortune_text}"
    else:
        result = f"今天是 {today_date}， @{user_name} {queried_name} 的運勢是 <{fortune}>：{fortune_text}"

    # 直接返回純文字
    return result

# 使用 waitress 啟動伺服器
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 使用 Render 指定的 PORT
    serve(app, host='0.0.0.0', port=port)
