from django.db import models
class MarkdownContent(models.Model):
    title = models.CharField(max_length=200)
