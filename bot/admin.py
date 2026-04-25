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
    list_display = ('id', 'display_participants', 'started_at') 
    list_filter = ('participants__username', 'started_at')
    search_fields = ('participants__username',)
    def display_participants(self, obj):
        return ", ".join([player.username for player in obj.participants.all()])
    
    display_participants.short_description = 'Participants'
    
@admin.register(ChatMessages)
class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'content', 'timestamp') 
    list_filter = ('session', 'sender')
    search_fields = ('sender',)
    