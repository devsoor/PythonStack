from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timezone, timedelta
import pytz
import pprint
from django.db.models import Q


def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=request.POST['email'], pw_hash=pw_hash)
        request.session["first_name"] = first_name
        request.session['user_email'] = email
        return redirect("/books")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(password.encode(), logged_user.pw_hash.encode()):
                request.session['user_email'] = logged_user.email
                request.session["first_name"] = logged_user.first_name
                return redirect("/books")

        messages.error(request, "Password does not match")
        return redirect("/")

def logout(request):
    try:
        del request.session['first_name']
        del request.session['user_email']
        # or we could do a request.session.flush() as well
    except KeyError:
        pass
    return redirect("/")

def bookshome(request):
    review_list = []
    books_with_reviews_list = []
    reviews = Review.objects.all().order_by("-created_at")
    for i in range(3):
        review_list.append(reviews[i])

    all_books = Book.objects.all()
    for book in all_books:
        if book.review != None:
            books_with_reviews_list.append(book)

    context = {
        "first_name":request.session["first_name"],
        "latest_three_reviews": review_list,
        "books_with_reviews_list": books_with_reviews_list,
    }
    return render(request, "books.html", context)

def books_add(request):
    author_list = Author.objects.all()
    return render(request, "books_add.html", {"author_list":author_list})

def addreview_book(request):
    title = request.POST["title"]
    new_author = request.POST["new_author"]
    book_review = request.POST["review"]
    rating = request.POST["rating"]

    if len(new_author):
        author_full_name = new_author.split()
        fname = author_full_name[0]
        lname = author_full_name[1]
        author_list = Author.objects.filter(Q(first_name=fname) & Q(last_name=lname))

        if len(author_list) == 0:
            this_author = Author.objects.create(first_name=fname, last_name=lname)
        else:
            this_author = Author.objects.get(id=author_list[0].id)
        
    else:
        author_id = request.POST["author_select"]
        this_author = Author.objects.get(id=author_id)

    this_user = User.objects.get(email=request.session['user_email'])
    this_book = Book.objects.filter(title__exact=title)
    if len(this_book) == 0:
        this_book = Book.objects.create(title=title, author=this_author, user=this_user)

    review = Review.objects.create(rating=rating, content=book_review, book=this_book, user=this_user)
    request.session['current_book_id'] = this_book.id

    url = f"/books/{this_book.id}"
    return redirect(url)

def view_book(request, id):
    this_book = Book.objects.get(id=id)
    request.session['current_book_id'] = this_book.id
    all_reviews = Review.objects.filter(book=this_book).order_by("-created_at")
    this_user = User.objects.get(email=request.session['user_email'])

    context = {
        "book": this_book,
        "all_reviews": all_reviews,
        "user": this_user
    }
    return render(request, "book_view.html", context)

def view_user(request, id):
    new_review = request.POST["new_review"]
    new_rating = request.POST["rating"]
    this_book = Book.objects.get(id=id)
    this_user = User.objects.get(email=request.session['user_email'])
    
    review = Review.objects.create(rating=new_rating, content=new_review, book=this_book, user=this_user)
    all_reviews = Review.objects.filter(user=this_user)
    book_list = []
    for review in all_reviews:
        book_list.append(review.book)
    number_of_reviews = len(all_reviews)

    context = {
        "book": this_book,
        "user": this_user,
        "number_of_reviews": number_of_reviews,
        "books_reviewed": book_list,
    }
    return render(request, "user_view.html", context)

def review_delete(request, id):
    book_id = request.session['current_book_id']
    this_review = Review.objects.get(id=id)
    this_review.delete()
    url = f"/books/{book_id}"
    return redirect(url)
