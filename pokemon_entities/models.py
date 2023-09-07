from django.db import models  # noqa F401


class Pokemon(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='poks', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'