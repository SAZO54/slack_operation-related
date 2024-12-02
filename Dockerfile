# Pythonベースイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Flaskアプリケーションをコピー
COPY . .

# Flask環境変数の設定
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Flaskアプリケーションを起動
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
