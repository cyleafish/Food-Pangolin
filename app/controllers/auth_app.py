from flask import Blueprint, render_template, request, redirect, url_for, session
from app.dbUtils.login import verify_user  # 假設 verify_user 是通用的驗證函式

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

            # 根據角色導航到不同頁面
            if user['role'] == 'deliver':
                return redirect(url_for('deliver.deliver_home'))
            elif user['role'] == 'platform':
                return redirect(url_for('platform.index'))
            else:
                return "未知角色，請聯繫管理員。", 400
        else:
            return redirect('auth.login')

    # GET 方法時顯示登入頁面
    return render_template('login.html')

# 登出功能
@auth_bp.route('/logout')
def logout():
    # 清除 session 中的使用者資料
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('username', None)

    # 重定向到登入頁面
    return redirect(url_for('auth.login'))  
