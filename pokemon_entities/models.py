from django.db import models  # noqa F401


class Pokemon(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=200)