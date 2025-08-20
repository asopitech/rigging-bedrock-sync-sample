import os
import asyncio
from dotenv import load_dotenv
from app.core import generate_catalog


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
    ローカル実行用の同期エントリポイント - 構造化出力でカタログを生成
    """
    model_id = _setup_env()
    loop = asyncio.get_event_loop()
    
    try:
        # サンプルメッセージでカタログを生成
        message = "3つの商品のカタログを作成してください。catalogに、product(name: str, price: float, in_stock: bool)を3つ含めて返してください。例：ノートパソコン(89800円、在庫あり)、ワイヤレスマウス(2980円、在庫あり)、USB-Cハブ(4500円、在庫なし)"
        catalog = loop.run_until_complete(generate_catalog(model_id, message))
        
        # 結果を整形して出力
        print(f"Generated Catalog: {catalog}")
        
    except Exception as e:
        raise RuntimeError(
            f"{e}\n"
            "確認項目: Bedrockでモデル有効化 / AWS_REGION_NAMEの一致 / 認証(プロファイルorロール) / "
            "モデルID(必要なら us.anthropic.* のInference Profile) "
        )


if __name__ == "__main__":
    run()