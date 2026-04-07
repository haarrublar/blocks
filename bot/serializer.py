from rest_framework import serializers
from .models import AgentInteraction, Player, ChatMessages


class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = [
            'id',
            'username',
            'player_type',
            'is_connected',
            'last_seen'
        ]


class AgentInteractionSerializer(serializers.ModelSerializer):
    
    player = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = Player.objects.all()
    )
    
    class Meta:
        model = AgentInteraction
        fields = [
            'id',
            'player',
            'timestamp',
            'player_id',
            'raw_prompt',
            'llm_reasoning',
            'action_payload',
            'task_type'
        ]
     
     
class ChatMessagesSerializer(serializers.ModelSerializer):
    
    player = serializers.SlugRelatedField(
        slug_field='username',
        queryset=Player.objects.all()
    )
    class Meta:
        model = ChatMessages
        fields = [
            'id',
            'player',
            'content',
            'timestamp'
        ]