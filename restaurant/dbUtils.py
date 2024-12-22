#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="se-1220"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)


#登入
def getList(username):
	sql="SELECT username, password, role FROM user_account where username=%s;"
	param=(username,)
	cursor.execute(sql,param)
	return cursor.fetchone()

#註冊
def register_user(data):
	sql="insert into user_account (username,password,role) VALUES (%s,%s,%s);"
	param=(data['username'], data['password'], data['role'],)
	cursor.execute(sql,param)
	conn.commit()
	return

#查看菜單
def get_all_menu(username):
	sql='SELECT menu_id,img, name, price, description FROM menu INNER JOIN restaurant ON menu.rest_id = restaurant.rest_id INNER JOIN user_account ON restaurant.user_id = user_account.user_id  where user_account.username=%s;'
	param=(username,)
	cursor.execute(sql,param)
	return cursor.fetchall()


#查看自己的
def get_all_good(ac):
	sql='SELECT ac, ginfo.gid, ginfo.gname, ginfo.rp, ginfo.hp, ginfo.gc FROM db INNER JOIN acinfo ON db.aid = acinfo.aid INNER JOIN ginfo ON db.gid = ginfo.gid where ac=%s;'
	param=(ac,)
	cursor.execute(sql,param)
	return cursor.fetchall()

#取得目前餐廳id
def getrest_id(rest_id):
    sql = "SELECT r.rest_id FROM menu m INNER JOIN restaurant r ON m.rest_id = r.rest_id INNER JOIN user_account ua ON r.user_id = ua.user_id WHERE ua.username = %s"
    param = (rest_id,)
    cursor.execute(sql, param)
    return cursor.fetchone()
# def getrest_id(rest_id):
#     sql = "SELECT rest_id FROM menu inner join restaurant on menu.rest_id = restaurant.rest_id inner join user_account on restaurant.user_id = user_account.user_id WHERE user_account.username = %s"
#     param = (rest_id,)
#     cursor.execute(sql, param)
#     return cursor.fetchone()

#新增菜單
def addmenu(data):
    sql = "INSERT INTO menu (rest_id, name, price, description, img) VALUES (%s, %s, %s, %s, %s);"  # 新增 img 欄位
    param = tuple(data)
    cursor.execute(sql, param)
    conn.commit()
    return 

# #新增的
# def add(data):
#     sql = "INSERT INTO ginfo (gname, gc, rp) VALUES (%s, %s, %s);"
#     param = tuple(data)
#     cursor.execute(sql, param)
#     conn.commit()
#     return cursor.lastrowid  # 返回新插入資料的 gid

# def getaid(ac,):
# 	sql="SELECT aid FROM acinfo where ac=%s ;"
# 	param=(ac,)
# 	cursor.execute(sql,param)
# 	result = cursor.fetchone()
# 	return result['aid']#確定指傳回一個值

# def adddb(data):
# 	sql="insert into db (aid,gid) VALUES (%s, %s);"
# 	param=tuple(data)
# 	cursor.execute(sql,param)
# 	conn.commit()
# 	return

#修改的
def getmenuedit(menu_id):
	sql="SELECT menu_id, name, price, description FROM menu where menu_id=%s;"
	param=(menu_id,)
	cursor.execute(sql,param)
	return cursor.fetchone()


def update_menu(menu_id, data):
    sql = "UPDATE menu SET name=%s, price=%s, description=%s WHERE menu_id=%s"
    params = (data['name'], data['price'], data['description'], menu_id)
    cursor.execute(sql, params)
    conn.commit()	
	
    return

#刪除
def delete_menu(menu_id):
    sql = "DELETE FROM menu WHERE menu_id = %s"
    param = (menu_id,)
    cursor.execute(sql, param)
    conn.commit()
    return

#刪除
def delete(gid):
    sql = "DELETE FROM ginfo WHERE gid = %s"
    param = (gid,)
    cursor.execute(sql, param)
    conn.commit()
    return
	
#競標
def getall():
	sql="SELECT ginfo.gid, ginfo.gname, ginfo.rp, ginfo.hp, ginfo.gc FROM db INNER JOIN acinfo ON db.aid = acinfo.aid INNER JOIN ginfo ON db.gid = ginfo.gid;"
	cursor.execute(sql,)
	return cursor.fetchall()

def gethis(gid):
	sql="SELECT ginfo.gname, ginfo.rp, bh.hp, ginfo.gc, bh.time, bh.aaid FROM bh INNER JOIN db ON db.did = bh.did INNER JOIN ginfo ON db.gid = ginfo.gid where ginfo.gid=%s;"
	parom=(gid,)
	cursor.execute(sql,parom)
	return cursor.fetchall()

def getdid(gid):
    sql = "SELECT did FROM db WHERE gid = %s;"
    parom=(gid,)
    cursor.execute(sql,parom)
    return cursor.fetchone()

#取得目前最高價
def getnowhp(gid):
    sql = "SELECT hp FROM ginfo WHERE gid = %s"
    param = (gid,)
    cursor.execute(sql, param)
    return cursor.fetchone()

#取得底價
def getnowrp(gid):
    sql = "SELECT rp FROM ginfo WHERE gid = %s"
    param = (gid,)
    cursor.execute(sql, param)
    return cursor.fetchone()

def addhis(data):
	sql="insert into bh (did,gid,aaid,hp) VALUES (%s, %s, %s, %s);"
	param=tuple(data)
	cursor.execute(sql,param)
	conn.commit()
	return

def updategifo(hp, gid):
    sql = "UPDATE ginfo SET hp=%s WHERE gid=%s"
    params = (hp, gid)
    cursor.execute(sql, params)
    conn.commit()		
    return










