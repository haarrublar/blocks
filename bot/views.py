import sys, os

from django.utils import timezone
from django.db import transaction

from .models import AgentInteraction, Player, ChatMessages, ChatSession
from .serializer import AgentInteractionSerializer, PlayerSerializer, ChatMessagesSerializer, ChatSessionSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def player_view(request):
    if request.method == 'GET':
        queryset = Player.objects.all()
        player = request.query_params.get('username')
        player_type = request.query_params.get('player_type')

        if player:
            queryset = queryset.filter(username=player)
        if player_type:
            queryset = queryset.filter(player_type=player_type)

        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        with transaction.atomic():
            player, created = Player.objects.update_or_create(
                username=username,
                defaults=request.data
            )
        serializer = PlayerSerializer(player)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([AllowAny])
def agent_interaction_view(request):
    if request.method == 'GET':
        tasks = AgentInteraction.objects.all()
        serializer = AgentInteractionSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = AgentInteractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PATCH':
        task_id = request.datag.get('id')
        
        try:
            task = AgentInteraction.objects.get(pk=task_id)
        except AgentInteraction.DoesNotExist:
            return Response({"error" : "Task not found"}, status=404)
        
        serializer = AgentInteractionSerializer(
            task, 
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def chat_messages_view(request):
    if request.method == 'GET':
        queryset = ChatMessages.objects.all()
        sender = request.query_params.get('sender')
        session = request.query_params.get('session')
        date_param = request.query_params.get('date')

        if sender:
            queryset = queryset.filter(sender__username=sender)
        if session:
            queryset = queryset.filter(session__id=session)
        if date_param:
            queryset = queryset.filter(timestamp__date=date_param)

        serializer = ChatMessagesSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
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
        player = request.query_params.get('player')
        if player:
            queryset = queryset.filter(player__username=player)
        serializer = ChatSessionSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        player_username = request.data.get('player')
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)

        try:
            player = Player.objects.get(username=player_username)
            
            session, created = ChatSession.objects.get_or_create(
                player=player,
                started_at__range=(today_start, today_end),
                defaults={'player': player}
            )

            serializer = ChatSessionSerializer(session)
            res_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=res_status)
            
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(["GET"])
@permission_classes([AllowAny])
def active_chat_dates_view(request):
    dates = ChatMessages.objects.dates('timestamp','day')
    return Response([d.strftime('%Y-%m-%d') for d in dates])

