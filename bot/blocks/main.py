import sys
import os
import time
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from bot.blocks.client import MinecraftBot
from bot.config import BOT_OPTIONS

def run():
    print('Starting APP...')
    bot_instance = MinecraftBot(BOT_OPTIONS)
    while True:
        try:
            bot_instance.check_connection()
        except:
            pass
            
        time.sleep(5) 
        
        
if __name__ == '__main__':
    run()