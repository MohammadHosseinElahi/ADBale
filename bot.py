import requests
import time
# from pyad import aduser
# from pyad import pyad
# from pyad import adcomputer


# pyad.set_defaults(
#     ldap_server="your_domain_controller", 
#     username="admin_username",            
#     password="admin_password",
# )

BOT_TOKEN = "492123909:6yPCF4smIzgi9mzU5Oa5XpAwAcBilYRQlJY"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"
user_states = {}

def find_index(index,List):
    for i in List:
        if index in i:
            return List.index(i) 
    return False 

# def reset_password_AC(username, new_password):
#     try:
#         user = aduser.ADUser.from_cn(username)
#         user.set_password(new_password)
#         print(f"پسورد کاربر {username} با موفقیت تغییر یافت.")
#         return True
#     except Exception as e:
#         print(f"خطا در تغییر پسورد: {str(e)}")
#         return False


# def enable_disable_user_AC(username, enable=True):
#     try:
#         user = aduser.ADUser.from_cn(username)
#         if enable:
#             user.enable()
#             print(f"کاربر {username} با موفقیت فعال شد.")

#         else:
#             user.disable()
#             print(f"کاربر {username} با موفقیت غیرفعال شد.")
#         return True
#     except Exception as e:
#         print(f"خطا در تغییر وضعیت کاربر: {str(e)}")
#         return False



# def delete_computer_AC(computer_name):
#     try:
#         # پیدا کردن کامپیوتر (نام کامپیوتر باید بدون $ باشد)
#         computer = adcomputer.ADComputer.from_cn(computer_name)       
#         computer.delete()        
#         print(f"کامپیوتر {computer_name} با موفقیت حذف شد.")
#         return True
#     except Exception as e:
#         print(f"خطا در حذف کامپیوتر: {str(e)}")
#         return False
    
#Start Bot
# def get_updates(offset=None):
#     try:
#         url = f"{BASE_URL}/getUpdates"
#         params = {"offset": offset} if offset else {}
#         response = requests.get(url, params=params, timeout=5)
#         return response.json()
#     except:
#         return {}
    
def get_updates():
    try:
        url = f"{BASE_URL}/getUpdates"
        response = requests.get(url)
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
        user_states[user_id] = ["MAIN_MENU"]

    state = user_states.get(user_id)[0]

    if text == "/start":
        send_message(chat_id, "help set:::::")
    
    elif state == "GET_USERNAME":
        user_states[user_id].append(text)
        user_states[user_id][0] = "GET_PASSWORD"
        send_message(chat_id, "Enter your password:")
    
    elif state == "GET_PASSWORD":
        if user_states[user_id][1] == "root" and text == "passwd":
            user_states[user_id][0] = "LOGGED_IN"
            user_states[user_id].remove(user_states[user_id][1])
            print(user_states)
            send_message(chat_id, "Welcome")
        else:
            user_states[user_id][0] = ["MAIN_MENU"]
            user_states[user_id].remove(user_states[user_id][1])
            send_message(chat_id, "Wrong")


    elif text == "/login":
        user_states[user_id][0] = "GET_USERNAME"
        send_message(chat_id, "Enter Username:")
    
    elif text == "/help":
        if user_states[user_id][0] == "LOGGED_IN":
            send_message(chat_id, "help set:")
        else:
            send_message(chat_id, "help set:::::")
    
    elif text == "rp":
        if user_states[user_id][0] == "LOGGED_IN":
            user_states[user_id].append('rp1')
            # print(user_states)
            send_message(chat_id, "Enter your username want to reset password:")
        else:
            send_message(chat_id, "You must log in")
    elif "rp1" in [h for h in user_states[user_id]]:
        user_states[user_id].append({'rp':[text]})
        # Number_Of_Index = find_index('rp1', user_states[user_id])
        # print(user_states[user_id], Number_Of_Index)
        user_states[user_id].remove('rp1')        
                 
        print(user_states)
        user_states[user_id].append('rp2')
        
        send_message(chat_id, "Enter new password:")

    elif "rp2" in [h for h in user_states[user_id]]:
        for i in user_states:
            if 'rp' in str(i):
               Number_Of_Index = user_states.index(i) 
        user_states[user_id].delete(user_states[user_id]['rp2'])
        user_states[user_id][Number_Of_Index].get('rp').append(text)
        print(user_states[user_id][Number_Of_Index])
        send_message(chat_id, "Enter new password:")
    

    else:
        send_message(chat_id, "help set:::::")

def main():
    while True:
        updates = get_updates()
        for update in updates.get("result", []):
            handle_message(update)
        # time.sleep(1)

if __name__ == "__main__":
    main()