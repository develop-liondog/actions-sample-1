# actions-sample-1

このリポジトリにはシンプルなノート CLI アプリケーション (`main.py`) と、OpenAI を利用してコードの差分を解析し、承認後にメールで送信する GitHub Actions ワークフローが含まれています。

## ノートアプリ

CLI では `notes.json` に保存されたノートの追加、一覧表示、削除、検索が行えます。

```bash
python main.py add "タイトル" "内容"
python main.py list
python main.py remove <id>
python main.py search "キーワード"
```

## GitHub Actions ワークフロー

`.github/workflows/analyze.yml` にあるワークフローは次の処理を行います。

1. `main` ブランチへの push をトリガーとして実行される。
2. git diff を取得し、OpenAI に送信して変更の影響を要約する。
3. 要約をアーティファクトとしてアップロードし、手動承認を待つ。
4. 承認されると、分析結果をメールで送信する。

### 必要なシークレット

- `OPENAI_API_KEY` – OpenAI の API キー。
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` – メール送信に使用する認証情報。
- `MAIL_TO` – 送信先メールアドレス。

手動承認ステップでは [trstringer/manual-approval](https://github.com/trstringer/manual-approval) アクションを使用しています。メール送信には [dawidd6/action-send-mail](https://github.com/dawidd6/action-send-mail) を利用しています。

### Personal Access Token

ワークフローは基本的に組み込みの `GITHUB_TOKEN` を利用しますが、フォーク環境などで権限が不足している場合は、以下のスコープを持つ PAT を作成してください。

- `repo` – リポジトリの読み取りと承認用ステータスの作成。
- `workflow` – ワークフローの実行・承認。

作成したトークンはシークレット（例: `GH_PAT`）として登録し、必要に応じてワークフローで参照してください。

### `GITHUB_OUTPUT` について

`Analyze diff with OpenAI` ステップでは、分析結果をマルチライン変数として出力します。`"Matching delimiter not found '__END_OF_ANALYSIS__'"` エラーを防ぐため、閉じ区切りは必ず単独行で記述する必要があります。このワークフローでは閉じ区切りの直前に空行を挿入しています。

```bash
echo "analysis<<__END_OF_ANALYSIS__" >> $GITHUB_OUTPUT
cat sanitized_analysis.txt >> $GITHUB_OUTPUT
echo "" >> $GITHUB_OUTPUT
echo "__END_OF_ANALYSIS__" >> $GITHUB_OUTPUT
```
