from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(max_length=200, verbose_name="Название на английском", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Название на японском", blank=True)
    image = models.ImageField(upload_to='pokemons', verbose_name="Изображение", null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name="Из кого эволюционировал"
    )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE, related_name='entities', null=True,
                                verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Время появления")
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Время исчезновения")

    Level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    Health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    Strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    Defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    Stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon.title} at ({self.lat}, {self.lon})"