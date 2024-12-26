#!/usr/local/bin/python
# Connect to MariaDB Platform
from datetime import datetime
import mysql.connector #mariadb

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="food_pangolin"
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

#取得user_id
def getuser_id(username):
	sql="SELECT user_id FROM user_account where username=%s;"
	param=(username,)
	cursor.execute(sql,param)
	return cursor.fetchone()


#創建restaurant
def create_rest(user_id):
    date=datetime.now()
    sql="insert into restaurant (user_id,time) VALUES (%s,%s);"
    param=(user_id,date,)
    cursor.execute(sql,param)
    conn.commit()
    return


#查看菜單
def get_all_menu(username):
	sql='SELECT menu_id,filename, name, price, description FROM menu INNER JOIN restaurant ON menu.rest_id = restaurant.rest_id INNER JOIN user_account ON restaurant.user_id = user_account.user_id  where user_account.username=%s;'
	param=(username,)
	cursor.execute(sql,param)
	return cursor.fetchall()

#取得目前餐廳id
def getrestid(username,password):
    sql = "SELECT restaurant.rest_id FROM `restaurant` INNER JOIN user_account ON restaurant.user_id = user_account.user_id WHERE user_account.username = %s && user_account.password = %s;"
    param = (username,password,)
    cursor.execute(sql, param)
    result = cursor.fetchone()  # 获取结果

    if result:
        return result  # 如果有结果则返回
    else:
        return None  # 否则返回 None


#取得目前餐廳id
def getrest_id(rest_id):
    sql = "SELECT restaurant.rest_id FROM `restaurant` INNER JOIN `menu` on restaurant.rest_id=menu.rest_id INNER JOIN user_account ON restaurant.user_id = user_account.user_id WHERE user_account.username = %s;"
    param = (rest_id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()  # 获取结果

    if result:
        return result  # 如果有结果则返回
    else:
        return None  # 否则返回 None
    
#新增菜單
def addmenu(rest_id, name, price, description, filename):
    
    restid = rest_id['rest_id']  # 使用鍵 'rest_id' 取出字典中的值
    sql = "INSERT INTO menu (rest_id, name, price, description, filename) VALUES (%s, %s, %s, %s, %s);"  # 新增 img 欄位
    param = (restid, name, price, description, filename)
    cursor.execute(sql, param)
    conn.commit()

    return

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


#餐廳資訊
def get_resturant_info(rest_id):
	sql='SELECT restaurant.rest_id, restaurant.restname, restaurant.phone, restaurant.addr FROM `restaurant` INNER JOIN user_account ON restaurant.user_id = user_account.user_id WHERE user_account.username =%s;'
	param=(rest_id,)
	cursor.execute(sql,param)
	return cursor.fetchall()


#更新餐廳資訊
def update_rest(rest_id, data):
    sql = "UPDATE restaurant SET restname=%s, phone=%s, addr=%s WHERE rest_id=%s"
    params = (data['restname'], data['phone'], data['addr'], rest_id)
    cursor.execute(sql, params)
    conn.commit()	
	
    return

#所有未處理訂單
def getorderlist(rest_id):
    restid = rest_id['rest_id']  # 使用鍵 'rest_id' 取出字典中的值
    
    sql='SELECT order.order_id, order.customer_id, restaurant.rest_id, order.date,order.total_price,  order.deliver_id ,order.status FROM `order` INNER JOIN restaurant ON restaurant.rest_id = order.rest_id WHERE restaurant.rest_id = %s && order.status = "order";'
    param=(restid,)
    print(param,488484)
    cursor.execute(sql,param)
    return cursor.fetchall()

#篩選出處理中的所有訂單
def getprocessing(rest_id):
    restid = rest_id['rest_id']  # 使用鍵 'rest_id' 取出字典中的值
    
    sql='SELECT order.order_id, order.customer_id, restaurant.rest_id, order.date,order.total_price,  order.deliver_id ,order.status FROM `order` INNER JOIN restaurant ON restaurant.rest_id = order.rest_id WHERE restaurant.rest_id = %s && order.status != "completed" && order.status != "cancelled" && order.status != "order";'
    param=(restid,)
    print(param,488484)
    cursor.execute(sql,param)
    return cursor.fetchall()


#篩選已完成所有訂單
def getcomplite(rest_id):
    restid = rest_id['rest_id']  # 使用鍵 'rest_id' 取出字典中的值
    sql='SELECT order.order_id, order.customer_id, restaurant.rest_id, order.date,order.total_price,  order.deliver_id ,order.status ,order.completed_time FROM `order` INNER JOIN restaurant ON restaurant.rest_id = order.rest_id WHERE restaurant.rest_id = %s && (order.status = "completed" or order.status = "cancelled");'
    param=(restid,)
    print(param,488484)
    cursor.execute(sql,param)
    return cursor.fetchall()


#篩選訂單細項
def getorderdetails(order_id):
    sql='SELECT order.order_id, menu.name, order_item.quantity, order_item.price,order_item.note, order.status FROM `order` INNER JOIN order_item ON order.order_id = order_item.order_id INNER JOIN menu ON menu.menu_id = order_item.menu_id WHERE order.order_id = %s;'
    param=(order_id,)
    print(param,488484)
    cursor.execute(sql,param)
    return cursor.fetchall()

#更新訂單狀態
def update_status(order_id, status):
    sql = "UPDATE `order` SET status=%s WHERE order_id=%s"
    params = (status, order_id)
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









