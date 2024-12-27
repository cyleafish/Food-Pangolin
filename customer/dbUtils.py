
import mysql.connector

# 連線資料庫
try:
    # 連線到 MariaDB/MySQL
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="food_pangolin"
    )
    # 建立 cursor，設定傳回 dictionary 型態的查詢結果
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)

# 新增資料
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

def compare(data):
    # 檢查帳號和用戶名是否已存在
    sql = "SELECT * FROM user_account WHERE username = %s"  # 確保使用正確的欄位名
    cursor.execute(sql, (data['username'],))
    return cursor.fetchone()  # 檢查是否有結果返回
def getUser(username):
    cursor.execute("SELECT user_id, username, password, role FROM user_account WHERE username = %s", (username,))
    user = cursor.fetchone()  
    return user
def getCustomer(username):
    cursor.execute("SELECT customer_id, name, addr, email, phone FROM customer WHERE name = %s", (username,))
    user = cursor.fetchone()  
    return user
def get_restaurants(rest_id=None):
    if rest_id:
        sql = "SELECT * FROM restaurant WHERE rest_id=%s"
        cursor.execute(sql, (rest_id,))
    else:
        sql = "SELECT * FROM restaurant"
        cursor.execute(sql)
    return cursor.fetchall()
def register_user(data):
    sql = "INSERT INTO customer (name, phone, addr, email) VALUES (%s, %s, %s ,%s)"  # 確保欄位名正確
    cursor.execute(sql, (data['username'], data['phone'], data['address'], data['email']))
    conn.commit()  # 提交更改
    return 
def register_account(data):
    sql = "INSERT INTO user_account (username, password) VALUES (%s, %s)"  # 確保欄位名正確
    cursor.execute(sql, (data['username'], data['password']))
    conn.commit()  # 提交更改
    return 
def get_menu_items(rest_id):
     sql = "SELECT * FROM menu WHERE rest_id = %s"
     cursor.execute(sql, (rest_id,))
     return cursor.fetchall()
def get_order_details(cart):
    order_details = []
    for item_id, item_data in cart.items():  # 正確迭代字典的鍵值對
        quantity = item_data.get('quantity', 0)
        note = item_data.get('note', '')

        # 從數據庫查詢菜品名稱和價格
        sql = "SELECT menu_id, name, price FROM menu WHERE menu_id = %s"
        cursor.execute(sql, (item_id,))
        item = cursor.fetchone()  # 假設這是返回字典 {'name': ..., 'price': ...}

        if item:
            id=item['menu_id']
            name = item['name']
            price = float(item['price'])
            item_total = price * quantity  # 計算小計

            order_details.append({
                'menu_id':id,
                'name': name,
                'price': price,
                'quantity': quantity,
                'note': note,
                'item_total': item_total
            })

    return order_details

def add_order(customer_id, cart, order_details, data):
    # 插入到訂單表
    sql = "INSERT INTO `order` (customer_id, status, rest_id, total_price, addr) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (customer_id, 'pending', data['rest_id'], data['total_price'], data['address']))
    conn.commit()
    order_id = cursor.lastrowid

    # 新增訂單詳細表
    for item_id, item_details in cart.items():
        # 從 order_details 找到對應的 price 和 note
        detail = next((item for item in order_details if str(item['menu_id']) == str(item_id)), None)
        if detail:
            price = detail['price']
            note = detail['note']
        else:
            price = 0.0
            note = ''

        quantity = item_details['quantity'] if isinstance(item_details, dict) else item_details

        sql = """
            INSERT INTO order_item (order_id, menu_id, quantity, price, note)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (order_id, item_id, quantity, price, note))

    conn.commit()
    return order_id

def get_order_history(customer_id):
    sql = """
    SELECT o.order_id, o.total_price, o.status, o.date, r.restname AS rest_name
    FROM `order` o
    JOIN restaurant r ON o.rest_id = r.rest_id
    WHERE o.customer_id = %s
    ORDER BY o.date 
    """
    cursor.execute(sql, (customer_id,))
    return cursor.fetchall()
def get_details(order_id):
    sql = """
    SELECT oi.item_id, m.name AS item_name, oi.quantity, oi.price, 
           (oi.quantity * oi.price) AS total_price, oi.note
    FROM order_item oi
    JOIN menu m ON oi.menu_id = m.menu_id
    WHERE oi.order_id = %s
    """
    cursor.execute(sql, (order_id,))
    return cursor.fetchall()

     