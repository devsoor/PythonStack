from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	      
    path('register', views.register),	      
    path('register_user', views.register_user),	      
    path('login', views.login),	      
    path('signin', views.signin),	      
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('trips/<int:id>', views.view_trip),
    path('trips/new', views.new_trip),
    path('trips/create', views.create_trip),
    path('trips/edit/<int:id>', views.edit_trip),
    path('trips/edit_form/<int:id>', views.edit_form),
    path('trips/remove/<int:id>', views.remove_trip),
    path('trips/join/<int:id>', views.join_trip),
]