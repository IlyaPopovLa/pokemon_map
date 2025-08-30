from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    lat = models.FloatField()  # широта
    lon = models.FloatField()  # долгота

    def __str__(self):
        return f"{self.pokemon.title} at ({self.lat}, {self.lon})"
