from django.contrib import admin

from .models import AgentInteraction , Player, ChatMessages, ChatSession

@admin.register(Player)
class AgentInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'player_type', 'is_connected', 'last_seen') 
    list_filter = ('username','player_type')
    search_fields = ('is_connected',)
    
    
@admin.register(AgentInteraction)
class AgentInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_id', 'timestamp', 'task_type') 
    list_filter = ('player_id', 'timestamp')
    search_fields = ('player_id', 'prompt', 'task_type')
    
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'started_at') 
    list_filter = ('player', 'started_at')
    search_fields = ('player',)
    
@admin.register(ChatMessages)
class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'content', 'timestamp') 
    list_filter = ('session', 'sender')
    search_fields = ('sender',)
    