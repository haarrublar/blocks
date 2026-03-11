import sys
import os

# This ensures Python can find your 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.blocks.client import MinecraftBot
from src.config import BOT_OPTIONS

def run():
    print('Startin APP...')
    
    bot_instance = MinecraftBot(BOT_OPTIONS)
    
    while True:
        pass
    
if __name__ == '__main__':
    run()