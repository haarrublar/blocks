import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from bot.blocks.client import MinecraftBot
from bot.config import BOT_OPTIONS

def run():
    print('Starting APP...')
    bot_instance = MinecraftBot(BOT_OPTIONS)
    
#     while True:
#         pass
    
# if __name__ == '__main__':
#     run()