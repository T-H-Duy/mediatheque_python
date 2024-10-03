from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bibliothecaire_home'),
    path('member/list', views.list_members_view, name='list_members'),
    path('member/add_member', views.add_member_view, name='add_member'),
    path('member/<int:id>', views.member_details_view, name='member_details'),
    path('member/<int:id>/update_member', views.update_member_view, name='update_member'),
    path('member/<int:id>/delete', views.delete_member_view, name='delete_member'),
    path('media/add_media', views.add_media_view, name='add_media'),
    path('media/list_media', views.list_media_view, name='list_media'),
    path('emprunt/add_emprunt', views.add_emprunt_view, name='add_emprunt'),
    path('emprunt/list_emprunt', views.list_emprunt_view, name='list_emprunt'),
    path('media/<int:id>/return/', views.return_emprunt_view, name='return_emprunt'),
    path('emprunt/error', views.error_view, name='error_emprunt'),

    ]