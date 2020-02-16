from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	      
    path('shows', views.all_shows),
    path('shows/new', views.new_show),
    path('shows/create', views.create_show),
    path('shows/<int:id>', views.view_show, name='view_show'),
    path('shows/<int:id>/edit', views.edit_show, name='edit_show'),
    path('shows/<int:id>/update', views.update_show, name='update_show'),
    path('shows/<int:id>/destroy', views.destroy_show, name='destroy_show'),
]