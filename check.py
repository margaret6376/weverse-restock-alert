import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCT_URL = "https://shop.weverse.io/zh-tw/shop/JPY/artists/128/sales/44138"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(PRODUCT_URL, headers=headers, timeout=30)
response.raise_for_status()

text = response.text

# Weverse currently uses "售罄" when the item is unavailable.
sold_out = "售罄" in text or "SOLD OUT" in text.upper()

if not sold_out:
    message = (
        "🔔 Weverse 補貨了！\n\n"
        "SUPER JUNIOR 10CM KEYRING\n\n"
        f"{PRODUCT_URL}"
    )

    telegram_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    )

    requests.post(
        telegram_url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=30,
    )

    print("RESTOCK DETECTED!")
else:
    print("Still sold out.")
