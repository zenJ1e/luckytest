from flask import Flask, request
import random
import os
import hashlib
from datetime import datetime
from waitress import serve

app = Flask(__name__)

# 運勢結果清單
fortune_levels = [
    "大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"
]

fortune_texts = {
    "大吉": "⭐⭐⭐⭐⭐。太帥啦麻吉！今天是你跟主播打倒黑大大的好日子！ greentea777",
    "吉": "⭐⭐⭐⭐。你好像有點幸運喔，路過彩券行就小買一張刮刮樂吧 greentea333",
    "中吉": "⭐⭐⭐。綠茶：唉呦，你中吉喔。中吉(不)一般喔 greentea555",
    "小吉": "⭐⭐。這運氣至少不會遇上壞天氣，抽空帶這隻寵物狗出門散散步吧！ greentea5551 (已嘎蛋) ",
    "末吉": "⭐。還行啦，小小的運氣也能招來好事發生的喔！ greentea506",
    "凶": "⚡。今天好像不太適合出門喔麻吉 greentea551 主播祝你出門上班上學順利 greentea405",
    "大凶": "💀。完蛋辣，你頭要禿啦老哥 greenteaTTBB ，找時間去祭改一下順便買瓶落建(後果請見 @標大郎 頭貼)"
}

@app.route('/fortune', methods=['GET'])
def get_fortune():
    user_id = request.args.get('user', 'unknown_id')  # 使用者的 Twitch ID
    queried_name = request.args.get('name', None)  # 要查詢的人名

    if not queried_name:
        queried_name = user_id  # 沒輸入時，就測自己的運勢

    today_date = datetime.today().strftime('%Y-%m-%d')

    # 若包含 "綠茶的"，強制回傳 "大凶"
    if "綠茶的" in queried_name:
        fortune = "大凶"
    else:
        # 使用 hashlib 來產生固定的雜湊值
        hash_input = f"{queried_name}_{today_date}".encode('utf-8')
        hashed_value = hashlib.sha256(hash_input).hexdigest()  # 產生 SHA-256 雜湊
        index = int(hashed_value, 16) % len(fortune_levels)  # 將雜湊轉為數字並取模
        fortune = fortune_levels[index]  # 取得該名字對應的運勢

    fortune_text = fortune_texts[fortune]

    # 準備回應內容
    if queried_name == user_id:
        result_message = f"今天是 {today_date}， @{user_id} 的運勢是 <{fortune}>：{fortune_text}"
    else:
        result_message = f"今天是 {today_date}， @{user_id} {queried_name} 的運勢是 <{fortune}>：{fortune_text}"

    return result_message

# 啟動 Flask 伺服器
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    serve(app, host='0.0.0.0', port=port)