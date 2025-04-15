import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model
from .serializers import *
from paperInfo.utils import paperInfo
from comments.utils import commentInfo
from datetime import datetime


@api_view(['POST'])
def user_creation(request):
    data = request.data
    if not data.get('username') or not data.get('password') or not data.get('email') :
        return Response({"message": "Please provide all the details"}, status=status.HTTP_400_BAD_REQUEST)
    userExist = User.objects.filter(username=data.get('username'))

    if userExist:
        return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else :
        get_user_model().objects.create_user(username=data.get('username'), password=data.get('password'), email=data.get('email'), profile=data.get('profile'))
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addPaper(request, id, paper_id):
    if id != request.user.id:
        return Response({"error": "You are not allowed to add paper to this account"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
    papers = user.papers.split(',') if user.papers else []

    paper_id_str = str(paper_id)
    paper_Info = paperInfo(paper_id_str)
    print(paper_Info)
    if "error" in paper_Info:
        return Response({"error": f"Paper Id : {paper_id} is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    print(paper_Info)
    commentInf = commentInfo(paper_id_str, user.username)
    if commentInf and commentInf[0].get('error') is None:
        paper_Info["comment"] = commentInf[0]["text"]
        paper_Info['comment_id'] = commentInf[0]["_id"]
        paper_Info["keywords"] = commentInf[0]["keyword"]

    
    if paper_id not in papers:
        papers.append(paper_id_str)
        user.papers = ','.join(papers)
    if user.papersAccessTime is None:
        user.papersAccessTime = {}
    user.papersAccessTime[paper_id_str] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.save()
    return Response(status=status.HTTP_200_OK, data=paper_Info)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showPapers(request, id):
    # print("----------",len(str(id)))
    # print("----------",len(str(request.user.id)))

    if str(id) != str(request.user.id):
        return Response({"error": "You are not allowed to add paper to this account"}, status=status.HTTP_400_BAD_REQUEST)
    # print("----------",id)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    papersAT = user.papersAccessTime
    last_5_access_times =  dict(sorted(papersAT.items(), key=lambda item: item[1], reverse=True)[:5]) if papersAT else {}
    print(last_5_access_times)
    listOfPaper = {}

    for paper in last_5_access_times.keys():
        paper_Info = paperInfo(paper)
        listOfPaper[paper] = [paper_Info["title"], paper_Info["abstract"]]
    if listOfPaper :
        return Response(listOfPaper, status=status.HTTP_200_OK)
    else :
        return Response({"message": f"Papers : "}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response(status=status.HTTP_200_OK, data={
        'username': user.username,
        'email': user.email,
        'profile': user.profile,
        'id': user.id,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    user = request.user
    papers = user.papers.split(',') if user.papers else []
    if not papers:
        return Response(status=status.HTTP_200_OK, data=[])
    url = 'https://api.semanticscholar.org/recommendations/v1/papers/?fields=abstract,title&limit=5'
    request = {
        'positivePaperIds': papers,
    }
    response = requests.post(url, json=request, timeout=5)
    if response.status_code == 200:
        return Response(status=status.HTTP_200_OK, data=response.json()['recommendedPapers'])
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': 'Internal server error'})