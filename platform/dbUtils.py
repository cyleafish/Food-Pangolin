import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # 如果有密碼請填入
            database="food_pangolin"
        )
        return connection
    except Error as err:
        print(f"資料庫連接錯誤: {err}")
        return None

def fetch_merchant_earnings():
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT r.restname, SUM(o.total_price) AS earnings
            FROM restaurant r
            JOIN `order` o ON r.rest_id = o.rest_id
            WHERE o.status = 'completed'
            GROUP BY r.rest_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        connection.close()

def fetch_deliver_orders():
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT d.deliver_name, COUNT(o.order_id) AS orders
            FROM deliver d
            JOIN `order` o ON d.deliver_id = o.deliver_id
            WHERE o.status = 'completed'
            GROUP BY d.deliver_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        connection.close()

def fetch_customer_payments():
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT c.name AS customer_name, SUM(o.total_price) AS payments
            FROM customer c
            JOIN `order` o ON c.customer_id = o.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.customer_id;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    finally:
        connection.close()
