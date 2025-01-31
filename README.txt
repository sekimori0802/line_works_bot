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
      - コールバックURL: http://localhost:4000/webhook
        (注: 本番環境では、インターネットからアクセス可能なURLに変更する必要があります)
      - メッセージタイプ: テキストを有効化

5. アプリケーションの起動
   ```
   python app.py
   ```
   - サーバーがポート4000で起動します
   - ヘルスチェック: http://localhost:4000/health にアクセスして動作確認

6. 動作確認
   - LINE Worksでボットにメッセージを送信
   - ボットがChatGPTを使用して応答することを確認

注意事項:
- .envファイルは機密情報を含むため、Gitにコミットしないでください
- ポート4000が他のアプリケーションで使用されている場合は、.envファイルでPORTを変更してください
- ローカルでの開発・テスト用の手順です。本番環境へのデプロイは別途設定が必要です
