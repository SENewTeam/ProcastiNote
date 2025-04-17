from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import google.generativeai as palm
from dotenv import load_dotenv

from features.utils import get_conferences
from features.serializers import ConferenceSerializer

import os
from .gemini_client import GeminiHttpClient  # Import the singleton


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_rewrite(request):
    if 'text' not in request.data:
        return Response(status=400, data={"error": "text is required"})

    prompt = "Rewrite the comment clearly:\n\n" + request.data['text']
    client = GeminiHttpClient()
    result = client.send_request(prompt)

    if "error" in result:
        return Response(status=500, data={"error": result["error"]})
    try:
        return Response({"rewritten_text": result['candidates'][0]['content']['parts'][0]['text']})
    except Exception as e:
        return Response(status=500, data={"error": str(e)})
    
    
@api_view(['GET'])
def upcoming_conferences(request):
    if request.method == 'GET':
        conferences = get_conferences()
        serializer = ConferenceSerializer(conferences, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})