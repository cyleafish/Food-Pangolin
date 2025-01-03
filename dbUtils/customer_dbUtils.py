
import mysql.connector



def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='food_pangolin'
    )
    return conn



def compare(data):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    # 檢查帳號和用戶名是否已存在
    sql = "SELECT * FROM user_account WHERE username = %s"  # 確保使用正確的欄位名
    cursor.execute(sql, (data['username'],))
    compare=cursor.fetchone()
    cursor.close()
    conn.close()
    return compare  # 檢查是否有結果返回

def getUser(username):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, password, role FROM user_account WHERE username = %s", (username,))
    user = cursor.fetchone()  
    cursor.close()
    conn.close()
    return user

def getCustomer(username):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_id, name, addr, email, phone FROM customer WHERE name = %s", (username,))
    user = cursor.fetchone()  
    cursor.close()
    conn.close()
    return user

def get_ordering(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT o.order_id, o.total_price, o.status, o.deliver_id 
             FROM `order` o 
             WHERE customer_id = %s AND o.status != 'completed'"""
    cursor.execute(sql, (customer_id,))
    ordering = cursor.fetchall()  # 正確獲取查詢結果
    cursor.close()
    conn.close()
    return ordering


def get_restaurants(rest_id=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if rest_id:
        sql = "SELECT * FROM restaurant WHERE rest_id=%s"
        cursor.execute(sql, (rest_id,))
        restaurants = cursor.fetchall()  # 獲取查詢結果
    else:
        sql = "SELECT * FROM restaurant"
        cursor.execute(sql)
        restaurants = cursor.fetchall()  # 獲取查詢結果
    cursor.close()
    conn.close()
    return restaurants


def register_user(data):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    sql = "INSERT INTO customer (name, phone, addr, email) VALUES (%s, %s, %s ,%s)"  # 確保欄位名正確
    cursor.execute(sql, (data['username'], data['phone'], data['address'], data['email']))
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return 

def register_account(data):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    sql = "INSERT INTO user_account (username, password) VALUES (%s, %s)"  # 確保欄位名正確
    cursor.execute(sql, (data['username'], data['password']))
    conn.commit()  # 提交更改
    cursor.close()
    conn.close()
    return 

def get_menu_items(rest_id):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    sql = "SELECT * FROM menu WHERE rest_id = %s"
    cursor.execute(sql, (rest_id,))
    items=cursor.fetchall()
    cursor.close()
    conn.close()
    return items

def get_order_details(cart):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
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
    cursor.close()
    conn.close()
    return order_details

def add_order(customer_id, cart, order_details, data):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    # 插入到訂單表
    sql = "INSERT INTO `order` (customer_id, status, rest_id, total_price, addr) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (customer_id, 'order', data['rest_id'], data['total_price'], data['address']))
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
    cursor.close()
    conn.close()
    return order_id

def get_order_history(customer_id):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    sql = """
    SELECT o.order_id, o.total_price, o.status, o.date, r.restname AS rest_name
    FROM `order` o
    JOIN restaurant r ON o.rest_id = r.rest_id
    WHERE o.customer_id = %s
    ORDER BY o.date 
    """
    cursor.execute(sql, (customer_id,))
    history=cursor.fetchall()
    cursor.close()
    conn.close()
    return history

def get_details(order_id):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)
    sql = """
    SELECT oi.order_id, oi.item_id, m.name AS item_name, oi.quantity, oi.price, 
           (oi.quantity * oi.price) AS total_price, oi.note
    FROM order_item oi
    JOIN menu m ON oi.menu_id = m.menu_id
    WHERE oi.order_id = %s
    """
    cursor.execute(sql, (order_id,))
    details=cursor.fetchall()
    cursor.close()
    conn.close()
    return details

def insert_comment(rest_id, customer_id, order_id,star, comment):
    conn = get_db_connection()
    cursor=conn.cursor(dictionary=True)

    sql = """
        INSERT INTO comment (rest_id, customer_id, order_id,star, comment)
        VALUES (%s, %s, %s,%s, %s)
    """
    cursor.execute(sql,(rest_id, customer_id, order_id,star, comment))
    conn.commit()  
    cursor.close()
    conn.close()
    return 
def if_comment(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """ SELECT c.order_id, o.status FROM `order` o
    LEFT JOIN `comment` c ON o.order_id = c.order_id
    where o.order_id=%s   """
    cursor.execute(sql, (order_id,))
    order_id = cursor.fetchone()  # 修改為 fetchone()
    print(order_id)
    cursor.close()
    conn.close()
    return order_id
"""
    if not order_id:
        return True  # 表示沒有評價
    return False  # 表示有評價了
"""


def get_restname(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT o.rest_id ,r.restname FROM `order` o
    JOIN `restaurant` r ON o.rest_id = r.rest_id
    WHERE o.order_id=%s"""
    cursor.execute(sql, (order_id,))
    restname = cursor.fetchone()  # 修改為 fetchone()
    cursor.close()
    conn.close()
    return restname

def get_restid(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """SELECT o.rest_id FROM `order` o
    WHERE o.order_id=%s"""
    cursor.execute(sql, (order_id,))
    restid = cursor.fetchone()  # 修改為 fetchone()
    cursor.close()
    conn.close()
    if restid:
        return restid['rest_id']  # 提取 'rest_id' 欄位的值
    return None  # 若沒有找到結果，則返回 None

def update_order_status(order_id, new_status):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
            UPDATE `order`
            SET `status` = %s
            WHERE `order_id` = %s
        """
    cursor.execute(query, (new_status, order_id))

    connection.commit()
    success = True

    cursor.close()
    connection.close()
    
    return success

def rest_reviews(rest_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT c.name, com.star, com.comment, com.data 
    FROM comment com 
    LEFT JOIN `customer` c ON c.customer_id = com.customer_id
    WHERE rest_id = %s 
    ORDER BY com.data  DESC;"""

    cursor.execute(query, (rest_id,))
    reviews = cursor.fetchall()
    return reviews

def rest_id_to_name(rest_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT restname FROM `restaurant` where rest_id=%s;"""

    cursor.execute(query, (rest_id,))
    reviews = cursor.fetchall()
    return reviews[0]['restname']