from pyad import aduser
from pyad import pyad
from pyad import adcomputer

# تنظیمات اتصال
pyad.set_defaults(
    ldap_server="your_domain_controller",  # مثلا: "dc01.yourdomain.com"
    username="admin_username",            # مثلا: "admin@yourdomain.com"
    password="admin_password",
    ssl=False  # در صورت نیاز به SSL=True تنظیم کنید
)

class Active_directoty():
    def reset_password(username, new_password):
        try:
            user = aduser.ADUser.from_cn(username)
            user.set_password(new_password)
            print(f"پسورد کاربر {username} با موفقیت تغییر یافت.")
            return True
        except Exception as e:
            print(f"خطا در تغییر پسورد: {str(e)}")
            return False


    def enable_disable_user(username, enable=True):
        try:
            user = aduser.ADUser.from_cn(username)
            if enable:
                user.enable()
                print(f"کاربر {username} با موفقیت فعال شد.")

            else:
                user.disable()
                print(f"کاربر {username} با موفقیت غیرفعال شد.")
            return True
        except Exception as e:
            print(f"خطا در تغییر وضعیت کاربر: {str(e)}")
            return False



    def delete_computer(computer_name):
        try:
            # پیدا کردن کامپیوتر (نام کامپیوتر باید بدون $ باشد)
            computer = adcomputer.ADComputer.from_cn(computer_name)       
            computer.delete()        
            print(f"کامپیوتر {computer_name} با موفقیت حذف شد.")
            return True
        except Exception as e:
            print(f"خطا در حذف کامپیوتر: {str(e)}")
            return False



