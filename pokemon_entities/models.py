from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(max_length=200, verbose_name="Название на англ.")
    title_jp = models.CharField(max_length=200, verbose_name="Название на яп.")
    image = models.ImageField(upload_to='pokemons', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=False, null=False)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions'
    )

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE, related_name='entities', null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    Level = models.IntegerField(null=True, blank=True)
    Health = models.IntegerField(null=True, blank=True)
    Strength = models.IntegerField(null=True, blank=True)
    Defence = models.IntegerField(null=True, blank=True)
    Stamina = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.pokemon.title} at ({self.lat}, {self.lon})"