from pyad import pyad


pyad.set_defaults(
    ldap_server="your_domain_controller",  
    username="admin_username",           
    password="admin_password",
    ssl=False  
)
