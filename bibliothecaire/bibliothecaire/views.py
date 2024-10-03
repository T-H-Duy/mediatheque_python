from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import CreationMember, CreationMedia, EmpruntForm
from .models import Member, Media


def home(request):
    return render(request, 'bibliothecaire/home.html')

#Views Member
def list_members_view(request):
    members = Member.objects.all()
    return render(request, 'bibliothecaire/list_members.html', {'members': members})

def add_member_view(request):
    if request.method == 'POST':
        creation_member = CreationMember(request.POST)
        if creation_member.is_valid():
            member = Member()
            member.first_name = creation_member.cleaned_data['first_name']
            member.last_name = creation_member.cleaned_data['last_name']
            member.email = creation_member.cleaned_data['email']
            member.tel = creation_member.cleaned_data['tel']
            member.save()
            return redirect('member_details', id=member.id)
    else:
        creation_member = CreationMember()
        return render(request, 'bibliothecaire/add_member.html', {'creationMember': creation_member})


def member_details_view(request, id):
    member = get_object_or_404(Member, id=id)
    return render(request, 'bibliothecaire/member_details.html', {'member': member})

def update_member_view(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = CreationMember(request.POST)
        if form.is_valid():
            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']
            member.email = form.cleaned_data['email']
            member.tel = form.cleaned_data['tel']
            member.save()
            Member.objects.all()
            return redirect('member_details', id=member.id)
    else:
        form = CreationMember(initial={
            'first_name': member.first_name,
            'last_name': member.last_name,
            'email': member.email,
            'tel': member.tel,
        })
    return render(request, 'bibliothecaire/update_member.html', {'form': form, 'member': member})

def delete_member_view(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        return redirect('list_members')
    return render(request, 'bibliothecaire/delete_member.html', {'member': member})


#Views Media
def add_media_view(request):
    if request.method == 'POST':
        form = CreationMedia(request.POST)
        if form.is_valid():
            media = Media(
                name=form.cleaned_data['name'],
                creator=form.cleaned_data['creator'],
                type_media=form.cleaned_data['type_media']
            )
            media.save()
            return redirect('bibliothecaire_home')
    else:
        form = CreationMedia()
    return render(request, 'bibliothecaire/add_media.html', {'form': form})

def list_media_view(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/list_media.html', {'medias': medias})


#Views Emprunt
def add_emprunt_view(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            media = form.cleaned_data['media']
            if media.est_disponible() and member.peut_emprunter():
                media.dateEmprunt = timezone.now()
                media.emprunteur = member
                media.disponible = False
                media.save()
                return redirect('list_media')
            else:
                if not media.est_disponible():
                    messages.error(request, "Ce média n'est pas disponible.")
                if not member.peut_emprunter():
                    messages.error(request, "Ce membre ne peut plus emprunter.")
                return redirect('error_emprunt')
    else:
        form = EmpruntForm()
        return render(request, 'bibliothecaire/add_emprunt.html', {'form': form})

def list_emprunt_view(request):
    emprunts = Media.objects.filter(disponible=False)
    emprunts_par_type = {
        type_media[1]: emprunts.filter(type_media=type_media[0])
        for type_media in Media.TYPE_MEDIA
    }
    return render(request, 'bibliothecaire/list_emprunt.html', {'emprunts_par_type': emprunts_par_type})

def return_emprunt_view(request, id):
    media = get_object_or_404(Media, id=id)
    if request.method == 'POST':
        media.disponible = True
        media.dateEmprunt = None
        media.emprunteur = None
        media.save()
        return redirect('list_emprunt')
    return render(request, 'bibliothecaire/return_emprunt.html', {'media': media})

def error_view(request):
    return render(request, 'bibliothecaire/error_emprunt.html')