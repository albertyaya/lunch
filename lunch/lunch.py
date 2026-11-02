from datetime import date, timedelta
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

# 暫存訂單資料 (實務上可改為資料庫)
orders = []

# HTML 範本
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>線上訂便當系統</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 30px auto; padding: 20px; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h2 { color: #333; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        .item-row { display: flex; gap: 10px; margin-bottom: 10px; }
        .item-row input, .item-row select { padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        .item-row input[type="text"] { flex: 1; }
        .item-row input[type="number"] { width: 80px; }
        .item-row select { width: 100%; }
        button { width: 100%; padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #218838; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #007bff; color: white; }
        input[type="date"] { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
    </style>
</head>
<body>

    <div class="card">
        <h2>🍱 訂便當系統</h2>
        <form action="/order" method="POST">
            <!-- 欄位 1: 日期 -->
            <div class="form-group">
                <label for="date">1. 選擇日期：</label>
                <input type="date" id="date" name="date" value="{{ tomorrow }}" required>
            </div>

            <!-- 欄位 2: 樓層 -->
            <div class="form-group">
                <label for="floor">2. 選擇樓層：</label>
                <select id="floor" name="floor" required>
                    <option value="">-- 選擇樓層 --</option>
                    <option value="一樓">一樓</option>
                    <option value="二樓">二樓</option>
                    <option value="三樓">三樓</option>
                    <option value="三樓">四樓</option>
                </select>
            </div>

            <!-- 欄位 3: 便當品項與價格 (三行) -->
            <div class="form-group">
                <label>3. 便當品項與價格：</label>
                
                <!-- 第一行 -->
                <div class="item-row">
                    <input type="text" name="item1" placeholder="品項名稱" maxlength="50">
                    <input type="number" name="price1" placeholder="價格" style="width: 80px;">
                </div>

                <!-- 第二行 -->
                <div class="item-row">
                    <input type="text" name="item2" placeholder="品項名稱" maxlength="50">
                    <input type="number" name="price2" placeholder="價格" style="width: 80px;">
                </div>

                <!-- 第三行 -->
                <div class="item-row">
                    <input type="text" name="item3" placeholder="品項名稱" maxlength="50">
                    <input type="number" name="price3" placeholder="價格" style="width: 80px;">
                </div>
            </div>

            <button type="submit">確認送出訂單</button>
        </form>
    </div>

    <!-- 顯示歷史訂購紀錄 -->
    <div class="card">
        <h3>📋 訂購紀錄</h3>
        {% if orders %}
        <table>
            <thead>
                <tr>
                    <th>日期</th>
                    <th>樓層</th>
                    <th>品項</th>
                    <th>價格</th>
                </tr>
            </thead>
            <tbody>
                {% for order in orders %}
                <tr>
                    <td>{{ order.date }}</td>
                    <td>{{ order.floor }}</td>
                    <td>{{ order.item }}</td>
                    <td>${{ order.price }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p style="color: #666; text-align: center;">目前尚無訂單</p>
        {% endif %}
    </div>

</body>
</html>
"""


@app.route("/")
def index():
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    return render_template_string(
        HTML_TEMPLATE, tomorrow=tomorrow, orders=orders
    )


@app.route("/order", methods=["POST"])
def place_order():
    order_date = request.form.get("date")
    floor = request.form.get("floor")

    # 處理三行便當品項與價格
    for i in range(1, 4):
        item = request.form.get(f"item{i}")
        price = request.form.get(f"price{i}")
        
        # 只有當品項和價格都有輸入時才保存
        if item and price:
            orders.append({"date": order_date, "floor": floor, "item": item, "price": price})

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)