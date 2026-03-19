import requests
from bot.config import BOT_OPTIONS

class MinecraftBot:
    def __init__(self, BOT_OPTIONS):
        self.host = "http://localhost:3000"
        self.bot_options = BOT_OPTIONS
        self.is_connected = False

    def start_bot(self):
            try:
                print("Requesting JS to start Minecraft bot...")
                requests.post(f"{self.host}/start", json=self.bot_options)
                self.is_connected = True
            except Exception as e:
                print(f"Could not connect to JS Engine: {e}")
                
    def check_connection(self):
            try:
                response = requests.get(f"{self.host}/status", timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    if not data.get('bot_online'):
                        print("JS Engine lost the bot (Restart detected). Re-initializing...")
                        self.start_bot()
            except requests.exceptions.ConnectionError:
                print("JS Engine is currently restarting (Nodemon)...")
        
