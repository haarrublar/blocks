from django.apps import AppConfig
import os
import threading

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from .models import Player
        Player.objects.all().update(is_connected=False)
        print("DEBUG: All players reset to offline.")

        try:
            from bot.blocks.main import run
            print("DEBUG: Starting the bot thread now...")
            threading.Thread(target=run, daemon=True).start()
        except ImportError as e:
            print(f"DEBUG: Failed to import bot.blocks.main: {e}")