
# 📬 Gmail to Telegram Alert Notifier

A simple Python app that watches your Gmail inbox and forwards specific **TradingView alerts** to your **Telegram** chat. This helps you receive important crypto/stock signals instantly on your phone — no paid webhook or TradingView Pro needed.

---

## 🚀 Features

- ✅ Checks Gmail inbox every 5 seconds
- ✅ Filters for specific sender and subject
- ✅ Sends matching alerts to Telegram
- ✅ Prevents duplicate messages
- ✅ Uses only HTTP requests (no Telegram libraries)

---

## 💠 Requirements

- Python 3.7+
- Gmail account with **App Password**
- A Telegram Bot via [@BotFather](https://t.me/BotFather)
- Your Telegram user or group **chat ID**

---

## 📦 Installation

Install required packages:

```bash
pip install imapclient pyzmail36 requests
```

---

## ⚙️ Configuration

Edit these variables in the script:

```python
EMAIL = 'your_email@gmail.com'
PASSWORD = 'your_16_char_gmail_app_password'

SENDER_EMAIL = 'noreply@tradingview.com'     # Or any specific email sender
SUBJECT_FILTER = 'Alert: order sell @ CRVUSDT'  # Or use 'BUY', 'SELL', etc.

TELEGRAM_TOKEN = 'your_bot_token'
TELEGRAM_CHAT_ID = 'your_chat_id'
```

📌 To get a Gmail **App Password**, follow: [Google App Password Setup](https://myaccount.google.com/apppasswords)

📌 To find your **Telegram chat ID**, you can use a bot like [@userinfobot](https://t.me/userinfobot).

---

## ▶️ Usage

```bash
python app.py
```

You’ll see logs like:

```
📬 Watching Gmail inbox for TradingView alerts...
📤 Sent to Telegram: Alert: order sell @ CRVUSDT
```

---

## 💡 How It Works

- Connects to Gmail over IMAP securely
- Searches for unseen emails from a specific sender
- Filters subjects for matching keywords
- Sends alerts to Telegram using raw HTTP `requests.post`
- Keeps track of already seen messages to avoid duplicates

---

## 🔐 Security Note

Do **NOT** hardcode your credentials in public repositories. Use environment variables or a `.env` file if sharing or deploying the code.

---

## 📃 License

MIT License — free to use, modify, and share.