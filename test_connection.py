# # from pyad import pyad


# # pyad.set_defaults(
# #     ldap_server="192.168.1.105",  
# #     username="TEST\Administrator",           
# #     password="Mhelahi@123"

# # )


# from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE


# # اطلاعات سرور اکتیو دایرکتوری
# server_address = '192.168.1.105'  # یا hostname
# domain_name = 'test.local'
# username = 'Administrator'
# password = 'Mhelahi@123'

# # آدرس سرور
# server = Server(server_address, get_info=ALL)

# # یوزر به فرمت DOMAIN\\username
# conn = Connection(server, user=f'{domain_name}\\{username}', password=password, authentication=NTLM, auto_bind=True, )

# if conn.bound:
#     print("connected")
#     # مثلا جستجوی یوزرها
#     conn.search(search_base='DC=test,DC=local',
#                 search_filter='(objectClass=user)',
#                 attributes=['cn', 'sAMAccountName'])
#     for entry in conn.entries:
#         print(entry)
# else:
#     print("اتصال برقرار نشد!")



# user_dn = 'CN=MHE,CN=Users,DC=test,DC=local'

# new_password = '"NewPass@wor@d123!"'.encode('utf-16-le')  # طبق نیاز AD

# conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [new_password])]})
# if conn.result['description'] == 'success':
#     print("ok")
# else:
#     print("خطا در ریست پسورد:", conn.result)

# # computer_dn = 'CN=test123,CN=Computers,DC=test,DC=local'

# # conn.delete(computer_dn)
# # if conn.result['description'] == 'success':
# #     print("ok")
# # else:
# #     print("خطا در حذف کامپیوتر:", conn.result)

# # user_dn = 'CN=test1,CN=Users,DC=test,DC=local'
# # conn.search(user_dn, '(objectClass=person)', attributes=['userAccountControl'])
# # current_uac = int(conn.entries[0].userAccountControl.value)

# # print(f"Current userAccountControl: {current_uac}")
# # DISABLE_UAC = current_uac | 0x2  # بیت 2 رو ست کن
# # conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [DISABLE_UAC])]})
# # ENABLE_UAC = current_uac & ~0x2  # بیت 2 رو صفر کن
# # conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [ENABLE_UAC])]})



from ldap3 import Server, Connection, Tls, NTLM, ALL


server = Server('192.168.1.105',  get_info=ALL)
conn = Connection(server, user='TEST\\Administrator', password='Mhelahi@123', authentication=NTLM, auto_bind=True)

