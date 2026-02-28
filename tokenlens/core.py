import tiktoken

# ─── Model configs ────────────────────────────────────────────────────────────
MODELS = {
    "gpt-4 / gpt-3.5 (cl100k_base)": "cl100k_base",
    "gpt-4o (o200k_base)":            "o200k_base",
    "text-davinci (p50k_base)":        "p50k_base",
    "gpt-2 / gpt-3 (r50k_base)":       "r50k_base",
}

PRICING = {
    "GPT-4o (input)":       5.00,
    "GPT-4 (input)":       30.00,
    "GPT-3.5-turbo (input)": 0.50,
}

COLORS = 8

def get_encoder(encoding_name: str):
    """Retrieve the tiktoken encoder for the given encoding name."""
    return tiktoken.get_encoding(encoding_name)

def tokenize(text: str, enc) -> list[dict]:
    """Tokenize text and return a list of dictionaries with token details."""
    ids = enc.encode(text)
    tokens = []
    for i, tok_id in enumerate(ids):
        tok_bytes = enc.decode_single_token_bytes(tok_id)
        try:
            tok_text = tok_bytes.decode("utf-8")
        except UnicodeDecodeError:
            tok_text = repr(tok_bytes)
        tokens.append({"id": tok_id, "text": tok_text, "bytes": len(tok_bytes)})
    return tokens
