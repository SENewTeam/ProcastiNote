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

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from paperInfo.utils import paperInfo
from paperInfo.models import PaperInfo
from paperInfo.specifications import (
    PaperNameSpecification,
    AuthorSpecification,
    VenueTypeSpecification,
    YearSpecification,
)


User = get_user_model()


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
def showAllPapers(request, id):
    """
    GET /api/user/<id>/papers/all
    Returns *all* papers the user has read, full metadata, sorted by access time desc.
    """
    if str(id) != str(request.user.id):
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    papersAT = user.papersAccessTime or {}
    # sort descending
    sorted_pids = sorted(
        papersAT.items(),
        key=lambda kv: kv[1],
        reverse=True
    )

    all_papers = []
    for paper_id, _ in sorted_pids:
        info = paperInfo(paper_id)
        all_papers.append({
            "paperId":   info["paperId"],
            "title":     info["title"],
            "abstract":  info["abstract"],
            "authors":   info["authors"],
            "year":      info["year"],
            "venue_type":info["venue_type"],
            "venue":     info.get("venue", ""),
            "venue_link":info.get("venue_link", ""),
        })

    return Response(all_papers, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filterPapers(request, id):
    if str(id) != str(request.user.id):
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # get all IDs the user has read
    pids = list((user.papersAccessTime or {}).keys())

    # pull comma‑lists from query params
    qp = request.query_params
    specs = []

    # helper that splits and strips, skipping empties
    def split_list(param):
        return [v.strip() for v in qp.get(param, "").split(",") if v.strip()]

    for name in split_list("paperName"):
        specs.append(PaperNameSpecification(name))
    for author in split_list("author"):
        specs.append(AuthorSpecification(author))
    for vt in split_list("venueType"):
        specs.append(VenueTypeSpecification(vt))
    for y in split_list("year"):
        try:
            specs.append(YearSpecification(int(y)))
        except ValueError:
            pass

    # combine into one OR‑Q
    if specs:
        q = specs[0].as_q()
        for s in specs[1:]:
            q = q | s.as_q()
    else:
        q = Q()  # no filtering

    # one DB fetch
    queryset = PaperInfo.objects.filter(paperId__in=pids).filter(q)

    data = [
        {
            "paperId":    p.paperId,
            "title":      p.title,
            "abstract":   p.abstract,
            "authors":    p.authors,
            "year":       p.year,
            "venue_type": p.venue_type,
            "venue":      p.venue,
            "venue_link": p.venue_link,
        }
        for p in queryset
    ]

    return Response(data, status=status.HTTP_200_OK)

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