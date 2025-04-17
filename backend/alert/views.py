from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from comments.models import CommentsCache
from paperInfo.models import PaperInfo

@api_view(['POST'])
def alert_api(request):
    print(request.body)
    current_keyword = request.data.get('keyword').split(',')

    user=request.data.get('user')
    print("Current keyword",current_keyword)
    # Retrieve comments from the entire database
    all_keywords = CommentsCache.objects.filter(user=user)
    #print(all_keywords.query)
    # Create a list to store papers with matching keywords
    matching_papers = []
    for key in all_keywords:
        print('key.keyword', key.keyword)
        comment_keyword=key.keyword.split(',')
        print("Database keyword",comment_keyword)
        matched_keywords=list(set(current_keyword).intersection(set(comment_keyword)))
        #print(matched_keywords)
       # print(key.paperTitle)
        if(len(matched_keywords)>=3):
           # print("Inside")
            title=key.paperTitle
           # print(title)
            if key.paper_id != request.data.get('paperId'):
                matching_papers.append(title)
            #print({paper_info})
    #print(matching_papers) 
     
    if matching_papers:
        print(matching_papers) 
        return Response(matching_papers,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

