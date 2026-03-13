from javascript import On
import time




def register_builder(bot_manager):
    
    bot = bot_manager.bot
    
    @On(bot, "messagestr")
    def activate_ui(this, message, messagePosition, jsonMsg, sender, verified=None):
        start = time.time()
        if messagePosition == "chat":
            print("discovered")
        end = time.time()
        print(end-start)