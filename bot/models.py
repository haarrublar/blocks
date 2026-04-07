from django.db import models
import uuid

class Player(models.Model):
    PLAYER_TYPE = {
        "B": "Bot",
        "H": "Human"
    }
    username = models.CharField(max_length=100, unique=True)
    player_type = models.CharField(
        max_length=1, 
        choices=PLAYER_TYPE,
        null=True, 
        blank=True
    )
    is_connected = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
            status = "Online" if self.is_connected else "Offline"
            return f"{self.username} ({status})"

class AgentInteraction(models.Model):
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name='interactions',
        null=True, 
        blank=True
    )
    raw_prompt = models.TextField()
    llm_reasoning = models.TextField(
        null=True, 
        blank=True,
        help_text="General LLM answer from the building instructions"
    )
    action_payload = models.TextField(
        null=True, 
        blank=True,
        help_text="Specific Minecraft commands to build based on the responses from general instructions"
    )
    task_type = models.CharField(max_length=20, default="building")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = 'Agent Task'
            verbose_name_plural = 'Agent Tasks'
            ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user_id} | {self.task_type} | {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    
class ChatSession(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    ) 
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name='sessions',
    )
    started_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = 'Chat Session'
            verbose_name_plural = 'Chat Sessions'
            ordering = ['started_at']
            
    def __str__(self):
        return f"{self.session_id} ({self.player})"

    
class ChatMessages(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name='messages',
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = 'Chat Message'
            verbose_name_plural = 'Chat Messages'
            ordering = ['timestamp']
        
    def __str__(self):
        name = self.sender.username if self.sender else "System/Unknown"
        return f"{name}: {self.content[:20]}"
    
    
    
    
    