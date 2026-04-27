import sys, os

from django.utils import timezone
from django.db import transaction

from .models import AgentInteraction, Player, ChatMessages, ChatSession
from .serializer import (
    AgentInteractionSerializer,
    PlayerSerializer,
    ChatMessagesSerializer,
    ChatSessionSerializer,
)
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def player_view(request):
    if request.method == "GET":
        queryset = Player.objects.all()
        player = request.query_params.get("username")
        player_type = request.query_params.get("player_type")

        if player:
            queryset = queryset.filter(username=player)
        if player_type:
            queryset = queryset.filter(player_type=player_type)

        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        username = request.data.get("username")
        with transaction.atomic():
            player, created = Player.objects.update_or_create(
                username=username, defaults=request.data
            )
        serializer = PlayerSerializer(player)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


@api_view(["GET", "POST", "PATCH"])
@permission_classes([AllowAny])
def agent_interaction_view(request):
    if request.method == "GET":
        tasks = AgentInteraction.objects.all()
        serializer = AgentInteractionSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AgentInteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        task_id = request.data.get("id")

        try:
            task = AgentInteraction.objects.get(pk=task_id)
        except AgentInteraction.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        serializer = AgentInteractionSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def chat_messages_view(request):
    if request.method == "GET":
        queryset = ChatMessages.objects.all()
        sender = request.query_params.get("sender")
        session = request.query_params.get("session")
        date_param = request.query_params.get("date")

        if sender:
            queryset = queryset.filter(sender__username=sender)
        if session:
            queryset = queryset.filter(session__id=session)
        if date_param:
            queryset = queryset.filter(timestamp__date=date_param)

        serializer = ChatMessagesSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ChatMessagesSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def chat_session_view(request):
    if request.method == 'GET':
        queryset = ChatSession.objects.all()
        participant_name = request.query_params.get('participants')
        if participant_name:
            queryset = queryset.filter(participants__username=participant_name)
        serializer = ChatSessionSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        usernames = request.data.get('participants', [])
        
        today_date = timezone.now().date()

        try:
            players = [Player.objects.get(username=u) for u in usernames]

            session, created = ChatSession.objects.get_or_create(
                date=today_date,
                defaults={'started_at': today_date}
            )

            if created:
                session.participants.set(players)

            serializer = ChatSessionSerializer(session)
            res_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=res_status)

        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=404)

