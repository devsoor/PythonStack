from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),	      
    path('register', views.register),	      
    path('login', views.login),	      
    path('logout', views.logout),
    path('books', views.bookshome),
    path('books/add', views.books_add),
    path('books/addreview_book', views.addreview_book),
    path('books/<int:id>', views.view_book, name='view_book'),
    path('users/<int:id>', views.view_user, name='view_user'),
    path('review_delete/<int:id>', views.review_delete, name='review_delete'),
]