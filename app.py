import time
import imapclient
import pyzmail
import requests

# === Gmail Config ===
EMAIL = ''
PASSWORD = ''  # Use the 16-character app password here
# SENDER_EMAIL = 'noreply@tradingview.com'
SUBJECT_FILTER = 'Alert: order'

# === Telegram Config ===
TELEGRAM_API =  ''
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# === Memory to avoid duplicate messages ===
seen_uids = set()

def send_telegram_message(text):
    url = f"{TELEGRAM_API}/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print(f"📤 Sent to Telegram: {text}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")

def check_email():
    global seen_uids
    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder('INBOX', readonly=True)

        # Search for unseen messages from TradingView
        uids = client.search(['UNSEEN', 'FROM', SENDER_EMAIL])
        for uid in uids:
            if uid in seen_uids:
                continue  # Already processed

            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
            subject = message.get_subject()

            # Determine the prefix emoji
            if 'buy' in subject.lower():
                subject = f"🟢 {subject}"
            elif 'sell' in subject.lower():
                subject = f"🔴 {subject}"

            if SUBJECT_FILTER.lower() in subject.lower():
                send_telegram_message(subject)
            else:
                print(f"ℹ️ Skipping non-matching subject: {subject}")

            seen_uids.add(uid)

if __name__ == '__main__':
    print("📨 Watching Gmail inbox for TradingView alerts...")
    while True:
        try:
            check_email()
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(5)