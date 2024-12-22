from flask import Flask,Blueprint, render_template, request, redirect, url_for, session,flash
from app.dbUtils.platform_dbUtils import fetch_merchant_earnings, fetch_deliver_orders, fetch_customer_payments
from app.dbUtils.login import verify_user

# 創建 Blueprint
platform_bp = Blueprint('platform', __name__, template_folder='../templates/platform')

# @platform_bp.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = verify_user(username, password)
#         if user:
#             session['user_id'] = user['user_id']
#             session['role'] = user['role']
#             session['username'] = user['username']
#             if user['role'] == 'platform':
#                 return redirect(url_for('index'))
#         return "登入失敗，請檢查帳號密碼"
#     return render_template('login.html')
@platform_bp.route('/')
@platform_bp.route('/home')
def index():
    return render_template('index.html')

@platform_bp.route('/merchant_earnings')
def merchant_earnings():
    results = fetch_merchant_earnings()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('merchant_earnings.html', merchants=results)

@platform_bp.route('/deliver_orders')
def deliver_orders():
    results = fetch_deliver_orders()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('deliver_orders.html', delivers=results)

@platform_bp.route('/customer_payments')
def customer_payments():
    results = fetch_customer_payments()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('customer_payments.html', customers=results)


