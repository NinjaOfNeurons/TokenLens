
#  TokenLens CLI

> See how AI models tokenize your text — straight from your terminal. No browser needed. 

---

## Demo Screenshot (GUI Reference)

Here’s the GUI version you’re converting to CLI, so you know what it’s doing:

![TokenLens GUI](https://github.com/user-attachments/assets/a3c4b5ff-1187-4c7b-a4cd-d0e0f817b8df)

---

## What is TokenLens CLI?

TokenLens CLI is a **Command-Line Interface** for TokenLens:

* Input your text in terminal
* See how it’s split into **tokens**
* Pick different encoders (`cl100k_base`, `o200k_base`, etc.)
* View **token IDs**, counts, and the full token list
* Works great for scripts, automation, or quick testing

---

## Installation

1. Make sure you have Python 3.8+

```bash id="python_check"
python --version
```

2. Clone the repo and enter CLI branch

```bash id="git_clone_cli"
git clone https://github.com/NinjaOfNeurons/TokenLens.git
cd TokenLens
git checkout cli-version
```

3. (Optional but recommended) Create a virtual environment

```bash id="venv_setup"
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies

```bash id="pip_install_cli"
pip install tiktoken
```

---

## Usage

```bash id="cli_usage"
python tokenlens_cli.py "Hello world!" --encoder cl100k_base
```

Output example:

```
Input text: Hello world!
Encoder: cl100k_base
Tokens (4): [15496, 2157, 0, 50256]
```

* `--encoder` is optional; default is `cl100k_base`
* Works with encoders: `cl100k_base`, `o200k_base`, `p50k_base`, `r50k_base`

---

## Why CLI?

* Fast token inspection without opening a browser
* Ideal for automation, scripts, or testing prompts
* Fun for contributors to add **bonus features** like colored output, JSON export, or cost estimation

---

## Contributing

Want to make it cooler? Suggestions:

* Add **color-coded tokens** in terminal
* Output **JSON / CSV** of tokens
* Add **API cost estimates**
* Add **unit tests** or **examples**

> PRs welcome! Start on the `cli-version` branch.

---

## License

MIT — do whatever you want.

