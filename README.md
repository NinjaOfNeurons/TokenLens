

# 🔬 TokenLens

> Wanna see how AI chops your text into tiny weird pieces? This shows it. 🟢🔵🟡


**Demo video:** [Watch it do its thing 🎥]
https://github.com/user-attachments/assets/your-video.mp4


---

## What even is TokenLens?

AI doesn’t read like humans. It breaks stuff into **tokens** — sometimes words, sometimes weird fragments, sometimes punctuation.

TokenLens lets you:

* See why prompts cost $$$
* Figure out why AI freaks out sometimes
* Compare how different models slice your text

---

## Features (or whatever)

* Colors for tokens (because why not)
* Token IDs, indexes, counts, ratios
* Shows API cost for GPT-4o, GPT-4, GPT-3.5 💸
* Flip between 4 encoders
* Updates as you type ⚡

---

## Supported Encoders

| Encoding      | Models               | Vocab    |
| ------------- | -------------------- | -------- |
| `cl100k_base` | GPT-4, GPT-3.5-turbo | 100k-ish |
| `o200k_base`  | GPT-4o               | 200k-ish |
| `p50k_base`   | text-davinci-002/003 | 50k-ish  |
| `r50k_base`   | GPT-2, GPT-3         | 50k-ish  |

---

## Run it (super easy)

```bash id="tz7p2m"
git clone https://github.com/your-username/TokenLens.git
cd TokenLens
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` and watch the magic happen ✨

---

## Token money stuff

| Model         | Cost / 1M tokens |
| ------------- | ---------------- |
| GPT-4o        | $5               |
| GPT-4         | $30              |
| GPT-3.5-turbo | $0.50            |

> Check OpenAI if prices matter.

---

## Why tokens even matter

* Tokens = text chunks (~4 chars each)
* BPE = AI’s way of merging bytes until vocab is big
* Costs, context windows, weird splits = all token stuff

---

## Project tree (looks organized, kinda)

```
TokenLens/
├── app.py            ← web app
├── requirements.txt  ← boring dependencies
└── README.md         ← this lazy thing
```

---

## License

MIT. Do what you want. Seriously.

---

*Built to learn. Inspired by [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app)*

