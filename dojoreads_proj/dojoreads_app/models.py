from django.db import models
import re
import bcrypt
from datetime import date, datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        if not postData:
            return
        errors = {}

        NAME_REGEX = re.compile ('[a-zA-Z0-9_]')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be atleast 2 characters long" 

        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "First name must be all letters"


        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be atleast 2 characters long "       
        if not NAME_REGEX.match(postData['last_name']):
            errors["first_name"] = "Last name must be all letters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) == 0:           
            errors['email'] = "Invalid email address!"

        # regular email uniqueness check
        if User.objects.filter(email=postData['email']).exists():
            errors['usertaken'] = "This user email already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters long"

        if len(postData['confirm_pw']) < 8:
            errors['confirm_pw'] = "Confirm Password must be atleast 8 characters long"

        if postData['password'] != postData['confirm_pw']:
            errors['pw_match'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        if not postData:
            return
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) == 0:           
            errors['email'] = "Invalid email address!"

        current_emails = User.objects.filter(email=postData['email'])
        if len(current_emails) == 0:
                errors['userunknown'] = "This user email does not exist"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters long"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    objects = UserManager()
    # book = models.ForeignKey(Book, related_name="user", on_delete=models.CASCADE, null=True)
    # review = models.ForeignKey(Review, related_name="user", on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"Author object: {self.id} {self.first_name} {self.Last_name}"


class Author(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    # note = models.TextField(null=True)
    # book = models.ForeignKey(Book, related_name="author", on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"Author object: {self.id} {self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="book", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="book", on_delete=models.CASCADE, null=True)
    # review = models.ForeignKey(Review, related_name="book", on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"Book object: {self.id} {self.title} {self.author}"

class Review(models.Model):
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, related_name="review", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name="review", on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return f"Author object: {self.id} {self.content}"

