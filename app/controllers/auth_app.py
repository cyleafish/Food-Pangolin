from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from app.dbUtils.login import (verify_user,check_existing_user,
                               register_merchant_account,register_deliver_account,
                               register_customer_account,verify_restaurant)  # 假設 verify_user 是通用的驗證函式

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = verify_user(username, password)  # 驗證帳號密碼

        if user:
            # 登入成功，設置 session
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['username'] = user['username']
            print(session['role'])
            # 根據角色導航到不同頁面
            if user['role'] == 'deliver':
                return redirect(url_for('deliver.deliver_home'))
            elif user['role'] == 'platform':
                return redirect(url_for('platform.index'))
            elif user['role'] == 'customer':
                return redirect(url_for('customer.homepage'))
            elif user['role'] == 'restaurant':
                rest_id = verify_restaurant(username)
                session['rest_id'] = rest_id['rest_id']
                print(rest_id['rest_id'])
                return redirect(url_for('restaurant.host_res'))
            else:
                flash("未知角色，請聯繫管理員。")
                
        else:
            flash("登入失敗，請重新登入")
            return redirect(url_for('auth.login'))

    # GET 方法時顯示登入頁面
    return render_template('login.html')

@auth_bp.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        addr = request.form.get('addr')
        email = request.form.get('email')

        role = 'customer'  # 顧客角色
        existing_user = check_existing_user(username)
        if existing_user:
            flash('已經有此帳號了')  
            return redirect(url_for('auth.register'))
        else:  # 帳號不存在，執行註冊
            register_customer_account(username, password, role, phone, addr, email)
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/register/merchant', methods=['GET', 'POST'])
def register_merchant():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        addr = request.form.get('addr')
        phone = request.form.get('phone')
        role = 'restaurant'  # 商家角色

        existing_user = check_existing_user(username)
        if existing_user:
            flash('已經有此帳號了')  
            return redirect(url_for('auth.merchant_register'))
        else:  # 帳號不存在，執行註冊
            register_merchant_account(username, password, addr, phone,role)
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))

    return render_template('restaurant/register_merchant.html')

@auth_bp.route('/register/deliver', methods=['GET', 'POST'])
def register_deliver():
    if request.method == 'POST':
        # 從表單取得資料
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        car_num = request.form['car_num']
        role = 'deliver'
        # 檢查帳號是否已存在
        existing_user = check_existing_user(username)
        
        if existing_user:
            flash('已經有此帳號了')  
            return redirect(url_for('auth.register_deliver'))
        else:  # 帳號不存在，執行註冊
            register_deliver_account(username, password, phone, car_num,role)
            flash('註冊成功，請登入')
            return redirect(url_for('auth.login'))

    # 如果是 GET 請求，直接顯示註冊表單
    return render_template('deliver/register_deliver.html')


# 登出功能
@auth_bp.route('/logout')
def logout():
    # 清除 session 中的使用者資料
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('username', None)

    # 重定向到登入頁面
    return redirect(url_for('auth.login'))  
