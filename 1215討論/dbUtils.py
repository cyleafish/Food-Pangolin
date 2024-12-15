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
		database="se"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)


#登入
def getList(ac):
	sql="SELECT ac, pw FROM acinfo where ac=%s;"
	param=(ac,)
	cursor.execute(sql,param)
	return cursor.fetchone()

#註冊

#讀取菜單

#新增菜單

#刪除菜單

#修改菜單

#讀取訂單

#讀取訂單資訊

#修改訂單狀態











