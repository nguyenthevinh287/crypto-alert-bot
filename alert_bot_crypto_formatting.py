import requests
import time

TOKEN = '7685442403:AAFyqbcBPBx8QjuiBcQmEnEqHKnqoh8nSL0'
CHAT_ID = '5522779350'

crypto_symbols = ['BTC', 'ETH', 'BOME', 'TON', 'SOL', 'FTM', 'AVAX', 'NEAR', 'MATIC']
base_prices = {}
alert_sent = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def get_price_crypto(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT'
    r = requests.get(url).json()
    return float(r['price'])

def percent_change(new, old):
    return abs((new - old) / old) * 100 if old != 0 else 0

def format_price(symbol, price):
    if symbol == 'BOME':
        return f"{price:,.8f}"
    elif symbol in ['BTC', 'ETH']:
        return f"{price:,.2f}"
    else:
        return f"{price:,.4f}"

send_telegram_message("✅ Bot đang theo dõi BTC, ETH, BOME, TON và altcoin. Cảnh báo nếu biến động ±1% trong 1 phút!")

while True:
    try:
        for sym in crypto_symbols:
            base_prices[sym] = get_price_crypto(sym)
        alert_sent = {s: False for s in crypto_symbols}

        for _ in range(12):  # 5s x 12 = 1 phút
            for sym in crypto_symbols:
                current_price = get_price_crypto(sym)
                change = percent_change(current_price, base_prices[sym])
                formatted = format_price(sym, current_price)
                print(f"[{sym}] {formatted} ({change:.2f}%)")
                if change >= 1 and not alert_sent[sym]:
                    send_telegram_message(f"📈 {sym} biến động {change:.2f}%\\nGiá mới: {formatted} USD")
                    alert_sent[sym] = True
            time.sleep(5)

    except Exception as e:
        send_telegram_message(f"❗Lỗi: {e}")
        time.sleep(60)
