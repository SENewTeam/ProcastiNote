from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
import requests

from search.models import History
from search.serializers import HistorySerializer

@api_view(['GET'])
def completions(request: Request) -> Response:
    if request.method == 'GET':
        if 'query' in request.query_params:
            query = request.query_params['query']
            url = f'https://api.semanticscholar.org/graph/v1/paper/autocomplete?query={query}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return JsonResponse(response.json(), safe=False)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'query is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})


@api_view(['GET'])
def details(request: Request) -> Response:
    if request.method == 'GET':
        if 'id' in request.query_params:
            paper_id = request.query_params['id']
            url = f'https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=url,abstract,title,year,authors'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                history_entry = History.objects.create(details=response.json())
                history_entry.save()
                return Response(status=status.HTTP_200_OK, data=response.json())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'id is required'})
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})

@api_view(['GET'])
def history(request: Request) -> Response:
    if request.method == 'GET':
        history_entries = History.objects.all()
        serializer = HistorySerializer(history_entries, many=True)
        return JsonResponse(serializer.data, safe=False)
    return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'only GET method is supported'})