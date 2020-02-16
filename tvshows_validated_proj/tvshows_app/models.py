from django.db import models
from datetime import date

class Network(models.Model):
    name = models.CharField(max_length=25)
    # shows = models.ForeignKey(Show, related_name="networks", on_delete=models.CASCADE, null=True)

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        if not postData:
            return
        errors = {}
        today = date.today()

        show_title = Show.objects.filter(title=postData['title'])
        # if len(show_title) > 0:
        #     errors["title"] = "Title must be unique"
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        if len(postData['network']) < 3:
            errors["network"] =  "Network should be at least 3 characters"
        if len(postData['desc']) > 0 and len(postData['desc']) < 10:
            errors["desc"] = "Description should be at least 10 characters"
        if len(postData['release_date']) < 10:
            errors["release_date"] = "Release Date is not complete"
        if  str(postData['release_date']) >= str(today):
            errors["release_date"] = "Release Date should be in the past"
        return errors

class Show(models.Model):
    title = models.CharField(max_length=25)
    network = models.CharField(max_length=25)
    release_date = models.DateField()
    desc = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    networks = models.ForeignKey(Network, related_name="shows", on_delete=models.CASCADE, null=True)
    objects = ShowManager()

