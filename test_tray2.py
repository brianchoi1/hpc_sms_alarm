from pystray import MenuItem, Menu
import pystray
from PIL import Image

def on_monitor(icon, item):
    global state,logintext
    state = not item.checked
    url = 'www.example.com'
    print("Waiting for login to complete")
    logintext = "Logout"
    print("Logged In",icon.update_menu())

logintext = "Login"
icon = pystray.Icon('Sample',title="Icons",menu=Menu(MenuItem(lambda text: logintext,on_monitor)))
icon.run()

