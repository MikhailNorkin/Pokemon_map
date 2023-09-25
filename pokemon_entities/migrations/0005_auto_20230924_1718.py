# Generated by Django 3.1.14 on 2023-09-24 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20230924_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappered_data',
            field=models.DateTimeField(verbose_name='дата исчезновения'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='level',
            field=models.PositiveSmallIntegerField(verbose_name='уровень'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemons', to='pokemon_entities.pokemon', verbose_name='покемон'),
        ),
    ]