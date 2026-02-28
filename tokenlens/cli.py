import argparse
import sys
from tokenlens.core import get_encoder, tokenize, MODELS, PRICING, COLORS

# True color ANSI background escapes matching the app.py UI
ANSI_BG_COLORS = [
    "\033[48;2;124;106;255m", # tok-0 (rgba(124,106,255))
    "\033[48;2;255;106;171m", # tok-1
    "\033[48;2;106;220;255m", # tok-2
    "\033[48;2;255;200;80m",  # tok-3
    "\033[48;2;80;255;160m",  # tok-4
    "\033[48;2;255;140;80m",  # tok-5
    "\033[48;2;200;80;255m",  # tok-6
    "\033[48;2;80;200;255m",  # tok-7
]
ANSI_RESET = "\033[0m"
ANSI_FG_BLACK = "\033[38;2;0;0;0m" # Black text for better contrast

def print_colored_tokens(tokens):
    """Print tokens with their corresponding background colors."""
    for i, t in enumerate(tokens):
        color = ANSI_BG_COLORS[i % COLORS]
        # Clean up newlines for inline printing so it doesn't break the background blocks
        text = t["text"].replace("\n", "↵")
        sys.stdout.write(f"{color}{ANSI_FG_BLACK}{text}{ANSI_RESET}")
    print()

def print_table(tokens, limit=100):
    """Print a clean table of tokens up to a given limit."""
    print(f"{'Index':>8} | {'Token':<20} | {'ID':>8}")
    print("-" * 44)
    for i, t in enumerate(tokens[:limit]):
        text_repr = repr(t["text"])[1:-1] # Remove the quotes from repr
        if len(text_repr) > 17:
             text_repr = text_repr[:16] + "…"
        print(f"{i:>8} | {text_repr:<20} | {t['id']:>8}")

    if len(tokens) > limit:
        print(f"  ... + {len(tokens)-limit} more tokens")

def main():
    parser = argparse.ArgumentParser(description="TokenLens CLI - A zero-dependency tokenizer visualizer")
    parser.add_argument("text", nargs="?", help="Text to tokenize (optional if piped via stdin)")
    parser.add_argument("-e", "--encoder", default="cl100k_base", help="Encoding name (default: cl100k_base)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output (useful for logs/redirection)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Output only the total token count")
    parser.add_argument("-s", "--stats", action="store_true", help="Always output statistics and cost estimates (default if interactive)")
    
    args = parser.parse_args()
    
    # Handle stdin pipeline if text not provided
    if not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        text = args.text
        if text is None:
            parser.print_help()
            sys.exit(1)
            
    try:
        enc = get_encoder(args.encoder)
    except Exception as e:
        print(f"Error loading encoder: {e}", file=sys.stderr)
        sys.exit(1)
        
    tokens = tokenize(text, enc)
    
    # Quiet mode for machine parsing
    if args.quiet:
        print(len(tokens))
        sys.exit(0)
        
    if not args.no_color:
        print("--- Token Visualization ---")
        print_colored_tokens(tokens)
        print()
    else:
        print("--- Tokens Dump ---")
        sys.stdout.write("".join([t["text"] for t in tokens]) + "\n\n")
        
    print("--- Token Table ---")
    print_table(tokens)
    print()
    
    # Print stats if asked or if it's an interactive TTY and not piped out
    if args.stats or (sys.stdout.isatty() and not args.quiet):
        print("--- Statistics ---")
        print(f"Tokens:      {len(tokens):,}")
        print(f"Characters:  {len(text):,}")
        ratio = len(text) / len(tokens) if tokens else 0
        print(f"Chars/token: {ratio:.2f}")
        print(f"Encoder:     {args.encoder}")
        
        print("\n--- Estimated Input Cost ---")
        for model_name, price_per_m in PRICING.items():
            cost = len(tokens) / 1_000_000 * price_per_m
            print(f"{model_name:<25} ${cost:.6f}")
        print()

if __name__ == "__main__":
    main()
