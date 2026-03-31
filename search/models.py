from django.db import models
from django.db.models import JSONField
# Create your models here.

class InvertedIndex(models.Model):
    token = models.CharField(max_length=255, unique=True)
    wiki = JSONField()

    def __str__(self):
        return self.token