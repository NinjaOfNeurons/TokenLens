import argparse
from tiktoken import get_encoding

# Pick default encoder (could make it an option)
ENCODERS = {
    "cl100k_base": "cl100k_base",
    "o200k_base": "o200k_base",
    "p50k_base": "p50k_base",
    "r50k_base": "r50k_base"
}

def main():
    parser = argparse.ArgumentParser(description="TokenLens CLI – see how AI tokenizes text")
    parser.add_argument("text", help="Text to tokenize", type=str)
    parser.add_argument("--encoder", choices=ENCODERS.keys(), default="cl100k_base")
    args = parser.parse_args()

    encoding = get_encoding(ENCODERS[args.encoder])
    tokens = encoding.encode(args.text)
    
    print(f"\nInput text: {args.text}\n")
    print(f"Encoder: {args.encoder}")
    print(f"Tokens ({len(tokens)}): {tokens}")

if __name__ == "__main__":
    main()