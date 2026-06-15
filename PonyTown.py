from tkinter.messagebox import showerror, showwarning, showinfo, askquestion
from discordrp import Presence
import subprocess
import threading
import requests
import keyboard
import webview
import time
import sys
import os

# preface to this script: i used NO ai when making this.
# just making that clear. because i'm NOT a vibe "coder".
# and if you are?
# * ...well.
# * hope that was a good experience for you.
# * ...
# * just kidding. i dont really hope that.
# * GO TO HELL.

# anyway.
# first, test if there's an internet connection:
try:
    rq = requests.get("https://pony.town/")
    if rq.status_code == 200:
        print("Internet check successful!")
    else:
        showwarning("Warning!", "https://pony.town/ can be reached, but returned a non-200 status code.\n\nPress OK to continue.")
except:
    showerror("Error", "No internet connection.\nAn internet connection is currently required to\n \
    run this client. Hopefully there will be an\n \
    offline/singleplayer mode in the future, though.")
    sys.exit(0)

# next, test if Microsoft Edge Webview2 is installed. this is needed for PyWebview.
if not os.path.isdir(r"C:\Program Files (x86)\Microsoft\EdgeWebView\Application"):
    if askquestion("Warning!", "Required software \"Microsoft Edge Webview 2\" is not installed.\n\nPress Yes to download and install the software.\nPress No to exit.") == "yes":
        res = requests.get("https://go.microsoft.com/fwlink/p/?LinkId=2124703")
        if res.status_code == 200:
            with open("MicrosoftEdgeWebview2Setup.exe", "wb") as f:
                f.write(res.content)

        subprocess.Popen("MicrosoftEdgeWebview2Setup.exe", creationflags=subprocess.DETACHED_PROCESS)
        showinfo("Info", "Please install Microsoft Edge Webview 2. When the installation is finished, re-run the Pony Town Client.")
        sys.exit(0)
    else:
        sys.exit(0)

try:
    net_versions = subprocess.check_output("powershell -c \"gci 'HKLM:\\SOFTWARE\\Microsoft\\NET Framework Setup\\NDP' -recurse | gp -name Version,Release -EA 0 | where { $_.PSChildName -match '^(?!S)\\p{L}'} | select Version")
except subprocess.CalledProcessError as e:
    net_versions = e.output.decode('utf-8')

# finally, check if the .NET Framework >4.0 is installed.
if "4." not in net_versions:
    # praying it detected correctly lmfaos
    try:
        subprocess.run("dotnet --list-runtimes")
    except:
        # ITS NOT INSTALLED
        if askquestion("Warning!", "Required software \".NET Framework >4.0\" is not installed.\n\nPress Yes to download and install the software.\nPress No to exit.") == "yes":
            res = requests.get("https://go.microsoft.com/fwlink/?LinkId=2203304")
            if res.status_code == 200:
                with open("NDP481-Web.exe", "wb") as f:
                    f.write(res.content)

            showinfo("Info", "Please install the .NET Framework. When the installation is finished, re-run the Pony Town Client.")
            os.system("NDP481-Web.exe")
            sys.exit(0)
        else:
            sys.exit(0)

ponytown_win = webview.create_window("Pony Town", "https://pony.town/", maximized=True)

# "dont put functions here its sloppy and looks bad"
# i...have no defense for this
def toggleFullscreen():
    ponytown_win.toggle_fullscreen()

def reloadPage():
    ponytown_win.load_url("about:blank")
    ponytown_win.load_url("https://pony.town")

def closeWindow():
    ponytown_win.destroy()

usedName = "?"
def richPresence():
    time.sleep(5)
    client_id = "1515536240223453274"
    startTime = int(time.time())

    with Presence(client_id) as presence:
        while len(webview.windows) > 0:
            print("Connected to Discord!")
            
            state = ""
            
            try:
                # todo: this works, but it might break in the future.
                # make it more reliable somehow...?
                tmp = ponytown_win.dom.get_elements('input')[1].value
                if tmp != None:
                    usedName = tmp
                if ponytown_win.dom.get_element(".character-tabset") != None:
                    state = f"Editing pony {usedName}"
                else:
                    state = f"Main menu (using pony {usedName})"
            except:
                state = f"In game (using pony {usedName})"
                pass

            presence.set(
                {
                    "state": state,
                    "details": "Playing on the Unofficial Pony Town Client",
                    "timestamps": {
                        "start": startTime
                    },
                    "assets": {
                        "large_image": "apple",
                        "large_text": "Pony Town logo"
                    },
                    "buttons": [
                        {
                            "label": "Pony Town",
                            "url": "https://pony.town/",
                        },
                        {
                            "label": "Pony Town Client",
                            "url": "https://github.com/dustedsylvia/PonyTown-Client/",
                        },
                    ],
                }
            )
            print("Presence updated!")

            time.sleep(1)
        print("exiting thread...")
        sys.exit(0)

keyboard.add_hotkey("f4", toggleFullscreen)
keyboard.add_hotkey("f11", toggleFullscreen)
keyboard.add_hotkey("ctrl+r", reloadPage)
keyboard.add_hotkey("f5", reloadPage)
keyboard.add_hotkey("ctrl+w", closeWindow)
keyboard.add_hotkey("ctrl+shift+w", closeWindow)

# start discord rich presence
drpUpdaterThread = threading.Thread(target=richPresence)
drpUpdaterThread.start()

# now that all the setup is done, we can start the "client"
# client in quotes because this barely does anything new lmfaos
webview.start(ponytown_win, icon="apple.ico", private_mode=False, http_server=True)