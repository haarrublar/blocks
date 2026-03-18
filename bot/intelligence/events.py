from javascript import On
import time
import threading
import requests
from bot.utils.aux_functions import get_distance

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
    def entity_spawn(this, entity):
        threading.Thread(
            target=_entity_spawn,
            args=(entity,),
            daemon=True
        ).start()
        
    def _entity_spawn(entity):
        time.sleep(0.5)
        
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
        
    @On(bot, 'messagestr')
    def handleMsg(this, message, messagePosition, jsonMsg, sender, *args):
        try:
        # The following rules will apply for all written interactions in between the users and the bot. Doing so, we reduce the possible infinite loops or confusion in the system.
        # Rule 1: Only process strictly uppercase commands (The Protocol)
        # Rule 2: Identity Guard (Using extraction to avoid type mismatch)
        # Rule 3: Execution & Capitalized Reply
        # print(bot.players['haarrublar']['entity']['position'])
            raw_message = message.split(">", 1)[1].strip()
            if messagePosition == "chat" and raw_message == "pos":
                print(bot.entity.position)
                # print(bot.username)
        except Exception as e:
            print(f"Error in handleMsg: {e}")
        # bot.chat("hi".capitalize())
            

        
    @On(bot, "playerLeft")
    def on_player_left(this, player):
        username = player['username']
        
        if username != bot.username:
            tracking_flag["active"] = False
            print(f"{username} disconnected, stopping radar thread.")
        else:
            print(f"Bot ({username}) is leaving the server.")

        p_type = 'B' if username == bot.username else 'H'
        
        try:
            payload = {
                "username": username,
                "is_connected": False,
                "player_type": p_type
            }
            requests.post('http://127.0.0.1:8000/bot/players/', json=payload, timeout=2)
        except Exception as e:
            print(f"Failed to report disconnect for {username}: {e}")
            
    @On(bot, "playerJoined")
    def on_player_joined(this, player):
        username = player['username']
        p_type = 'B' if username == bot.username else 'H'
        print(f"REPORT: {username} ({'Bot' if p_type == 'B' else 'Human'}) joined.")

        try:
            payload = {
                "username": username,
                "is_connected": True,
                "player_type": p_type
            }
            requests.post('http://127.0.0.1:8000/bot/players/', json=payload, timeout=2)
        except Exception as e:
            print(f"Failed to report join for {username}: {e}")
            