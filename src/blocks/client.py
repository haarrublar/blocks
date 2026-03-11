from javascript import require
from src.config import BOT_OPTIONS
from src.handlers.events import register_events
from src.actions.pathfinder import PathFinderManager
from src.actions.gaze import GazeManager

class MinecraftBot:
    
    def __init__(self, BOT_OPTIONS):
        self.mineflayer = require('mineflayer')
        self.pathfinder_plugin = require('mineflayer-pathfinder')
        self.data_plugin = require('minecraft-data')
        self.vec3_plugin = require('vec3')

        self.bot = self.mineflayer.createBot(BOT_OPTIONS)
        self.bot.loadPlugin(self.pathfinder_plugin.pathfinder)
        
        self.pathfinder_manager = PathFinderManager(self)
        self.gaze_manager = GazeManager(self)
        
        register_events(self)