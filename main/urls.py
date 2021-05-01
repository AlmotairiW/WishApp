from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process_user', views.process_user),
    path('wishes', views.wishes),
    path('wishes/new', views.Add_wish),
    path('create', views.create_wish),
    path('grant/<int:id>', views.grant_wish),
    path('like/<int:id>', views.like_wish),
    path('wishes/edit/<int:id>', views.edit_wish),
    path('update_wish/<int:id>', views.update_wish),
    path('destroy/<int:id>', views.delete_wish),
    path('wishes/stats', views.stats),
    path('logout', views.logout),
]