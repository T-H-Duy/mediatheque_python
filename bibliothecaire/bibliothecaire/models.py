from django.db import models
from django.utils import timezone
from datetime import timedelta


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    bloque = models.BooleanField(default=False)

    def peut_emprunter(self):

        if self.media_set.filter(dateEmprunt__isnull=False,
                                 dateEmprunt__lte=timezone.now() - timedelta(weeks=1)).exists():
            return False

        if self.media_set.filter(dateEmprunt__isnull=False).count() >= 3:
            return False
        return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Media(models.Model):
    TYPE_MEDIA = [
        ('livre', 'Livre'),
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('Jeu_de_plateau', 'Jeu de plateau'),
    ]

    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    type_media = models.CharField(max_length=20, choices=TYPE_MEDIA)
    disponible = models.BooleanField(default=True)
    dateEmprunt = models.DateTimeField(null=True, blank=True)
    emprunteur = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL)

    def est_disponible(self):
        return self.disponible and (self.type_media != 'Jeu_de_plateau') and (self.dateEmprunt is None)

    def __str__(self):
        return f"{self.name} ({self.get_type_media_display()})"