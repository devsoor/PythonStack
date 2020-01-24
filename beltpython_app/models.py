from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt
from datetime import date, datetime, timedelta
import pprint

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        if not postData:
            return
        errors = {}
        NAME_REGEX = re.compile ('[a-zA-Z_]')

        if NAME_REGEX.match(postData['first_name']) == None or len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be all letters and length atleast 2 characters long"

        if NAME_REGEX.match(postData['last_name']) == None or len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be all letters and length atleast 2 characters long"


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

class TripManager(models.Manager):
    def trip_validator(self, postData):
        if not postData:
            return
        errors = {}
        today = date.today()

        NAME_REGEX = re.compile ('[a-zA-Z_]')

        if NAME_REGEX.match(postData['destination']) == None or len(postData['destination']) < 3:
            errors["destination"] = "Destination must be all letters and length atleast 3 characters long"

        if len(postData['plan']) < 3:
            errors["last_name"] = "Length of plan should be atleast 3 characters long"

        if len(postData['start_date']) < 10:
            errors["start_date"] = "Start Date is not complete"

        if  str(postData['start_date']) > str(today):
            errors["start_date"] = "Start date has to be in the future. Time travel is not allowed!!!!"

        if len(postData['end_date']) < 10:
            errors["end_date"] = "End Date is not complete"
        
        if  str(postData['end_date']) <= str(postData['start_date']):
            errors["end_date"] = "End date has to be after the start date"


        return errors

class User(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.CharField(max_length=50)
    pw_hash = models.CharField(max_length=255)
    level = models.CharField(max_length=50, default="normal")
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
    # trip = models.ManyToManyField(Trip, related_name="user")
    # creator = models.ForeignKey(Trip, related_name="creator", on_delete=models.CASCADE, null=True)


    def __repr__(self):
        return f"User object: {self.id} {self.first_name} {self.last_name}"

class Trip(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    destination = models.CharField(max_length=100)
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name="trip_creator", on_delete=models.CASCADE, null=True)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    user = models.ManyToManyField(User, related_name="trip")
    objects = TripManager()


