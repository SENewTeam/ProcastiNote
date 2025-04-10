from django.db import models

class PaperInfo(models.Model):
    paperId = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.CharField(max_length=255, default="")
    paperPdf = models.CharField(max_length=255, default="")
    year = models.PositiveIntegerField()
    authors = models.CharField(max_length=1022)
    venue = models.CharField(max_length=255, default="")
    venue_type = models.CharField(max_length=50, choices=[('conference', 'Conference'), ('journal', 'Journal')])
    venue_link = models.URLField(default="")

    def __str__(self):
        return self.title
    
    @classmethod
    def get_paper_by_id(cls, paper_id):
        try:
            paper_info = cls.objects.get(paperId=paper_id)
            return paper_info
        except cls.DoesNotExist:
            return None