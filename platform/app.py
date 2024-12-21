from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 資料庫連接函數
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merchant_earnings')
def merchant_earnings():
    connection = get_db_connection()
    if not connection:
        return "無法連接到資料庫，請稍後再試。"

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
    connection.close()
    return render_template('merchant_earnings.html', merchants=results)

@app.route('/deliver_orders')
def deliver_orders():
    connection = get_db_connection()
    if not connection:
        return "無法連接到資料庫，請稍後再試。"

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
    connection.close()
    return render_template('deliver_orders.html', delivers=results)

@app.route('/customer_payments')
def customer_payments():
    connection = get_db_connection()
    if not connection:
        return "無法連接到資料庫，請稍後再試。"

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
    connection.close()
    return render_template('customer_payments.html', customers=results)

if __name__ == '__main__':
    app.run(debug=True)
