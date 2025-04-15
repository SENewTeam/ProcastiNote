from django.db import models
from djongo import models
from paperInfo.models import PaperInfo
from user.models import User
# Create your models here.


class CommentsCache(models.Model):
    paper_id = models.CharField(max_length=255)
    _id = models.ObjectIdField(primary_key=True) 
    user = models.CharField(max_length=255)
    text = models.TextField()
    keyword=models.CharField(max_length=255)
    paperTitle = models.CharField(max_length=255)
    

    class Meta:
        db_table = 'comment_paper_db'