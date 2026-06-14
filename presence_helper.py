from discordrp import Presence
import time

client_id = "1515536240223453274"

with Presence(client_id) as presence:
    print("Connected to Discord!")
    presence.set(
        {
            "details": "Playing on the Unofficial Pony Town Client",
            "timestamps": {
                "start": int(time.time())
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
    print("Presence set.")

    while True:
        time.sleep(3)