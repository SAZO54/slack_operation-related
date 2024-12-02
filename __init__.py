import os
from flask import Flask
from flask_socketio import SocketIO
from .scheduler import start_scheduler
from dotenv import load_dotenv # type: ignore

# .envファイルから環境変数を読み込む
load_dotenv()

socketio = SocketIO()

def create_app(config_class=None):
    if config_class is None:
        # 環境変数からFlaskの環境設定を取得（デフォルトはProductionConfig）
        config_class = os.getenv('FLASK_CONFIG', 'app.config.ProductionConfig')

    app = Flask(__name__)
    app.config.from_object(config_class)

    from .event import slack_event_bp
    app.register_blueprint(slack_event_bp)

    # スケジューラの開始
    start_scheduler()

    return app
