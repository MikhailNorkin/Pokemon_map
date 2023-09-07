from django.contrib import admin
from .models import Pokemon, PokemonEntity

admin.site.register(Pokemon)

@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lon', 'appeared_date', 'disappered_data')