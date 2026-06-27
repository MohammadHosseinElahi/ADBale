import requests
import time
from pyad import aduser
from pyad import pyad
from pyad import adcomputer

pyad.set_defaults(
    ldap_server="your_domain_controller", 
    username="admin_username",            
    password="admin_password",
)

Admin_Username = "root"
Admin_Password = "passwd"

BOT_TOKEN = ""
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"
user_states = {}



def unlock_user_AC(username, chat_id):
    try:
        user = aduser.ADUser.from_cn(username)
        user.unlock()
        send_message(chat_id, f"User {username} Unlooked.")
    except Exception as e:
        send_message(chat_id, f"Don't found this user:{username}")
    
def reset_password_AC(username, new_password, chat_id):
    try:
        user = aduser.ADUser.from_cn(username)
        user.set_password(new_password)
        send_message(chat_id, f"Password user {username} changed.")
    except Exception as e:
        send_message(chat_id, f"Don't found this user:{username}")

def enable_disable_user_AC(username, state, chat_id):
    try:
        user = aduser.ADUser.from_cn(username)
        if state == "enable":
            user.enable()
            send_message(chat_id, f"User {username} enabled.")

        elif state == "disable":
            user.disable()
            send_message(chat_id, f"User {username} disabled.")

    except Exception as e:
        send_message(chat_id, f"Don't found this user:{username}")
        # print(f"خطا در تغییر وضعیت کاربر: {str(e)}")

def delete_computer_AC(computer_name, chat_id):
    try:
        computer = adcomputer.ADComputer.from_cn(computer_name)       
        computer.delete()        
        send_message(chat_id, f"Computer name {computer_name} deleted.")
        return True
    except Exception as e:
        send_message(chat_id, f"Computer name {computer_name} don't found.")
        return False



def send_help(chat_id, user_id):
    if user_states[user_id]["states"] == "LOGGED_IN":
            send_message(chat_id, """Wlcome
You can remove computer name with /rcn
You can unlook user with /uu
You can enable/disable user with /edu
You can reset password user with /rp
You can logout with /logout""")
    else:
        send_message(chat_id, """Hello
you can login with /login""")
            
def get_updates(offset=None):
    try:
        url = f"{BASE_URL}/getUpdates"
        params = {"offset": offset} if offset else {}
        response = requests.get(url, params=params, timeout=5)
        return response.json()
    except:
        return {}
    
def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

def handle_message(update):
    if update == {}:
        return
    message = update.get("message")
    text = message.get("text")
    user_id = str(message.get("from").get("id"))
    chat_id = str(message.get("chat").get("id"))
    
    if not user_id or not chat_id:
        return
    
    if user_id not in user_states:
        user_states[user_id] = {"states":"MAIN_MENU","rp_state":"","rcn_state":"","uu_state":"","edu_state":""}

    state = user_states.get(user_id)["states"]

    if text == "/start":
        send_help(chat_id, user_id)
    
    elif state == "GET_USERNAME":
        user_states[user_id].update({"username":[text]})
        user_states[user_id]["states"] = "GET_PASSWORD"
        send_message(chat_id, "Enter your password:")
    
    elif state == "GET_PASSWORD":
        if user_states[user_id]["username"][0] == Admin_Username and text == Admin_Password:
            user_states[user_id]["states"] = "LOGGED_IN"
            user_states[user_id]["username"].append(text)
            send_message(chat_id, """Wlcome
You can remove computer name with /rcn
You can unlook user with /uu
You can enable/disable user with /edu
You can reset password user with /rp
You can logout with /logout""")
        else:
            user_states[user_id]["states"] = ["MAIN_MENU"]
            user_states[user_id].pop("username")
            send_message(chat_id, "Wrong")


    elif text == "/login":
        if user_states[user_id]["states"] == "LOGGED_IN":
            send_message(chat_id, "You are login")    
        else:
            user_states[user_id]["states"] = "GET_USERNAME"
            send_message(chat_id, "Enter Username:")
    
    elif text == "/help":
        if user_states[user_id]["states"] == "LOGGED_IN":
            send_message(chat_id, """Wlcome
You can remove computer name with /rcn
You can unlook user with /uu
You can enable/disable user with /edu
You can reset password user with /rp
You can logout with /logout""")
        else:
            send_message(chat_id, """Hello
                     you can login with /login""")
    
    elif text == "/rp":
        if user_states[user_id]["states"] == "LOGGED_IN":
            user_states[user_id].update({'rp_state':'rp1'})
            send_message(chat_id, "Enter your username want to reset password:")
        else:
            send_message(chat_id, "You must log in")
    elif user_states[user_id]["rp_state"] == "rp1":
        user_states[user_id].update({'rp':[text]})
        user_states[user_id]['rp_state'] = 'rp2'
        send_message(chat_id, "Enter new password:")

    elif user_states[user_id]["rp_state"] == "rp2":
        user_states[user_id]['rp'].append(text)
        user_states[user_id]["rp_state"] = ""
        send_message(chat_id, "ok")
        # send to function
        reset_password_AC(user_states[user_id]['rp'][0], user_states[user_id]['rp'][1], chat_id)
        # Delete value
        user_states[user_id].pop('rp')
    
    elif text == "/rcn":
        if user_states[user_id]["states"] == "LOGGED_IN":
            user_states[user_id].update({'rcn_state':'rcn1'})
            send_message(chat_id, "Enter your coputer name want to remove:")
        else:
            send_message(chat_id, "You must log in")

    elif user_states[user_id]["rcn_state"] == "rcn1":
        user_states[user_id].update({'rcn':[text]})
        user_states[user_id]["rcn_state"] = ""
        send_message(chat_id, "ok")
        # send to function
        delete_computer_AC(user_states[user_id]['rcn'][0], chat_id)
        # Delete value
        user_states[user_id].pop('rcn')

    elif text == "/uu":
        if user_states[user_id]["states"] == "LOGGED_IN":
            user_states[user_id].update({'uu_state':'uu'})
            send_message(chat_id, "Enter your user want to unlook:")
        else:
            send_message(chat_id, "You must log in")

    elif user_states[user_id]["uu_state"] == "uu":
        user_states[user_id].update({'uu':[text]})
        user_states[user_id]["uu_state"] = ""
        send_message(chat_id, "ok")
        # send to function
        unlock_user_AC(user_states[user_id]['uu'][0], chat_id)
        # Delete value
        user_states[user_id].pop('uu')
    
    elif text == "/edu":
        if user_states[user_id]["states"] == "LOGGED_IN":
            user_states[user_id].update({'edu_state':'edu1'})
            send_message(chat_id, "Enter your user want to enable/disable:")
        else:
            send_message(chat_id, "You must log in")

    elif user_states[user_id]["edu_state"] == "edu1":
        user_states[user_id].update({'edu':[text]})      
        user_states[user_id]['edu_state'] = 'edu2'
        send_message(chat_id, "enable or disable:")

    elif user_states[user_id]["edu_state"] == "edu2":
        user_states[user_id]['edu'].append(text)
        user_states[user_id]["edu_state"] = ""
        send_message(chat_id, "ok")
        # send to function
        enable_disable_user_AC(user_states[user_id]['edu'][0], user_states[user_id]['edu'][1], chat_id)
        # Delete value
        user_states[user_id].pop('edu')
            
    elif text == "/logout":
        user_states.pop(user_id)
        send_message(chat_id, "bye")

    else:
        send_help(chat_id, user_id)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            handle_message(update)
        # time.sleep(1)

if __name__ == "__main__":
    main()