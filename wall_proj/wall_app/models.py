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
        today = date.today()

        NAME_REGEX = re.compile ('[a-zA-Z0-9_]')
        # if len(postData['first_name']) < 2 or not NAME_REGEX.match(postData['first_name']):
        #     errors["first_name"] = "First name should be atleast 2 characters long and must be all letters"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be atleast 2 characters long" 

        if not NAME_REGEX.match(postData['first_name']):
            errors["first_name"] = "First name must be all letters"
        # if len(postData['last_name']) < 2 or not NAME_REGEX.match(postData['last_name']):
        #     errors["last_name"] = "Last name should be atleast 2 characters long and must be all letters"

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
    # message = models.ForeignKey(Message, related_name="users", on_delete=models.CASCADE, null=True)
    # comment = models.ForeignKey(Comment, related_name="users", on_delete=models.CASCADE, null=True)


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="message", on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, related_name="comment", on_delete=models.CASCADE, null=True)

