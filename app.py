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
TELEGRAM_ADDRESS =  'https://api.telegram.org'
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# === Track last seen UID and processed UIDs ===
last_seen_uid = 0
seen_uids = set()

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

def get_last_uid(client):
    client.select_folder('INBOX', readonly=True)
    uids = client.search(['ALL'])
    return max(uids) if uids else 0

def check_email():
    global last_seen_uid, seen_uids
    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        client.select_folder('INBOX', readonly=True)

        # Get only UIDs greater than last seen
        new_uids = client.search(['UID', f'{last_seen_uid + 1}:*'])

        for uid in new_uids:
            if uid in seen_uids:
                continue

            raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
            subject = message.get_subject()
            from_address = message.get_addresses('from')[0][1]

            if from_address.lower() != SENDER_EMAIL.lower():
                continue

            if 'buy' in subject.lower():
                subject = f"🟢 {subject}"
            elif 'sell' in subject.lower():
                subject = f"🔴 {subject}"

            if SUBJECT_FILTER.lower() in subject.lower():
                send_telegram_message(subject)
            else:
                print(f"ℹ️ Skipping non-matching subject: {subject}")

            seen_uids.add(uid)
            last_seen_uid = max(last_seen_uid, uid)

if __name__ == '__main__':
    print("📨 Watching Gmail inbox for new TradingView alerts...")

    with imapclient.IMAPClient('imap.gmail.com', ssl=True) as client:
        client.login(EMAIL, PASSWORD)
        last_seen_uid = get_last_uid(client)
        print(f"🧭 Starting from UID: {last_seen_uid}")

    while True:
        try:
            check_email()
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(5)