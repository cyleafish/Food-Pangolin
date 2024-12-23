import mysql.connector
from mysql.connector import Error

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

def fetch_merchant_earnings(order_by=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT r.rest_id, r.restname, 
            COALESCE(SUM(o.total_price), 0) AS earnings
        FROM restaurant r
        LEFT JOIN 
            `order` o ON r.rest_id = o.rest_id AND o.status = 'completed'
        GROUP BY  r.rest_id
    """
    # 根據排序條件修改查詢
    if order_by == "rest_id":
        query += " ORDER BY r.rest_id ASC"
    elif order_by == "total_price":
        query += " ORDER BY earnings DESC"
    else:
        query += " ORDER BY r.rest_id ASC"

    cursor.execute(query)
    results = cursor.fetchall()
    return results



def fetch_deliver_orders(order_by=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT 
            d.deliver_name, 
            d.deliver_id, 
            COALESCE(COUNT(o.order_id), 0) AS orders
        FROM deliver d
        LEFT JOIN `order` o ON d.deliver_id = o.deliver_id AND o.status = 'completed'
        GROUP BY d.deliver_id
    """ 
    # 因為後面 query 要加 order，所以不能有「；」
    if order_by == "deliver_id":
        query += " ORDER BY d.deliver_id ASC"
    elif order_by == "orders":
        query += " ORDER BY orders DESC"
    else:
        query += " ORDER BY d.deliver_id ASC"

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

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
