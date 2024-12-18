from flask import Flask, render_template, request, redirect, url_for, session
from dbUtils import (verify_user, fetch_pending_orders, fetch_deliver_info,get_order_info,get_order_details
,get_delivery_address)
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

@app.route('/deliver/home', methods=['GET'])
def deliver_home():
    if session.get('role') != 'deliver':
        return redirect(url_for('login'))
    order_by = request.args.get('order_by')
    orders = fetch_pending_orders(order_by=order_by)
    return render_template('deliver_home.html', orders=orders)

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

if __name__ == '__main__':
    app.run(debug=True)
