import os
import asyncio
from dotenv import load_dotenv
from app.core import chat_once


def _setup_env():
    """
    環境変数を設定し、必要なデフォルト値を設定する
    
    Returns:
        str: 使用するモデル ID
    """
    load_dotenv()
    
    # デフォルト値の設定
    if os.getenv("AWS_REGION_NAME") is None:
        os.environ["AWS_REGION_NAME"] = "us-west-2"
    
    # AWS_PROFILE はローカルのみ任意
    prof = os.getenv("AWS_PROFILE")
    if prof:
        os.environ["AWS_PROFILE"] = prof
    
    model_id = os.getenv("BEDROCK_MODEL_ID", "bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0")
    return model_id


def run():
    """
    ローカル実行用の同期エントリポイント
    """
    model_id = _setup_env()
    loop = asyncio.get_event_loop()
    
    try:
        res = loop.run_until_complete(chat_once(model_id, "こんにちは、同期ハンドラーのテストです。"))
        print(res)
    except Exception as e:
        raise RuntimeError(
            f"{e}\n"
            "確認項目: Bedrockでモデル有効化 / AWS_REGION_NAMEの一致 / 認証(プロファイルorロール) / "
            "モデルID(必要なら us.anthropic.* のInference Profile) "
        )


if __name__ == "__main__":
    run()