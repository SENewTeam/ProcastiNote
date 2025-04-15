from django.db import models

# Create your models here.
class History(models.Model):
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
