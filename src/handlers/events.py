from javascript import On
import time
import threading
from src.handlers.aux_functions import get_distance

def register_events(bot_manager):
    
    bot = bot_manager.bot
    @On(bot, "login")
    def on_login(this):
        """Handle bot login event."""
        print("Bot connected")
        bot_manager.is_connected = True
        
    @On(bot, "spawn")
    def welcoming_message(this):
        welcome_msg = "I got connected! Let's start the adventure."
        bot.chat(welcome_msg)
        
    SPAWN_RADIUS = 15
    tracking_flag = {"active": False}
    inspawn_alert = {"value": None}
    @On(bot, "entitySpawn")
    def on_entity_spawn(this, entity):
        time.sleep(0.7)
        
        list_players = list(bot.players)
        if entity.type == 'player' and entity.username != bot.username and len(list_players) == 2:
            entity_name1 = str(list_players[0]).strip("'")
            entity_name2 = str(list_players[1]).strip("'")
            
            tracking_flag['active'] = False
            time.sleep(0.2)
            
            tracking_flag['active'] = True  
            def radar_loop():
                while tracking_flag['active']:
                    try:
                        distance = get_distance(
                            bot.players[entity_name1].entity.position, bot.players[entity_name2].entity.position
                        )
                        
                        if distance <= SPAWN_RADIUS:
                            bot_manager.gaze_manager.look_at_entity(entity)
                            if inspawn_alert['value'] != True:
                                print(f"{entity.username} inside the spawn zone")
                                inspawn_alert['value'] = True
                        else:
                            if inspawn_alert['value'] != False:
                                print(f"{entity.username} outside the spawn zone")
                                inspawn_alert['value'] = False
                    except Exception as e:
                        print(f"Tracking error: {e}")
                        break
                    time.sleep(0.2)
            t = threading.Thread(target=radar_loop, daemon=True)
            t.start()
            
    @On(bot, "entityGone")
    def on_entity_gone(this, entity):
        """Check if the entity (not bot) is on the server. If not stops the radar while loop"""
        if entity.type == 'player' and entity.username != bot.username:
            tracking_flag["active"] = False
            print(f"{entity.username} left, stopped tracking")
        
        
    @On(bot, 'chat')
    def handleMsg(this, sender, message, *args):
        # The following rules will apply for all written interactions in between the users and the bot. Doing so, we reduce the possible infinite loops or confusion in the system.
        # Rule 1: Only process strictly uppercase commands (The Protocol)
        # Rule 2: Identity Guard (Using extraction to avoid type mismatch)
        # Rule 3: Execution & Capitalized Reply
        # print(bot.players['haarrublar']['entity']['position'])
        if not message.isupper():
            return
            
        if str(sender) == bot.username:
            return

        if "HI" in message:
            bot.chat("hi".capitalize())
            