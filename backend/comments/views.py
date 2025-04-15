from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from bson import ObjectId
from rest_framework.permissions import IsAuthenticated

from comments.models import CommentsCache
from paperInfo.models import PaperInfo

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request):
    if request.method == 'POST':
          #  print("18")
            paper_id = request.data.get('paper_id')
            paper_info = PaperInfo.objects.get(paperId=paper_id)
            comments = CommentsCache.objects.filter(paper_id=paper_id,user=request.user.username).values('_id', 'user', 'text','keyword')
            
            if comments and comments.text:
                return Response({'error': f'Comment Already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            if paper_info:
             user=request.data.get('user')
             text=request.data.get('text')
             keyword=request.data.get('keyword')
             print("30")
             #print(keyword)
             comment = CommentsCache(
                paper_id=paper_id,
             user=user,
             text=text,
             keyword=keyword,
              paperTitle=paper_info
        )  
              
             comment.save()
            else:
                return Response({'error': f'PaperInfo with paper_id {paper_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Create and save the Comment object directly
            

            return Response({'success': 'Comment created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Only POST method is supported'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_all_paper(request):
     if request.method == 'POST':
       try:
        print(request.body)
        username=request.data.get('user')
        comments = CommentsCache.objects.filter(user=username).values('_id', 'paper_id', 'text','paperTitle', 'keyword')
        for c in range(len(comments)):
            comments[c]['_id']=str(comments[c]['_id'])
        return Response(comments, status=status.HTTP_200_OK)
       except CommentsCache.DoesNotExist:
           return Response({'error': f'User with username {username} does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_comments_for_paper(request, paper_id):
    if request.method == 'GET':
       try:
        print(request.body)
        username=request.data.get('user')
        pid=paper_id
       
        #print(pid)
        paper_info = get_object_or_404(PaperInfo, paperId=pid)
       # print(paper_info)
        comments = CommentsCache.objects.filter(paper_id=pid,user=username).values('_id', 'user', 'text','keyword')  # Add other fields as needed
       # comments.queryset
        
        for c in range(len(comments)):
            comments[c]['_id']=str(comments[c]['_id'])
        #print(comments)
        return Response(comments, status=status.HTTP_200_OK)
       except CommentsCache.DoesNotExist:
           return Response({'error': f'User with username {username} does not exist'}, status=status.HTTP_404_NOT_FOUND)
       except PaperInfo.DoesNotExist:
        return Response({'error': f'PaperInfo with paper_id {paper_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
       # return Response(status=status.HTTP_200_OK)
    return Response({'error': 'Only GET method is supported'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_comment(request,comment_id):
    if request.method == 'PUT':
        try:
            print(request.body)
            username=request.data.get('user')
            print(username)
            text=request.data.get('text')
            keyword=request.data.get('keyword')
            CommentsCache.objects.filter(_id=ObjectId(comment_id),user=username).update(text=text,keyword=keyword)
           
        except CommentsCache.DoesNotExist:
            return Response({'error': f'Comment with comment_id {comment_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Update the comment with the provided data
        
       

        return Response({'success': 'Comment updated successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Only PUT method is supported'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        
        try:
            print(request.body)
            username=request.data.get('user')
            print(username)
            comment = CommentsCache.objects.filter(_id=ObjectId(comment_id),user=username)
            if comment:
                print(comment)
                comment.delete()
        except CommentsCache.DoesNotExist:
            return Response({'error': f'Comment with comment_id {comment_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
        return Response({'success': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Only DELETE method is supported'}, status=status.HTTP_400_BAD_REQUEST)