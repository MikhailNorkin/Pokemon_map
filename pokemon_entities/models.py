from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    description = models.TextField(verbose_name="описание:")
    title_ru = models.CharField(max_length=200, verbose_name="на русском:")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="на английском:")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="на японском:")
    photo = models.ImageField(upload_to='poks', verbose_name="фото:", null=True, blank=True)
    previous_evolution = models.ForeignKey("self", verbose_name="из кого родился", on_delete=models.CASCADE, related_name='next_evolutions', null=True, blank=True)
    def __str__(self):
        return self.title_ru
    

class PokemonEntity(models.Model):
    """Свойства покемона"""
    pokemon = models.ForeignKey(Pokemon,  verbose_name="покемон", on_delete=models.CASCADE, related_name='pokemon')
    lat = models.DecimalField(max_digits=10, decimal_places=7, verbose_name="широта")
    lon = models.DecimalField(max_digits=10, decimal_places=7, verbose_name="долгота")
    appeared_date = models.DateTimeField(verbose_name="дата появления")
    disappered_data = models.DateTimeField(verbose_name="дата исчезновения")
    level = models.PositiveSmallIntegerField(verbose_name="уровень")
    health = models.PositiveSmallIntegerField(verbose_name="здоровье")
    strength = models.PositiveSmallIntegerField(verbose_name="сила")
    defence = models.PositiveSmallIntegerField(verbose_name="защита")
    stamina = models.PositiveSmallIntegerField(verbose_name="стамина")
    def __str__(self):
        return f'Дата появления: {self.appeared_date}, дата исчезновения: {self.disappered_data}, широта: {self.lat}, долгота: {self.lon}'