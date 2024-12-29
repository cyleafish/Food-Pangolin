import os
from flask import Flask,Blueprint, render_template, url_for,request, session, redirect
from functools import wraps
from app.dbUtils.restaurant_dbUtils import (getList,addmenu
,getuser_id,create_rest,register_user,getmenuedit,get_all_menu
,update_menu,delete_menu,get_resturant_info,update_rest,getrestid
,getorderlist,getcomplite,getprocessing,getorderdetails
,update_status)

# 創建 Blueprint
restaurant_bp = Blueprint('restaurant', __name__, template_folder='../templates/restaurant')

# creates a Flask application, specify a static folder on /
restaurant_app = Flask(__name__, static_folder='static', static_url_path='/static')
#set a secret key to hash cookies
restaurant_app.config['SECRET_KEY'] = '123TyU%^&'
UPLOAD_FOLDER = 'app/static'  # 設定圖片上傳資料夾
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 設定允許的圖片格式

restaurant_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		username = session.get('username') #username
		if not username:
			return redirect(url_for('auth.login'))
		return f(*args, **kwargs)
	return wrapper

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
'''
#根目錄#no
@restaurant_bp.route("/") 
def hello(): 
	return redirect('/host')
#選擇使用者#no
@restaurant_bp.route('/host')
def glsds():
	return render_template('host.html')
     
#登入#no
@restaurant_bp.route('/login_res', methods=['GET'])
def gl():
	return render_template('login_res.html')
#註冊#no
@restaurant_bp.route('/log_res', methods=['GET'])
def log():
    return render_template('log_res.html')
@restaurant_bp.route('/register', methods=['POST'])
def register():
    data = {
        'username': request.form['username'],
        'password': request.form['password'],
        'role': 'restaurant'
    }
    
    register_user(data)
    user_id = getuser_id(data['username'])
    create_rest(user_id['user_id'])
    return redirect('/login_res')
#登出
@restaurant_bp.route('/logout', methods=['GET','POST'])
def logout():
    session.clear()
    return redirect('/login_res')

@restaurant_bp.route('/user', methods=['GET','POST'])
def login():
        return redirect('/host_res')#餐廳主頁

'''



#主頁
@restaurant_bp.route('/host_res', methods=['GET'])
@login_required
def host_res():
    username=session['username']
    user_id=getuser_id(username)
    rest_id=getrestid(user_id['user_id'])
    session['rest_id'] = rest_id
    print(rest_id)
    return render_template('host_res.html')


#自己商品
@restaurant_bp.route('/menu_res', methods=['GET'])
@login_required
def menu_res():
    username=session['username']
    abb=get_all_menu(username)
    #print(render_template('menu_res.html',data=abb))
    return render_template('menu_res.html',data=abb)

# 新增菜單
@restaurant_bp.route('/add_menu')
@login_required
def add_menu():
    return render_template('add_menu.html')

@restaurant_bp.route('/ad_menu', methods=['POST'])
@login_required
def ad_menu():
    name = str(request.form['name'])
    price = str(request.form['price'])
    description = str(request.form['description'])
    print(name, price, description)  # 檢查 name, price, description 是否正確e
    rest_id = session['rest_id']
    print(rest_id)
    file = request.files.get('itemImage')
    
    print(rest_id)

    if file and allowed_file(file.filename):
        # ⚠️  移除 secure_filename() 和 uuid.uuid4()
        filename = file.filename  
        file_path = os.path.join(restaurant_app.config['UPLOAD_FOLDER'], filename)
        #file_path = os.path.normpath(os.path.join(restaurant_app.root_path, restaurant_app.config['UPLOAD_FOLDER'], filename))

        file.save(file_path)
        print(rest_id)

        # data = (rest_id, name, price, description, filename)  # 儲存檔名
        addmenu(rest_id, name, price, description, filename)
        print(rest_id)
        
        return redirect(url_for('restaurant.menu_res'))
  
    else:
        return '不允許的檔案類型'



#編輯
@restaurant_bp.route("/edit_res/<int:menu_id>", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def edit_res(menu_id):
    item = getmenuedit(menu_id)  # 獲取菜單項目的資料
    return render_template('edit_menu.html', item=item)

@restaurant_bp.route("/update_menu", methods=['POST','GET'])
@login_required
def menu_update():
    print()
    data = {
        'menu_id': request.form['menu_id'],
        'name': request.form['name'],		
        'price': request.form['price'],
        'description': request.form['description']
    }
    update_menu(data['menu_id'],data)
    return redirect(url_for('restaurant.menu_res'))

#刪除
@restaurant_bp.route("/delete_menu", methods=['POST','GET'])
@login_required
def delete_item():
    menu_id = request.form['menu_id']
    if menu_id:
        delete_menu(menu_id)
    return redirect('/menu_res')

#看餐廳資訊
@restaurant_bp.route('/Restaurant', methods=['GET','POST'])
@login_required
def restaurant_info():
    username = session['username']
    data = get_resturant_info(username)
    return render_template("/Restaurant_information.html", data=data)

#更新資料
@restaurant_bp.route("/edit_restaurant", methods=['POST','GET'])
@login_required
def edit_restaurant():
    print()
    data = {
        'rest_id': request.form['rest_id'],
        'restname': request.form['restname'],		
        'phone': request.form['phone'],
        'addr': request.form['addr']
    }
    print(data)
    update_rest(data['rest_id'],data)
    
    return redirect('/host_res')


@restaurant_bp.route("/order_res_host")  # 只允許 POST 方法
@login_required
def order_function():
    return render_template('order_res_host.html')


#看所有訂單
@restaurant_bp.route("/order_res_list", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def print_order():
    rest_id = session['rest_id']
    items = getorderlist(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_list.html', data=items)



#看所有完成訂單
@restaurant_bp.route("/order_res_complete", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def print_order_complete():
    rest_id = session['rest_id']
    items = getcomplite(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_complite.html', data=items)


#看所有處理中訂單
@restaurant_bp.route("/order_res_processing", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def print_order_processing():
    rest_id = session['rest_id']
    items = getprocessing(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_processing.html', data=items)


#取得訂單資料
@restaurant_bp.route("/order_res_details", methods=['GET', 'POST']) 
@login_required
def print_order_details():
    order_id =request.form.get('order_id')
    items = getorderdetails(order_id)  # 使用 db.py 中的 getorderdetails 函式
    return render_template('order_res_details.html', data=items)


@restaurant_bp.route("/order_res_update_details", methods=['POST']) 
@login_required
def update_order_details():
    status = request.form.get('status')
    order_id = request.form.get('order_id')  # 從查詢參數獲取 order_id
    print(order_id, status)
    update_status(order_id, status) 
    return redirect('/order_res_host')