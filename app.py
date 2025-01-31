import os
import json
import requests
import jwt
import time
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

# 環境変数の読み込み
load_dotenv()

app = Flask(__name__)

# 環境変数から設定を読み込み
ADMIN_ID = os.getenv('ADMIN_ID')
BOT_ID = os.getenv('BOT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
DOMAIN_ID = os.getenv('DOMAIN_ID')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI APIの設定
openai.api_key = OPENAI_API_KEY

def generate_jwt():
    """JWT トークンの生成"""
    current_time = int(time.time())
    payload = {
        'iss': CLIENT_ID,
        'sub': SERVICE_ACCOUNT,
        'iat': current_time,
        'exp': current_time + (60 * 60)  # 1時間有効
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
    return token

def get_access_token():
    """アクセストークンの取得"""
    jwt_token = generate_jwt()
    url = 'https://auth.worksmobile.com/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': jwt_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'bot'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get('access_token')

def send_message(user_id, message):
    """メッセージの送信"""
    access_token = get_access_token()
    url = f'https://www.worksapis.com/v1.0/bots/{BOT_ID}/users/{user_id}/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'content': {
            'type': 'text',
            'text': message
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_chatgpt_response(message):
    """ChatGPTからの応答を取得"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"ChatGPT API Error: {e}")
        return "申し訳ありません。現在応答を生成できません。"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhookエンドポイント"""
    try:
        data = request.get_json()
        
        # メッセージイベントの処理
        if data.get('type') == 'message':
            user_id = data['source'].get('userId')
            received_message = data['content'].get('text', '')
            
            # ChatGPTから応答を取得
            response_message = get_chatgpt_response(received_message)
            
            # 応答を送信
            send_message(user_id, response_message)
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        print(f"Webhook Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """ヘルスチェックエンドポイント"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=True)
