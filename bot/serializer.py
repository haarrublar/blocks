from rest_framework import serializers
from .models import AgentInteraction, Player


class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = [
            'username',
            'player_type',
            'is_connected',
            'last_seen'
        ]


class AgentInteractionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AgentInteraction
        fields = [
            'timestamp',
            'player_id',
            'raw_prompt',
            'llm_reasoning',
            'action_playload',
            'task_type'
        ]
     