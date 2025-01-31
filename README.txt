LINE Works ChatGPTボット ローカル起動手順

1. 環境構築
   - Pythonがインストールされていることを確認
   - コマンドプロンプトで以下を実行:
     ```
     python --version
     ```

2. プロジェクトのセットアップ
   a. 仮想環境の作成と有効化
      ```
      cd line_works_bot
      python -m venv venv
      .\venv\Scripts\activate
      ```
   
   b. 必要なパッケージのインストール
      ```
      pip install -r requirements.txt
      ```

3. 環境変数の設定
   a. .env.exampleを.envにコピー
   b. .envファイルを編集し、以下の値を設定:
      - ADMIN_ID=10004480
      - BOT_ID=9022288
      - CLIENT_ID=3vkZGLfATh1Y2t35TrrF
      - CLIENT_SECRET=bnUgQ7ewO1
      - DOMAIN_ID=10004480
      - SCOPE=bot,bot.read,bot.message
      - SERVICE_ACCOUNT=yhdll.serviceaccount@wmj.sas-cloud.jp
      - PRIVATE_KEY=(プライベートキーを設定)
      - OPENAI_API_KEY=(OpenAI APIキーを設定)
      - PORT=4000

4. LINE Worksの設定
   a. LINE Works Developers Consoleで以下を設定:
      - コールバックURL: https://localhost:4000/webhook
        (注: 本番環境では、インターネットからアクセス可能なURLに変更する必要があります)
      - メッセージタイプ: テキストを有効化

   b. HTTPSの設定:
      - アプリケーションはHTTPSで動作します(自己署名証明書を使用)
      - 初回アクセス時にブラウザで警告が表示されますが、開発環境では「詳細設定」から進むことができます

5. ローカル環境でのテスト実行
   a. ngrokのセットアップ
      - ngrokのアカウントを作成: https://ngrok.com/
      - アカウント作成後、認証トークンを取得
      - 以下のコマンドで認証を設定:
        ```
        ngrok config add-authtoken your_auth_token
        ```

   b. アプリケーションの起動
      ```
      python app.py
      ```
      - サーバーがポート4000で起動します
      - ngrokが自動的に起動し、公開用URLが表示されます
      - 表示されたWebhook URLをコピーします(例: https://xxxx-xxx-xxx-xxx-xxx.ngrok.io/webhook)

   c. LINE Works Developers Consoleの設定更新
      - コールバックURLに、表示されたWebhook URLを設定
      - [更新]ボタンをクリック

   d. 動作確認
      - ヘルスチェック: 表示されたngrok URLの/healthにアクセス
      - LINE Worksアプリでボットにメッセージを送信してテスト

6. 動作確認
   - LINE Worksでボットにメッセージを送信
   - ボットがChatGPTを使用して応答することを確認

注意事項:
- .envファイルは機密情報を含むため、Gitにコミットしないでください
- ポート4000が他のアプリケーションで使用されている場合は、.envファイルでPORTを変更してください
- ローカルでの開発・テスト用の手順です。本番環境へのデプロイは別途設定が必要です

デプロイ手順:
1. サーバー要件
   - Python 3.11以上がインストールされているサーバー
   - インターネットからアクセス可能な固定IPアドレスまたはドメイン
   - SSL証明書(Let's Encryptなど)

2. SSL証明書の準備
   a. Let's Encryptを使用する場合:
      ```
      # certbotのインストール
      sudo apt-get update
      sudo apt-get install certbot

      # 証明書の取得
      sudo certbot certonly --standalone -d your-domain.com
      ```
      証明書は以下の場所に保存されます:
      - 証明書: /etc/letsencrypt/live/your-domain.com/fullchain.pem
      - 秘密鍵: /etc/letsencrypt/live/your-domain.com/privkey.pem

3. デプロイ手順
   a. サーバーにコードをクローン
      ```
      git clone https://github.com/sekimori0802/line_works_bot.git
      cd line_works_bot
      ```

   b. 環境構築
      ```
      python -m venv venv
      source venv/bin/activate  # Linuxの場合
      pip install -r requirements.txt
      ```

   c. 環境変数の設定
      ```
      cp .env.example .env
      vim .env
      ```
      以下の項目を設定:
      - LINE Works API関連の設定
      - OpenAI APIキー
      - SSL証明書のパス
        ```
        SSL_CERT_PATH=/etc/letsencrypt/live/your-domain.com/fullchain.pem
        SSL_KEY_PATH=/etc/letsencrypt/live/your-domain.com/privkey.pem
        ```

   d. systemdサービスの設定
      ```
      sudo vim /etc/systemd/system/lineworks-bot.service
      ```
      以下の内容を追加:
      ```
      [Unit]
      Description=LINE Works ChatGPT Bot
      After=network.target

      [Service]
      User=your-username
      WorkingDirectory=/path/to/line_works_bot
      Environment="PATH=/path/to/line_works_bot/venv/bin"
      ExecStart=/path/to/line_works_bot/venv/bin/python app.py
      Restart=always

      [Install]
      WantedBy=multi-user.target
      ```

   e. サービスの起動
      ```
      sudo systemctl daemon-reload
      sudo systemctl enable lineworks-bot
      sudo systemctl start lineworks-bot
      ```

   f. ログの確認
      ```
      sudo journalctl -u lineworks-bot -f
      ```

4. LINE Works設定の更新
   a. LINE Works Developers Consoleにアクセス
   b. コールバックURLを更新: https://your-domain.com/webhook
   c. [更新]ボタンをクリック

5. 動作確認
   a. ヘルスチェック
      ```
      curl https://your-domain.com/health
      ```
   b. LINE Worksアプリでボットにメッセージを送信してテスト

トラブルシューティング:
1. サービスが起動しない場合
   - ログを確認: sudo journalctl -u lineworks-bot -f
   - 権限の確認: SSL証明書と秘密鍵の読み取り権限
   - パスの確認: .envファイルの設定が正しいか

2. Webhookが動作しない場合
   - ファイアウォールの確認: ポート443が開いているか
   - SSL証明書の確認: 有効期限と設定
   - URLの確認: LINE Works Developers Consoleの設定

セキュリティに関する注意:
- .envファイルのバックアップを安全な場所に保管
- SSL証明書の定期的な更新を確認
- システムの定期的なアップデートを実施
