import rigging as rg
from app.models import Catalog
from rigging.watchers import make_stream_to_logs

stream_to_logs = make_stream_to_logs()

def build_prompt(user_message: str) -> str:
    return f"""
あなたは厳密なXMLシリアライザです。以下の契約に従い、**有効なXMLのみ**を返します。

[出力契約]
あなたは厳密なXMLシリアライザです。
- ルート要素は <catalog>…</catalog> とする。
- 中には <product> 要素のみを複数含める。
- <product> の中には <name>（文字列）, <price>（数値）, <in_stock>（true/false小文字）の3要素を必ず順に含める。
- 余計なテキスト・コメント・XML宣言は禁止。
- 出力は XML 本体のみ。

例:
<catalog>
  <product>
    <name>Sample</name>
    <price>123.45</price>
    <in_stock>true</in_stock>
  </product>
  <product>
    <name>Another</name>
    <price>67.89</price>
    <in_stock>false</in_stock>
  </product>
</catalog>

[タスク]
- 次の要求に基づき、3件の product を作成して返す。
- 商品名は簡潔な英語または日本語。価格は現実的な数値。in_stock は整合的に。

[要求]
{user_message}

[最終指示]
- 出力は **<catalog> から </catalog> まで**のXML本体のみ。
- その前後に改行・空白・他の記号・説明は一切つけない。
""".strip()


async def generate_catalog(model_id: str, message: str) -> Catalog:
    """
    Generate a catalog using AWS Bedrock with structured output.
    
    Args:
        model_id: The Bedrock model ID to use
        message: The user message for catalog generation
        
    Returns:
        Catalog: Parsed catalog with structured products
        
    Raises:
        Exception: If parsing fails with helpful troubleshooting hints
    """
    try:
        gen = rg.get_generator(model_id)
        
        # Include the XML example in the prompt for structured output
        prompt = build_prompt(message)

        # Create pipeline with structured parsing
        pipeline = gen.chat(prompt).until_parsed_as(Catalog, max_depth=2)
        
        # Execute the pipeline
        chat = await pipeline.watch(stream_to_logs).run()

        # Parse the result
        catalog = chat.last.parse(Catalog)
        
        return catalog
        
    except Exception as e:
        # Provide helpful error message with troubleshooting hints
        error_msg = (
            f"構造化出力の抽出に失敗しました: {str(e)}\n"
            "トラブルシューティングのヒント:\n"
            "- タグ例をより具体的にする\n"
            "- プロンプトに属性の説明を追加する\n"
            "- max_depthパラメータを増やす\n"
            "- モデルの応答形式を確認する"
        )
        raise Exception(error_msg) from e