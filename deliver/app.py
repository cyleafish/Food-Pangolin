from flask import Flask, render_template, request, redirect, url_for, session
from dbUtils import (verify_user, fetch_pending_orders, fetch_deliver_info,get_order_info,get_order_details
,get_delivery_address,update_order_status,fetch_deliver_id,get_current_orders,get_deliver_history)
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = verify_user(username, password)
        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['username'] = user['username']
            if user['role'] == 'deliver':
                return redirect(url_for('deliver_home'))
        return "登入失敗，請檢查帳號密碼"
    return render_template('login.html')

@app.route('/deliver_home')
def deliver_home():
    user_id = session.get('user_id')  
    deliver_id = fetch_deliver_id(user_id)
    order_by = request.args.get('order_by', 'time')
    # 待接單訂單
    orders = fetch_pending_orders(order_by)
    # 目前接的訂單
    current_orders = get_current_orders(deliver_id)
    # 歷史訂單
    deliver_history = get_deliver_history(deliver_id)

    return render_template(
        'deliver_home.html',
        orders=orders,
        current_orders=current_orders,
        deliver_history=deliver_history
    )


@app.route('/deliver/info', methods=['GET'])
def deliver_info():
    if session.get('role') != 'deliver':
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    info = fetch_deliver_info(user_id)
    return render_template('deliver_info.html',info=info,deliver_id=user_id)

@app.route('/order_info/<int:order_id>')
def order_info(order_id):
    # 獲取訂單基本資訊
    order_info = get_order_info(order_id)

    # 獲取訂單詳細內容
    order_details = get_order_details(order_id)

     # 獲取送貨地址
    delivery_address = get_delivery_address(order_id)

    return render_template('order_info.html', 
                           order_info=order_info, 
                           order_details=order_details,
                           delivery_address=delivery_address)

@app.route('/accept_order', methods=['GET'])
def accept_order():
    # 獲取訂單 ID 和外送員的 deliver_id
    order_id = request.args.get('order_id')
    user_id = session.get('user_id')  
    deliver_id = fetch_deliver_id(user_id)
    if not order_id or not deliver_id:
        return "錯誤：無法接單，請重新嘗試。", 400

    try:
        success = update_order_status(order_id, deliver_id)

        if not success:
            return "接單失敗：訂單可能已被接走。", 400

        return redirect(url_for('deliver_home'))

    except Exception as e:
        return f"發生錯誤：{e}", 500

if __name__ == '__main__':
    app.run(debug=True)
