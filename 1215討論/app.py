from flask import Flask, render_template, request, session, redirect
from functools import wraps
from dbUtils import getList
from dbUtils import add
from dbUtils import register_user
from dbUtils import getedit
from dbUtils import get_all_good
from dbUtils import update
from dbUtils import adddb
from dbUtils import getaid
from dbUtils import delete
from dbUtils import getall
from dbUtils import gethis
from dbUtils import addhis
from dbUtils import getdid
from dbUtils import updategifo
from dbUtils import getnowhp
from dbUtils import getnowrp


# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID')
		if not loginID:
			return redirect('/login')
		return f(*args, **kwargs)
	return wrapper


#根目錄
@app.route("/") 
@login_required
def hello(): 
	return redirect('/host1')


#登入
@app.route('/login', methods=['GET'])
def gl():
	return render_template('login_res.html')

@app.route('/user', methods=['GET','POST'])
def login():
	form=request.form
	id = form['id']
	pwd =form['pwd']
	data=getList(id)
	if data and data['pw']==int(pwd):
		session['loginID'] = id
		return redirect('/host1')
	else:
		session['loginID'] = False
		return redirect('/log')


#註冊
@app.route('/log', methods=['GET'])
def log():
    return render_template('log_res.html')
	
@app.route('/register', methods=['POST'])
def register():
    data = {
        'account': request.form['username'],
        'password': request.form['password'],
        'email': request.form['email']
    }
    
    register_user(data)
    
    return redirect('/login')

#顯示目前所有料理

#新增料理

#編輯料理

#刪除料理

#顯示所有訂單

#查看訂單內容

#更改訂單狀態

#傳送通知

