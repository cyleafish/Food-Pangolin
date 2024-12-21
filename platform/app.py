from flask import Flask, render_template
from dbUtils import fetch_merchant_earnings, fetch_deliver_orders, fetch_customer_payments

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merchant_earnings')
def merchant_earnings():
    results = fetch_merchant_earnings()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('merchant_earnings.html', merchants=results)

@app.route('/deliver_orders')
def deliver_orders():
    results = fetch_deliver_orders()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('deliver_orders.html', delivers=results)

@app.route('/customer_payments')
def customer_payments():
    results = fetch_customer_payments()
    if results is None:
        return "無法連接到資料庫，請稍後再試。"
    return render_template('customer_payments.html', customers=results)

if __name__ == '__main__':
    app.run(debug=True)
