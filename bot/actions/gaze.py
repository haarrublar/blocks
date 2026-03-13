from javascript import On, require

class GazeManager:
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.bot = bot_instance.bot
        self.vec3_module = bot_instance.vec3_plugin
    
    
    def look_at_entity(self, entity):
        if not entity or not entity.position:
            return
            
        pos = entity.position
        # print(pos, type(pos))
        target_location = self.vec3_module(
            pos.x, 
            pos.y + 1, 
            pos.z
        )
        # print(target_location, type(target_location))
        self.bot.lookAt(target_location, True)
