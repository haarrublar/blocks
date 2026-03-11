from javascript import require

class PathFinderManager:
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.bot = bot_instance.bot
        
        self.pathfinder_module = bot_instance.pathfinder_plugin
        self.movements = None
    
    def setup(self):
        user_data = self.bot_instance.data_plugin(self.bot.version)
        
        self.movements = self.pathfinder_module.Movements(self.bot, user_data)
        self.bot.pathfinder.setMovements(self.movements)


