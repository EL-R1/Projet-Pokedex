from django.db import models

class TeamPokemon(models.Model):
    Pokid1 = models.IntegerField(max_length=50)
    Pokid2 = models.IntegerField(max_length=50)
    Pokid3 = models.IntegerField(max_length=50)
    Pokid4 = models.IntegerField(max_length=50)
    Pokid5 = models.IntegerField(max_length=50)
    Pokid6 = models.IntegerField(max_length=50)

    def __str__(self):
        return self.Pokid1