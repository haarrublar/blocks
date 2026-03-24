from django.urls import path

from .views import agent_interaction_view, player_view, process_ai_build


urlpatterns = [
    path('agent/', agent_interaction_view, name="agent"),
    path('players/', player_view, name="players"),
    path('process-ai/', process_ai_build, name="process_ai"),
]
