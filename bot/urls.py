from django.urls import path

from .views import agent_interaction_view, player_view, chat_messages_view, chat_session_view, active_chat_dates_view


urlpatterns = [
    path('agent/', agent_interaction_view, name="agent"),
    path('players/', player_view, name="players"),
    path('chat/', chat_messages_view, name="chat"),
    path('chat/sessions/', chat_session_view, name="sessions"),
    path('chat/sessions/active/', active_chat_dates_view, name="active-sessions"),
]
