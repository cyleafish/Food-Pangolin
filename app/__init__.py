from flask import Flask, redirect, url_for
from app.controllers.auth_app import auth_bp
from app.controllers.deliver_app import deliver_bp
from app.controllers.platform_app import platform_bp
from app.controllers.restaurant_app import restaurant_bp
from app.controllers.customer_app import customer_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # 註冊 Blueprint
    app.register_blueprint(auth_bp ,url_prefix='/auth')
    app.register_blueprint(deliver_bp, url_prefix='/deliver')
    app.register_blueprint(platform_bp, url_prefix='/platform')
    app.register_blueprint(restaurant_bp, url_prefix='/restaurant')
    app.register_blueprint(customer_bp, url_prefix='/customer')

    # 根路徑重定向到 /auth/
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))  # 將根路徑導向到 auth.login 路由

    return app
