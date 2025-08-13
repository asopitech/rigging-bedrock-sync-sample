import os
import asyncio
from app.core import chat_once


def lambda_handler(event, context):
    """
    AWS Lambda 用の同期ハンドラー
    
    Args:
        event: Lambda イベント
        context: Lambda コンテキスト
        
    Returns:
        dict: HTTP レスポンス形式の辞書
    """
    model_id = os.environ.get("BEDROCK_MODEL_ID", "bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0")
    
    # Lambdaでは通常ロール認証。必要なら AWS_REGION_NAME をLambda環境変数で指定。
    loop = asyncio.get_event_loop()
    
    try:
        body = loop.run_until_complete(chat_once(model_id, "Lambda同期ハンドラーのテストです。"))
        return {"statusCode": 200, "body": body}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}