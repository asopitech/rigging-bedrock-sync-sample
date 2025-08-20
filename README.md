# rigging-bedrock-sync-sample

Python で `rigging` を用いて AWS Bedrock 上の Claude を呼び出す最小実行サンプル。ローカル実行と AWS Lambda 実行の両方に対応し、**Pydantic モデル（`rg.Model`）による構造化出力**をサポート。

**主な特徴：**
- ✅ 同期エントリポイント（`asyncio.get_event_loop().run_until_complete`使用）
- ✅ **構造化出力**: `xml_example()` → `.until_parsed_as(Model)` → `.parse(Model)` で厳格な型抽出
- ✅ rigging と python-dotenv のみの最小依存
- ✅ ローカルとLambda両対応
- ✅ 適切なエラーハンドリングとトラブルシューティングガイド
- ✅ 200行以内のコード

**使用方法：**
1. `.env.example` → `.env` にコピーして設定
2. `python -m app.main` でローカル実行（構造化カタログが生成される）
3. Lambda では `app.handler.lambda_handler` を指定（JSON形式で構造化カタログを返す）

## 前提

- Python 3.11 以上
- AWS アカウントと適切な権限設定
- AWS CLI の設定または Lambda 実行ロール

## セットアップ

### uv を使用する場合

```bash
cd rigging-bedrock-sync-sample
uv venv
uv pip install -e .
```

### pip を使用する場合

```bash
cd rigging-bedrock-sync-sample
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## ローカル実行

1. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集して適切な値を設定：

```env
AWS_PROFILE=your-aws-profile
AWS_REGION_NAME=us-west-2
BEDROCK_MODEL_ID=bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0
```

2. 実行

```bash
python -m app.main
# または
python app/main.py
```

## Lambda デプロイ（概要）

### 設定

- **ハンドラー**: `app.handler.lambda_handler`
- **ランタイム**: Python 3.11
- **環境変数**:
  - `AWS_REGION_NAME`: `us-west-2` など
  - `BEDROCK_MODEL_ID`: `bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0` など
- **実行ロール**: Bedrock Invoke 権限が必要

### 必要な IAM 権限

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

### デプロイ方法

ZIP パッケージまたはコンテナイメージでデプロイ可能。最小構成では ZIP パッケージが推奨。

## トラブルシューティング

### アクセス拒否エラー

- Bedrock でモデルが有効化されているか確認
- IAM ロール/ユーザーに `bedrock:InvokeModel` 権限があるか確認
- 実行リージョンでモデルが利用可能か確認

### モデル未検出エラー

- `BEDROCK_MODEL_ID` が正しいか確認
- モデル ID に `bedrock/us.anthropic...` が含まれているか確認
- Inference Profile ID の使用を検討

### リージョン不一致エラー

- `AWS_REGION_NAME` がモデルの有効リージョンと一致しているか確認
- AWS CLI の設定リージョンと環境変数の一致を確認

### 認証エラー

- ローカル実行: AWS プロファイル設定を確認
- Lambda 実行: 実行ロールの権限を確認
- AWS SSO の場合: 有効なセッションがあるか確認

## 構造化出力について

このプロジェクトでは rigging の **Pydantic モデル（`rg.Model`）** を使用して構造化された出力を取得します：

### 仕組み

1. **モデル定義**: `app/models.py` で `Product` と `Catalog` クラスを定義
2. **タグ例の提示**: `Catalog.xml_example()` をプロンプトに含めて Claude に構造を示す
3. **厳格な抽出**: `.until_parsed_as(Catalog)` で構造化を強制し、`.parse(Catalog)` で型安全に取得

### サンプル出力

```python
{
    'items': [
        {'name': 'ノートPC', 'price': 89800.0, 'in_stock': True},
        {'name': 'ワイヤレスマウス', 'price': 3980.0, 'in_stock': False},
        {'name': 'モニター', 'price': 24800.0, 'in_stock': True}
    ]
}
```

## プロジェクト構成

```
rigging-bedrock-sync-sample/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
└── app/
    ├── __init__.py
    ├── models.py      # Pydantic モデル（rg.Model）定義
    ├── core.py        # 非同期の実処理（構造化出力抽出）
    ├── main.py        # ローカル実行用：同期エントリポイント
    └── handler.py     # Lambda用：同期ハンドラー
```

## トラブルシューティング（構造化出力関連）

### 構造化出力の解析失敗

- **症状**: `MaxDepth` エラーや整合性エラー
- **対策**: 
  - タグ例をより具体的にする
  - プロンプトに属性の説明を追加する
  - `max_depth` パラメータを増やす
  - モデルの応答形式を確認する
