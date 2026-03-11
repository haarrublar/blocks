import math

def get_distance(bot_location, entity_location):
    return math.sqrt(
        (bot_location['x'] - entity_location['x']) ** 2 + 
        (bot_location['y'] - entity_location['y']) ** 2 + 
        (bot_location['z'] - entity_location['z']) ** 2  
    )
    