from django.db import models  # noqa F401


class Pokemon(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='poks', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.CharField(max_length=10)
    lon = models.CharField(max_length=10)
    appeared_date = models.DateTimeField()
    disappered_data = models.DateTimeField()
    level = models.CharField(max_length=5)
    health = models.CharField(max_length=5)
    strength = models.CharField(max_length=5)
    defence = models.CharField(max_length=5)
    stamina = models.CharField(max_length=5)
