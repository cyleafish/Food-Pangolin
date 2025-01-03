from flask import Flask, render_template, request, redirect, url_for, session,flash
from dbUtils import (get_db_connection,verify_user, fetch_pending_orders, fetch_deliver_info,
get_order_info,get_order_details,get_delivery_address,update_order_status,
fetch_deliver_id,get_current_orders,get_deliver_history,accepted_order,add_customer_rating,
register_deliver_account)


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

@app.route('/register_deliver', methods=['GET', 'POST'])
def register_deliver():
    if request.method == 'POST':
        # 從表單取得資料
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        car_num = request.form['car_num']

        # 檢查帳號是否已存在
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_account WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        

        if existing_user:
            flash('已經有此帳號了')  
            return redirect(url_for('register_deliver'))
        else:  # 帳號不存在，執行註冊
            register_deliver_account(username, password, phone, car_num)
            flash('註冊成功，請登入')
            return redirect(url_for('login'))

    # 如果是 GET 請求，直接顯示註冊表單
    return render_template('register_deliver.html')


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
        success = accepted_order(order_id, deliver_id)

        if not success:
            return "接單失敗：訂單可能已被接走。", 400

        return redirect(url_for('deliver_home'))

    except Exception as e:
        return f"發生錯誤：{e}", 500

@app.route('/update_order_status/<int:order_id>/<new_status>', methods=['GET'])
def update_order_status_route(order_id, new_status):
    if session.get('role') != 'deliver':
        return redirect(url_for('login'))
    
    success = update_order_status(order_id, new_status)
    if success:
        return redirect(url_for('deliver_home'))
    else:
        return "狀態更新失敗", 500

@app.route('/rate_customer_and_complete/<int:order_id>', methods=['POST'])
def rate_customer_and_complete(order_id):
    if session.get('role') != 'deliver':
        return redirect(url_for('login'))

    rating = request.form.get('rating')
    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        return "無效的評分", 400

    user_id = session.get('user_id')
    deliver_id = fetch_deliver_id(user_id)
    print(order_id, deliver_id, int(rating))
    # 添加評分
    success_rating = add_customer_rating(order_id, deliver_id, int(rating))
    if success_rating!=True:
        return f"失敗：{success_rating}", 500

    # 更新訂單狀態為 'completed'
    success_status = update_order_status(order_id, 'completed')
    if not success_status:
        return "訂單狀態更新失敗", 500

    return redirect(url_for('deliver_home'))


if __name__ == '__main__':
    app.run(debug=True)
