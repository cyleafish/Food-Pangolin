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

def verify_restaurant(username):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """SELECT restaurant.rest_id AS rest_id FROM `restaurant` 
    INNER JOIN user_account ON restaurant.user_id = user_account.user_id 
    WHERE user_account.username = %s;"""
    cursor.execute(query, (username,))
    rest_id = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return rest_id

def check_existing_user(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_account WHERE username = %s', (username,))
    existing_user = cursor.fetchone()

    cursor.close()
    connection.close()
    return existing_user

def register_deliver_account(username, password, phone, car_num,role):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # 新增到 deliver 資料表
        cursor.execute(
            "INSERT INTO deliver (deliver_name, phone, car_num) VALUES (%s, %s, %s)",
            (username, phone, car_num)
        )
        deliver_id = cursor.lastrowid  # 取得剛插入的 deliver_id

        # 新增到 user_account 資料表
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(
            "INSERT INTO user_account (username, password, role, created_at) VALUES (%s, %s, %s, %s)",
            (username, password, role, created_at)
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

def register_customer_account(username, password, role, phone, addr, email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # 新增到 customer 資料表
        cursor.execute(
            "INSERT INTO customer (name, phone, addr, email) VALUES (%s, %s, %s, %s)",
            (username, phone, addr, email)
        )
        
        # 新增到 user_account 資料表
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(
            "INSERT INTO user_account (username, password, role, created_at) VALUES (%s, %s, %s, %s)",
            (username, password, role, created_at)
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

def register_merchant_account(username, password, addr, phone,role):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:

        # 新增到 user_account 資料表
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO user_account (username, password, role, created_at) VALUES (%s, %s, %s, %s)",
            (username, password, role, created_at)
        )
        user_id = cursor.lastrowid  # 取得剛插入的 deliver_id

        # 新增到 restaurant 資料表
        time = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            """
            INSERT INTO restaurant (restname,user_id, addr, phone, time)
            VALUES (%s,%s, %s, %s, %s)
            """,
            (username,user_id, addr, phone,time)
        )

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()