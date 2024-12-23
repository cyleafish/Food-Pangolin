import os
from flask import Flask, render_template, request, session, redirect
from functools import wraps
from dbUtils import getList
from dbUtils import addmenu
from dbUtils import register_user
from dbUtils import getmenuedit
from dbUtils import get_all_menu
from dbUtils import update_menu
from dbUtils import delete_menu
from dbUtils import get_resturant_info
from dbUtils import update_rest
from dbUtils import getrestid
from dbUtils import getorderlist
from dbUtils import getcomplite
from dbUtils import getprocessing


# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'
UPLOAD_FOLDER = 'static'  # 設定圖片上傳資料夾
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 設定允許的圖片格式

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID')
		if not loginID:
			return redirect('/login_res')
		return f(*args, **kwargs)
	return wrapper

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#根目錄
@app.route("/") 
def hello(): 
	return redirect('/host')

#選擇使用者
@app.route('/host')
def glsds():
	return render_template('host.html')

#登入
@app.route('/login_res', methods=['GET'])
def gl():
	return render_template('login_res.html')

@app.route('/user', methods=['GET','POST'])
def login():
    form=request.form
    id = form['username']
    password =form['password']
    data=getList(id)
    print(id, password)
    dataa=getrestid(id,password)
    if data and data['password']==str(password) and data['role'] == 'restaurant':
        session['loginID'] = id
        session['rest_id'] = dataa
        return redirect('/host_res')
    else:
        session['loginID'] = False
        return redirect('/log_res')
    
#登出
@app.route('/logout', methods=['GET','POST'])
def gggggh():
    session.clear()
    return redirect('/login_res')
    
#註冊
@app.route('/log_res', methods=['GET'])
def log():
    return render_template('log_res.html')
	
    
@app.route('/register', methods=['POST'])
def register():
    data = {
        'username': request.form['username'],
        'password': request.form['password'],
        'role': 'restaurant'
    }
    
    register_user(data)
    
    return redirect('/login_res')


#主頁
@app.route('/host_res', methods=['GET'])
@login_required
def ggggg():
    return render_template('host_res.html')


#自己商品
@app.route('/menu_res', methods=['GET'])
@login_required
def gghgi():
	username=session['loginID']
	abb=get_all_menu(username)
	return render_template('menu_res.html',data=abb)

# 新增菜單
@app.route('/add_menu')
@login_required
def ggggfsfsh():
    return render_template('add_menu.html')

@app.route('/ad_menu', methods=['POST'])
@login_required
def ggggidsw():
    name = str(request.form['name'])
    price = str(request.form['price'])
    description = str(request.form['description'])
    print(name, price, description)  # 檢查 name, price, description 是否正確e
    rest_id = session['rest_id']
    print(rest_id)
    file = request.files['itemImage']
    
    print(rest_id)

    if file and allowed_file(file.filename):
        # ⚠️  移除 secure_filename() 和 uuid.uuid4()
        filename = file.filename  
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(rest_id)

        # data = (rest_id, name, price, description, filename)  # 儲存檔名
        addmenu(rest_id, name, price, description, filename)
        print(rest_id)
        
        return redirect('/menu_res')  
    else:
        return '不允許的檔案類型'



#編輯
@app.route("/edit_res/<int:menu_id>", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def edit_menu_item(menu_id):
    item = getmenuedit(menu_id)  # 獲取菜單項目的資料
    return render_template('edit_menu.html', item=item)

@app.route("/update_menu", methods=['POST','GET'])
@login_required
def h12():
    print()
    data = {
        'menu_id': request.form['menu_id'],
        'name': request.form['name'],		
        'price': request.form['price'],
        'description': request.form['description']
    }
    update_menu(data['menu_id'],data)
    return redirect('/menu_res')

#刪除
@app.route("/delete_menu", methods=['POST','GET'])
@login_required
def delete_item():
    menu_id = request.form['menu_id']
    if menu_id:
        delete_menu(menu_id)
    return redirect('/menu_res')

#看餐廳資訊
@app.route('/Restaurant', methods=['GET','POST'])
@login_required
def restaurant_info():
    username = session['loginID']
    data = get_resturant_info(username)
    return render_template("/Restaurant_information.html", data=data)

#更新資料
@app.route("/edit_restaurant", methods=['POST','GET'])
@login_required
def fscafea():
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


@app.route("/order_res_host")  # 只允許 POST 方法
@login_required
def order_function():
    return render_template('order_res_host.html')


#看所有訂單
@app.route("/order_res_list", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def printorder():
    rest_id = session['rest_id']
    items = getorderlist(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_list.html', data=items)



#看所有完成訂單
@app.route("/order_res_complete", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def printordercompleteqq():
    rest_id = session['rest_id']
    items = getcomplite(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_complite.html', data=items)

#看所有處理中訂單
@app.route("/order_res_processing", methods=['POST', 'GET'])  # 只允許 POST 方法
@login_required
def printordercomplete():
    rest_id = session['rest_id']
    items = getprocessing(rest_id)  # 獲取菜單項目的資料
    print(items)
    return render_template('order_res_processing.html', data=items)


# #競標、全部資料
# @app.route('/all', methods=['GET','POST'])
# @login_required
# def gghji():
# 	abb=getall()
# 	return render_template('all.html',data=abb)

# @app.route('/bid', methods=['GET','POST'])
# @login_required
# def grhji():
#     gid = request.args.get("gid")  # 從 URL 參數獲取 gid
#     print(gid)
#     abb = gethis(gid)        # 使用 gid 查詢競標紀錄
#     return render_template('his.html', data=abb, gid = gid)

# @app.route('/addhis', methods=['GET', 'POST'])
# @login_required
# def pghji():
#     ac = session['loginID']
#     aaid = getaid(ac)
#     gid = request.form['gid']  # 從 URL 參數獲取 gid
#     did_dict = getdid(gid)
#     did = did_dict["did"]  # 提取 did 值

#     user_bid = int(request.form['hp'])  # 使用者的出價
#     hp_dict = getnowhp(gid)  # 獲取當前最高價
#     rp_dict = getnowrp(gid)  # 獲取底價

#     # 提取數值
#     current_hp = hp_dict["hp"]
#     rp = rp_dict["rp"]

#     # 判斷使用者出價是否高於當前最高價和底價
#     if user_bid > current_hp and user_bid > rp:
#         data = (did, gid, aaid, user_bid)
#         addhis(data)
#         updategifo(user_bid, gid)
#         return redirect('/all')
#     else:
#         return redirect('/all')

