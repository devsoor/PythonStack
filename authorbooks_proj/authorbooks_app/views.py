from django.shortcuts import render, redirect
from .models import Author, Book

def index(request):
    books = Book.objects.all()
    context = {
        "all_books": books,
    }
    return render(request, "index.html", context)

def create_book(request):
    book_title = request.POST["book_title"]
    book_desc = request.POST["book_desc"]
    Book.objects.create(title=book_title, desc=book_desc)
    return redirect("/")

def view_book(request, id):
    book = Book.objects.get(id=id)
    this_book_author_list = book.authors.all()
    balist = []
    balist_ids = []
    for author in this_book_author_list:
        balist.append(f"{author.first_name} {author.last_name}")
        balist_ids.append(f"{author.id}")

    authors = Author.objects.all().exclude(id__in=balist_ids)
    context = {
        "book_detail": book,
        "all_authors": authors,
        "authors_of_this_book": balist,
    }
    return render(request, "book.html", context)

def index_author(request):
    authors = Author.objects.all()
    context = {
        "all_authors": authors,
    }
    return render(request, "authors.html", context)

def create_author(request):
    author_fname = request.POST["author_fname"]
    author_lname = request.POST["author_lname"]
    author_notes = request.POST["author_notes"]
    Author.objects.create(first_name=author_fname, last_name=author_lname, notes=author_notes)
    return redirect("/authors")

def view_author(request, id):
    author = Author.objects.get(id=id)
    this_author_book_list = author.books.all()
    book_list = []
    ablist_ids = []
    for book in this_author_book_list:
        ablist_ids.append(f"{book.id}")

    books = Book.objects.all().exclude(id__in=ablist_ids)

    context = {
        "author_detail": author,
        "all_books": books,
        "books_with_this_author": this_author_book_list,
    }
    return render(request, "author_view.html", context)

def add_author_to_book(request, id):
    author_id = request.POST["author_select"]
    this_book = Book.objects.get(id=id)
    this_author = Author.objects.get(id=author_id)
    this_book.authors.add(this_author)
    url = f"/books/{id}"
    return redirect(url)


def add_book_to_author(request, id):
    book_id = request.POST["book_select"]
    this_author = Author.objects.get(id=id)
    this_book = Book.objects.get(id=book_id)
    this_author.books.add(this_book)
    return redirect("/authors", id=id)
