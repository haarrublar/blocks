import sys
import os
import threading  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from bot.mcp.mcp_bridge import start_bridge


from bot.blocks.client import MinecraftBot
from bot.config import BOT_OPTIONS

def run():
    print('Starting APP...')
    
    threading.Thread(target=start_bridge, daemon=True).start()
    bot_instance = MinecraftBot(BOT_OPTIONS)
    
    while True:
        pass
    
if __name__ == '__main__':
    run()