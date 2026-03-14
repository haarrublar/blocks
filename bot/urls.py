from django.urls import path

from .views import agent_interaction_view, player_view


urlpatterns = [
    path('agent/', agent_interaction_view, name="agent"),
    path('players/', player_view, name="players"),
]
