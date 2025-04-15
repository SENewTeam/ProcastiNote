from comments.models import CommentsCache
def commentInfo(paper_id, username):
    try:
        pid=paper_id
        # paper_info = get_object_or_404(PaperInfo, paperId=pid)
        comments = CommentsCache.objects.filter(paper_id=pid,user=username).values('_id', 'user', 'text','keyword')
        print(comments)
        for c in range(len(comments)):
            comments[c]['_id']=str(comments[c]['_id'])
        return comments
    except CommentsCache.DoesNotExist:
           return {'error': f'User with username {username} does not exist'}
