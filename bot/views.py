import sys, os

from django.shortcuts import render

from .models import AgentInteraction, Player, ChatMessages
from .serializer import AgentInteractionSerializer, PlayerSerializer, ChatMessagesSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def player_view(request):
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        username = request.data.get('username')
        instance = Player.objects.filter(username=username).first()
        serializer = PlayerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        player_name = request.query_params.get('player')
        data_param = request.query_params.get('date')
        
        if player_name:
            queryset = queryset.filter(player__username=player_name)
        if data_param:
            queryset = queryset.filter(timestamp__date=data_param)
        serializer = ChatMessagesSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ChatMessagesSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    