from flask import Flask,Blueprint,url_for,render_template, request, session, redirect, flash
from functools import wraps
from app.dbUtils.customer_dbUtils import (compare, register_user,
register_account, getUser, getCustomer, get_restaurants, get_menu_items, 
get_order_details, add_order, get_order_history, get_details, insert_comment,
get_restname,get_ordering,get_restid,if_comment,update_order_status)

# 創建 Blueprint
customer_bp = Blueprint('customer', __name__, template_folder='../templates/customer')

# 定義檢查登入狀態的裝飾器
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        username = session.get('username') #username
        if not username:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper
'''
# 根路由，跳轉到登入頁面
@customer_bp.route('/')
def index():
    return redirect('/login')

# 登入頁面
@customer_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form['username']
        pwd = form['password']

        # 從資料庫中取得使用者資料
        user = getUser(username)

        if user is not None and 'password' in user and user['password'] == pwd and user['role'] == 'customer':
            session['loginID'] = user['user_id']
            session['username'] = user['username']
            return redirect('/homepage')
        else:
            flash('登入失敗，請再次嘗試')
            return redirect('/login')

    return render_template('login_customer.html')

@customer_bp.route('/loginerror', methods=['GET'])
def login_error():
    return "Congrats!! Login failed!! Please try again."

# 註冊頁面
@customer_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        password = form['password']
        username = form['username']
        phone = form['phone']
        address = form['address']
        email = form['email']
        data = {
            'password': password,
            'username': username,
            'email': email,
            'phone': phone,
            'address': address
        }
        if compare(data):
            flash('帳號或用戶名已存在，請使用其他名稱。')
            return redirect('/register')
        else:
            register_user(data)
            register_account(data)
            flash('註冊成功！請登入。')
            return redirect('/login')
    return render_template('register.html')
'''


@customer_bp.route('/addr', methods=['post'])
def addr():
    return render_template('register.html')



@customer_bp.route('/homepage', methods=["GET"])
@login_required
def homepage():
    username = session.get('username')
    users = getCustomer(username)
    session['customer_id']=users['customer_id']
    session['name'] = users['name']
    session['email'] = users['email']
    session['phone'] = users['phone']
    session['address'] = users['addr']
    user = {
        'name': session['name'],
        'email': session['email'],
        'phone': session['phone'],
        'address': session['address']
    }
    print(session['customer_id'])
    order=get_ordering(session['customer_id'])
    return render_template('homepage.html', user=user,order=order)

# 點餐頁面
@customer_bp.route('/customer', methods=["GET","POST"])
@login_required
def customer():
    rest_id = request.form.get('rest_id') 
    restaurants = get_restaurants(rest_id)
    return render_template('customer.html', restaurants=restaurants)

@customer_bp.route('/menu', methods=['GET'])
def menu():
    rest_id = request.args.get('id')
    if not rest_id:
        flash('請選擇餐廳後再進入菜單頁面。')
        return redirect(url_for('customer'))
    session['restaurant_id'] = rest_id  # 存入 session
    menu_items = get_menu_items(rest_id)
    return render_template('menu_restaurant.html', menu_items=menu_items, restaurant=rest_id)

@customer_bp.route('/confirm', methods=['GET', 'POST'])
def confirm_order():
    cart = {}
    restaurant_id = session.get('restaurant_id')  # 優先從 session 獲取餐廳 ID

    if request.method == 'POST':
        for key, value in request.form.items():
            if key.startswith('quantity_'):
                menu_id = key.split('_')[1]
                quantity = int(value)
                note = request.form.get(f'note_{menu_id}', '')
                
                # 將數據存入購物車字典
                cart[menu_id] = {
                    'quantity': quantity,
                    'note': note,
                }
        cart = {key: val for key, val in cart.items() if val['quantity'] > 0}
        session['cart'] = cart  # 保存購物車到 session

    cart = session.get('cart', {})
    print(cart)
    if not cart:
        flash('購物車為空，請重新選擇餐點。')
        return redirect(url_for(f'menu?id={restaurant_id}'))

    # 傳遞整個 cart 給 get_order_details
    order_details = get_order_details(cart)
    total_price = sum(item['item_total'] for item in order_details)

    return render_template('confirm.html', cart=order_details, total_price=total_price, restaurant=restaurant_id)

# 訂單完成頁面
@customer_bp.route('/order_finish', methods=['GET','POST'])
def order_finish():
    cart=session.get('cart' ,{})
    customer_id=session.get('customer_id')
    order_details = get_order_details(cart)
    print(order_details)
    total_price = sum(item['item_total'] for item in order_details)
    user = {
        'rest_id': session['restaurant_id'],
        'total_price': total_price,
        'address': session['address']
    }
    order=add_order(customer_id,cart,order_details,user)
    return render_template('orderfinish.html',order=order,cart=order_details,total_price=total_price,user=user)

@customer_bp.route('/update_order_status/<int:order_id>/<new_status>', methods=['GET'])
def update_order_status_route(order_id, new_status):
    customer_id = session.get('customer_id')
    if not customer_id:
        flash('請先登入')
        return redirect(url_for('auth.login'))
    
    success = update_order_status(order_id, new_status)

    if success:
        return redirect(url_for('customer.homepage'))
    else:
        return "狀態更新失敗", 500
    
@customer_bp.route('/orderhistory', methods=['GET'])
def orderhistory():
    customer_id = session.get('customer_id')
    if not customer_id:
        flash('請先登入')
        return redirect(url_for('auth.login'))
    orders = get_order_history(customer_id)
    return render_template('history.html', orders=orders)

@customer_bp.route('/orderdetails/<int:order_id>', methods=['GET'])
@login_required
def order_details(order_id):
    # 查詢訂單商品明細
    items = get_details(order_id)
    comment = if_comment(order_id)
    return render_template('details.html', items=items, order_id=order_id,comment=comment)

@customer_bp.route('/evaluate/<int:order_id>', methods=['GET', 'POST'])
@login_required
def evaluate(order_id):
    
    rest_name=get_restname(order_id)
    
    customer_id=session.get('customer_id')

    if request.method == 'POST':
        rest_id=get_restid(order_id)
        customer_id = request.form['customer_id']
        star = request.form['star']
        comment = request.form['comment']
        insert_comment(rest_id, customer_id, order_id,star, comment)

        flash('評論提交成功！')
        return redirect(url_for('customer.order_details',order_id=order_id))
    return render_template('evaluate.html', order_id=order_id, rest_name=rest_name['restname'], customer_id=customer_id)
