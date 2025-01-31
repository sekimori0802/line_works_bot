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
   - HTTPSに対応したWebサーバー(Nginx推奨)
   - インターネットからアクセス可能な固定IPアドレスまたはドメイン

2. デプロイ手順
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
      - .env.exampleを.envにコピーして必要な値を設定
      - コールバックURLを本番環境のURLに変更(例: https://your-domain.com/webhook)

   d. Webサーバーの設定
      - Nginxなどのリバースプロキシを設定
      - SSL証明書の設定(Let's Encryptなど)

   e. アプリケーションの起動
      - systemdなどのサービス管理ツールを使用して自動起動を設定

3. LINE Works設定の更新
   - LINE Works Developers ConsoleでコールバックURLを本番環境のURLに更新
   - Webhook URLの形式: https://your-domain.com/webhook

本番環境では、必ずHTTPSを使用し、適切なセキュリティ対策を実施してください。
