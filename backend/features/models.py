from djongo import models

# Create your models here.
class ConferencesCache(models.Model):
    conference_id = models.IntegerField(unique=True)
    conference_name = models.CharField(max_length=255)
    deadline = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    conference_link = models.CharField(max_length=255)
    fetch_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conferences_cache'

