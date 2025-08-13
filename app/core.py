import rigging as rg


async def chat_once(model_id: str, message: str) -> str:
    """
    Rigging を使って単発チャットを送る非同期関数
    
    Args:
        model_id: Bedrock モデル ID (例: bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0)
        message: 送信するメッセージ
        
    Returns:
        Claude からの応答文字列
    """
    gen = rg.get_generator(model_id)
    chat = await gen.chat(message).run()
    return chat.last.content