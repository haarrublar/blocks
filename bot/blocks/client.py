from javascript import require
from bot.config import BOT_OPTIONS
from bot.intelligence.events import register_events
from bot.intelligence.buildoperator import register_builder
from bot.behaviors.pathfinder import PathFinderManager
from bot.behaviors.gaze import GazeManager

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
        register_builder(self)