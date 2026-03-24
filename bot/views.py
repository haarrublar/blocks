import sys, os
from datetime import datetime
from django.shortcuts import render

from .models import AgentInteraction, Player
from .serializer import AgentInteractionSerializer, PlayerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from .utils.build_api import ask_claude_build, load_all_sessions, save_all_sessions

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

@api_view(['POST'])
@permission_classes([AllowAny])
def process_ai_build(request):
    task_id = request.data.get('task_id')
    player_coordinates = request.data.get('player_coordinates')
    task_description = request.data.get('task_description')
    
    try:
        interaction = AgentInteraction.objects.get(pk=task_id)
        
        all_sessions = load_all_sessions()
        ids = [int(k) for k in all_sessions.keys()]
        current_max = max(ids) if ids else 0
            
        if "reset" is task_description or current_max == 0:
            session_id = str(current_max + 1)
            all_sessions[session_id] = {
                "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "history" : []
            }
        else:
            session_id = str(current_max)
        
        ai_data = ask_claude_build(
            player_coordinates, 
            task_description, 
            session_id, 
            all_sessions)
        interaction.llm_reasoning = ai_data['llm_reasoning']
        interaction.action_payload = ai_data['action_payload']
        interaction.save()
        
        return Response({
            "status" : "success",
            "commands" : ai_data['action_payload']
        })
    except AgentInteraction.DoesNotExist:
        return Response({
            "error": "Task ID not found"
        }, status=404)

