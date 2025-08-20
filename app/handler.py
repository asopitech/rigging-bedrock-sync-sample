import os
import json
import asyncio
from app.core import generate_catalog


def lambda_handler(event, context):
    """
    AWS Lambda 用の同期ハンドラー - 構造化出力でカタログを生成
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        dict: HTTP response with statusCode and body
    """
    try:
        # Lambda 環境変数から設定を取得
        model_id = os.environ.get(
            "BEDROCK_MODEL_ID", 
            "bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0"
        )
        
        # AWS_REGION_NAME のデフォルト設定
        if os.environ.get("AWS_REGION_NAME") is None:
            os.environ["AWS_REGION_NAME"] = "us-west-2"
        
        # イベントループでカタログ生成を実行
        loop = asyncio.get_event_loop()
        message = "Lambda用の簡易カタログを3件作成してください。商品名、価格、在庫状況を含めてください。"
        catalog = loop.run_until_complete(generate_catalog(model_id, message))
        
        # レスポンスを作成
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(catalog.model_dump(), ensure_ascii=False)
        }
        
    except Exception as e:
        # エラーレスポンス
        error_message = {
            "error": str(e),
            "message": "カタログ生成中にエラーが発生しました",
            "troubleshooting": [
                "Bedrock でモデルが有効化されているか確認",
                "AWS_REGION_NAME と実際のリージョンが一致しているか確認",
                "Lambda 実行ロールに bedrock:InvokeModel* 権限があるか確認",
                "モデル ID の形式が正しいか確認"
            ]
        }
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(error_message, ensure_ascii=False)
        }