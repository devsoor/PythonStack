from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	      
    path('book', views.create_book),
    path('books/<int:id>', views.view_book, name='view_book'),
    path('authors', views.index_author),
    path('add_author', views.create_author),
    path('authors/<int:id>', views.view_author, name='view_author'),
    path('books/<int:id>/add_author_to_book', views.add_author_to_book, name='add_author_to_book'),
    path('authors/<int:id>/add_book_to_author', views.add_book_to_author, name='add_book_to_author'),
]