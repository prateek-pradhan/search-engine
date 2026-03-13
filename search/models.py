from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class InvertedIndex(models.Model):
    token = models.CharField(max_length=255, unique=True)
    wiki = ArrayField(models.IntegerField(), blank=True, default=list)

    def __str__(self):
        return self.token