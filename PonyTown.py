from tkinter.messagebox import showerror, showwarning
import subprocess
import requests
import keyboard
import webview
import sys

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

ponytown_win = webview.create_window("Pony Town", "https://pony.town/")

# "dont put functions here its sloppy and looks bad"
# i...have no defense for this
def toggleFullscreen():
    ponytown_win.toggle_fullscreen()

def reloadPage():
    ponytown_win.load_url("about:blank")
    ponytown_win.load_url("https://pony.town")

def closeWindow():
    ponytown_win.destroy()

keyboard.add_hotkey("f4", toggleFullscreen)
keyboard.add_hotkey("f11", toggleFullscreen)
keyboard.add_hotkey("ctrl+r", reloadPage)
keyboard.add_hotkey("f5", reloadPage)
keyboard.add_hotkey("ctrl+w", closeWindow)
keyboard.add_hotkey("ctrl+shift+w", closeWindow)

# start discord rich presence
# note: i really did try NOT to use a helper program for this.
# it didn't work out so well.
try:
    subprocess.Popen("presence_helper.exe")
except:
    print("Discord Rich Presence failed to start. Oh well.")

# now that all the setup is done, we can start the "client"
# client in quotes because this barely does anything new lmfaos
webview.start(ponytown_win, icon="apple.ico", private_mode=False, http_server=True)

subprocess.run("taskkill /f /im presence_helper.exe") # End Discord Rich Presence