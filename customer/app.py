from flask import Flask, render_template, request, session, redirect, flash
from functools import wraps
from dbUtils import compare, register_user, register_account, getUser, getCustomer, get_restaurants, get_menu_items, get_order_details, add_order, save_order_to_history

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = '123TyU%^&'

# 定義檢查登入狀態的裝飾器
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'loginID' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper

# 根路由，跳轉到登入頁面
@app.route('/')
def index():
    return redirect('/login')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/loginerror', methods=['GET'])
def login_error():
    return "Congrats!! Login failed!! Please try again."

@app.route('/addr', methods=['post'])
def gg():
    return render_template('register.html')

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/homepage', methods=["GET"])
@login_required
def homepage():
    username = session.get('username')
    users = getCustomer(username)
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
    return render_template('homepage.html', user=user)

# 點餐頁面
@app.route('/customer', methods=["GET","POST"])
@login_required
def customer():
    rest_id = request.form.get('rest_id') 
    restaurants = get_restaurants(rest_id)
    return render_template('customer.html', restaurants=restaurants)

@app.route('/menu', methods=['GET'])
def menu():
    rest_id = request.args.get('id')
    if not rest_id:
        flash('請選擇餐廳後再進入菜單頁面。')
        return redirect('/customer')
    session['restaurant_id'] = rest_id  # 存入 session
    menu_items = get_menu_items(rest_id)
    return render_template('menu_mcdonald.html', menu_items=menu_items, restaurant=rest_id)

@app.route('/confirm', methods=['GET', 'POST'])
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
        session['cart'] = cart  # 保存購物車到 session

    cart = session.get('cart', {})
    if not cart:
        flash('購物車為空，請重新選擇餐點。')
        return redirect(f'/menu?id={restaurant_id}')

    # 傳遞整個 cart 給 get_order_details
    order_details = get_order_details(cart)
    total_price = sum(item['item_total'] for item in order_details)

    return render_template('confirm.html', cart=order_details, total_price=total_price, restaurant=restaurant_id)

# 訂單完成頁面
@app.route('/order_finish', methods=['GET'])
def order_finish():
    cart = session.pop('cart', None)  # 清空購物車
    if not cart:
        flash('訂單無效或已完成。')
        return redirect('/menu')
    return render_template('orderfinish.html')


if __name__ == '__main__':
    app.run(debug=True)
