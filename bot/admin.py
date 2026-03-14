from django.contrib import admin

from .models import AgentInteraction , Player

@admin.register(Player)
class AgentInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_connected', 'last_seen') 
    list_filter = ('username',)
    search_fields = ('is_connected',)
    
    
@admin.register(AgentInteraction)
class AgentInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_id', 'timestamp', 'task_type') 
    list_filter = ('player_id', 'timestamp')
    search_fields = ('player_id', 'prompt', 'task_type')
    