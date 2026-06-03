import requests
import threading
import time

ESP_IP = "10.49.144.120"
SEND_URL = f"http://{ESP_IP}/send"
RECV_URL = f"http://{ESP_IP}/recv"

def poll_loop():
    while True:
        try:
            r = requests.get(RECV_URL, timeout = 2)
            msg = r.text.strip()
            if msg:
                print(f"\r[ESP32] {msg}\n[Python] ", end = "", flush = True)
        except Exception as e:
            print(f"\r[error] {e}\n[Python] ", end = "", flush = True)
        time.sleep(0.2)

threading.Thread(target = poll_loop, daemon = True).start()

print("ESP32 chat ready. Type a message and press Enter.\n")
while True:
    try:
        msg = input("[Python] ").strip()
        if not msg:
            continue
        requests.post(SEND_URL, data = msg, timeout = 2)
    except KeyboardInterrupt:
        print("\nBye.")
        break
    except Exception as e:
        print(f"[error] {e}")