import mysql.connector
from datetime import datetime

def get_db_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='food_pangolin'
    )
    return connection

# JOSH: 不要開開關關->耗資源

def verify_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_account WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return user

def fetch_pending_orders(order_by=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            o.order_id, 
            o.total_price, 
            o.addr AS customer_addr,
            c.name, 
            r.restname,
            r.addr AS restaurant_addr,
            ROUND(IFNULL(AVG(cs.star), 0), 1) AS star
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        JOIN restaurant r ON o.rest_id = r.rest_id
        LEFT JOIN customer_star cs ON c.customer_id = cs.customer_id
        WHERE o.deliver_id IS NULL
        GROUP BY o.order_id, c.name, r.restname
    """
    if order_by == "price":
        query += " ORDER BY o.total_price DESC"
    elif order_by == "star":
        query += " ORDER BY star DESC"
    elif order_by == "time":
        query += " ORDER BY date DESC"  # 按時間升序排列
    cursor.execute(query)
    orders = cursor.fetchall()
    cursor.close()
    connection.close()
    return orders


def fetch_deliver_info(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            ua.user_id,
            ua.username,
            ua.role,
            d.deliver_id,
            d.deliver_name,
            d.phone,
            d.car_num,
            ROUND(IFNULL(AVG(ds.star), 0), 1) AS star
        FROM user_account ua
        LEFT JOIN deliver d ON ua.username = d.deliver_name
        LEFT JOIN deliver_star ds ON d.deliver_id = ds.deliver_id
        WHERE ua.role = 'deliver' AND ua.user_id = %s
        GROUP BY d.deliver_id;
    """
    cursor.execute(query, (user_id,))  # 傳遞 user_id 作為參數
    info = cursor.fetchone()
    cursor.close()
    connection.close()
    return info


def get_order_info(order_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # 查詢訂單基本資訊
    query = """
        SELECT 
            o.order_id, 
            o.total_price, 
            o.status,
            r.restname,
            c.name AS customer_name,
            ROUND(IFNULL(AVG(cs.star), 0), 1) AS star
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        JOIN restaurant r ON o.rest_id = r.rest_id
        LEFT JOIN customer_star cs ON c.customer_id = cs.customer_id
        WHERE o.order_id = %s
        GROUP BY o.order_id
    """
    cursor.execute(query, (order_id,))
    order_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return order_info

def get_order_details(order_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # 查詢訂單詳細項目
    query = """
        SELECT 
            oi.item_id, 
            oi.menu_id, 
            m.name, 
            oi.quantity, 
            oi.price, 
            oi.note,
            (oi.quantity * oi.price) AS total_price  -- 計算單項目總價
        FROM order_item oi
        JOIN menu m ON oi.menu_id = m.menu_id  -- 假設有menu資料表
        WHERE oi.order_id = %s
    """
    cursor.execute(query, (order_id,))
    order_details = cursor.fetchall()

    cursor.close()
    connection.close()

    return order_details

def get_delivery_address(order_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # 查詢訂單送貨地址
    query = """
        SELECT addr FROM `order` WHERE order_id = %s
    """
    cursor.execute(query, (order_id,))
    delivery_address = cursor.fetchone()

    cursor.close()
    connection.close()

    return delivery_address

def accepted_order(order_id, deliver_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            UPDATE `order`
            SET status = 'accepted', deliver_id = %s
            WHERE order_id = %s ;
        """
        cursor.execute(query, (deliver_id, order_id))
        connection.commit()
        cursor.close()
        connection.close()
        return cursor.rowcount > 0  # True: 更新成功, False: 訂單已被接走或不存在
    except Exception as e:
        connection.rollback()
        raise e  # 將錯誤傳遞給上層處理
    finally:
        cursor.close()
        connection.close()

def fetch_deliver_id(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            ua.user_id,
            ua.username,
            ua.role,
            d.deliver_id,
            d.deliver_name
        FROM user_account ua
        LEFT JOIN deliver d ON ua.username = d.deliver_name
        WHERE ua.role = 'deliver' AND ua.user_id = %s
        GROUP BY d.deliver_id;
    """
    cursor.execute(query, (user_id,))  # 傳遞 user_id 作為參數
    info = cursor.fetchone()
    cursor.close()
    connection.close()
    return info["deliver_id"]

def get_current_orders(deliver_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT o.order_id, o.total_price, 
        r.restname, r.addr AS restaurant_addr,
        c.name AS customer_name, 
        o.addr AS customer_addr,o.status
        FROM `order` o
        JOIN restaurant r ON o.rest_id = r.rest_id
        JOIN customer c ON o.customer_id = c.customer_id
        WHERE o.deliver_id = %s  AND o.status != 'completed'
    """
    cursor.execute(query, (deliver_id,))
    orders = cursor.fetchall() or []
    cursor.close()
    connection.close()
    return orders

def get_deliver_history(deliver_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT o.order_id, o.total_price, o.status,o.completed_time,
        r.restname, c.name AS customer_name
        FROM `order` o
        JOIN restaurant r ON o.rest_id = r.rest_id
        JOIN customer c ON o.customer_id = c.customer_id
        WHERE o.deliver_id = %s AND o.status = 'completed'
    """
    cursor.execute(query, (deliver_id,))
    orders = cursor.fetchall() or []
    cursor.close()
    connection.close()
    return orders

def update_order_status(order_id, new_status):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
         # 如果新狀態是 `completed`，記錄完成時間
        if new_status == 'completed':
            query = """
                UPDATE `order`
                SET `status` = %s, `completed_time` = %s
                WHERE `order_id` = %s
            """
            completed_time = datetime.now()
            cursor.execute(query, (new_status, completed_time, order_id))

        else:
            # 更新其他狀態時不修改 `completed_time`
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
    except Exception as e:
        print(f"更新訂單狀態時發生錯誤: {e}")
        success = False
    return success

def add_customer_rating(order_id, deliver_id, rating):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # 根據 `order_id` 找到對應的 `customer_id`
        cursor.execute("SELECT customer_id FROM `order` WHERE order_id = %s", (order_id,))
        result = cursor.fetchone()
        if not result:
            print(f"[錯誤] 找不到對應的顧客ID，order_id: {order_id}")
            return False
        customer_id = result['customer_id']

        # 插入評分，確保每個訂單有唯一的評分
        query = """
            INSERT INTO customer_star (customer_id, deliver_id, order_id, star) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (customer_id, deliver_id, order_id, rating))

        connection.commit()
        print(f"[成功] 評分已新增 - order_id: {order_id}, customer_id: {customer_id}, deliver_id: {deliver_id}, star: {rating}")
        return True
    except Exception as e:
        print(f"[錯誤] 評分失敗，原因: {e}")
        return customer_id, deliver_id, order_id, rating,e
    finally:
        cursor.close()
        connection.close()



