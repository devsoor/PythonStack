from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(null=True)
    # authors = models.ManyToManyField(Author, related_name="books")

    def __repr__(self):
        return f"Book object: {self.id} {self.title} {self.desc}"

class Author(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    notes = models.TextField(null=True)
    books = models.ManyToManyField(Book, related_name="authors")

    def __repr__(self):
        return f"Author object: {self.id} {self.first_name} {self.last_name} {self.notes}"