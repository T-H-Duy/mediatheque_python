from django.shortcuts import render
from bibliothecaire.bibliothecaire.models import Media


def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'membres/liste_medias.html', {'medias': medias})