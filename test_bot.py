# import requests

# token = ""
# chat_id = ""

# url = f"https://api.bale.ai/bot{token}/sendMessage"

# keyboard = {
#     "type": "keyboard",
#     "buttons": [
#         [
#             {"type": "text", "text": "دکمه اول"},
#             {"type": "text", "text": "دکمه دوم"}
#         ]
#     ]
# }

# payload = {
#     "chat_id": chat_id,
#     "text": "لطفا یکی از دکمه‌ها را انتخاب کنید:",
#     "keyboard": keyboard
# }

# response = requests.post(url, json=payload)
# print(response.json())












import requests

token = "48729529:NKv5639sutJckUN1BVWuIplJZ6rDzG6WwTnfgZ1l"
url = f"https://api.bale.ai/bot{token}/sendMessage"

def get_updates(offset=None):
    try:
        url = f"{url}/getUpdates"
        params = {"offset": offset} if offset else {}
        response = requests.get(url, params=params, timeout=5)
        print(response)
        return response.json()
    except:
        return {}
        


def send_mess(r):
    l = r.json().get("message").get("text")
    chat_id = l.get("chat").get("id")
    print (chat_id)
    keyboard = {
        "type": "keyboard",
        "buttons": [
            [
                {"type": "text", "text": "دکمه اول"},
                {"type": "text", "text": "دکمه دوم"}
            ]
        ]
    }

    payload = {
        "chat_id": chat_id,
        "text": "لطفا یکی از دکمه‌ها را انتخاب کنید:",
        "keyboard": keyboard
    }

    response = requests.post(url, json=payload)
    print(response.json())

last_update_id = None
while True:
    updates = get_updates(last_update_id)
    print(updates)
    for update in updates.get("result", []):
        last_update_id = update["update_id"] + 1
        send_mess(update)
    # time.sleep(1)



