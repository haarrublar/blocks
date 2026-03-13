from javascript import On
import time
import threading
import requests




def register_builder(bot_manager):
    
    bot = bot_manager.bot
    
    @On(bot, "messagestr")
    def activate_ui(this, message, messagePosition, jsonMsg, sender, verified=None):
        threading.Thread(
            target=_activate_ui, 
            args=(message, messagePosition),
            daemon=True
        ).start()
        
    def _activate_ui(message, messagePosition):
        start = time.time()
        try:
            raw_message = message.split(">", 1)[1].strip()
            if messagePosition == "chat" and raw_message == "BUILD":
                payload = {"state": "active", "label": "Active"}
                try:
                    requests.post('http://127.0.0.1:8000/update-state', json=payload)
                except Exception as e:
                    print(f"API unreachable {e}")
            end = time.time()
            print(end-start)
        except IndexError:
            pass
        