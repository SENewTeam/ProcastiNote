from djongo import models

# Create your models here.
class AuthorPapersCache(models.Model):
    author_id = models.CharField(max_length=50)
    papers = models.JSONField()

    class Meta:
        db_table = 'author_papers_cache'

class PaperDetailsCache(models.Model):
    paper_id = models.CharField(max_length=50)
    details = models.JSONField()

    class Meta:
        db_table = 'paper_details_cache'

class PaperReferencesCache(models.Model):
    paper_id = models.CharField(max_length=50)
    references = models.JSONField()

    class Meta:
        db_table = 'paper_references_cache'

class PaperCitationsCache(models.Model):
    paper_id = models.CharField(max_length=50)
    citations = models.JSONField()

    class Meta:
        db_table = 'paper_citations_cache'

class PaperRecommendationsCache(models.Model):
    paper_id = models.CharField(max_length=50)
    recommendations = models.JSONField()

    class Meta:
        db_table = 'paper_recommendations_cache'
