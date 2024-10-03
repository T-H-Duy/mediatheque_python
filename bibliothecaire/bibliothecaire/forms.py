from django import forms
from .models import Media
from .models import Member

class CreationMember(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    tel = forms.FloatField(required=True)

class CreationMedia(forms.Form):
    name = forms.CharField(label='Nom', max_length=100)
    creator = forms.CharField(label='Créé par', max_length=100)
    type_media = forms.ChoiceField(label='Type de Média', choices=Media.TYPE_MEDIA)


class EmpruntForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.objects.all(), label="Membre")
    media = forms.ModelChoiceField(queryset=Media.objects.filter(disponible=True, type_media__in=['livre', 'CD', 'DVD']), label="Média")