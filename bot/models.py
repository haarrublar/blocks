from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
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
    llm_reasoning = models.TextField(help_text="General LLM answer from the building instructions")
    action_playload = models.TextField(help_text="Specific Minecraft commands to build based on the responses from general instructions")
    task_type = models.CharField(max_length=20, default="building")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = 'Agent Task'
            verbose_name_plural = 'Agent Tasks'
            ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user_id} | {self.task_type} | {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    