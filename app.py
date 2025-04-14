import time
import imapclient
import pyzmail
import requests

# === Gmail Config ===
EMAIL = ''
PASSWORD = ''  # Use the 16-character app password here
SENDER_EMAIL = 'noreply@tradingview.com'
SUBJECT_FILTER = 'Alert: order'

# === Telegram Config ===
TELEGRAM_ADDRESS =  'https://api.telegram.org'
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# === Internal State ===
last_seen_uid = None

def send_telegram_message(text):
    url = f"{TELEGRAM_ADDRESS}/bot{TELEGRAM_TOKEN}/sendMessage"
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
    global last_seen_uid
    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder('INBOX', readonly=True)

        uids = client.search(['FROM', SENDER_EMAIL])
        uids.sort()

        if last_seen_uid is None:
            # On first run, set the latest UID and skip everything before it
            last_seen_uid = uids[-1] if uids else 0
            print(f"🚫 Ignoring existing emails. Starting from UID {last_seen_uid + 1}")
            return

        new_uids = [uid for uid in uids if uid > last_seen_uid]

        for uid in new_uids:
            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
            subject = message.get_subject()

            if SUBJECT_FILTER.lower() not in subject.lower():
                print(f"ℹ️ Skipping subject: {subject}")
                continue

            # Add emoji
            if 'buy' in subject.lower():
                subject = f"🟢 {subject}"
            elif 'sell' in subject.lower():
                subject = f"🔴 {subject}"

            send_telegram_message(subject)
            last_seen_uid = uid

if __name__ == '__main__':
    print("📨 Waiting for new TradingView alerts...")
    while True:
        try:
            check_email()
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(5)