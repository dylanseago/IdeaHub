from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class DatedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100)

class Idea(DatedModel):
    poster = models.ForeignKey(User, related_name="ideas")
    category = models.ForeignKey(Category, related_name="ideas")
    name = models.TextField(max_length=100)
    summary = models.TextField(max_length=250)
    about = models.TextField(max_length=20000)
    tags = models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse('idea', args=[str(self.id)])

    def __str__(self):
        return self.name


class Rating(models.Model):
    rater = models.ForeignKey(User, related_name="ratings_given")
    idea = models.ForeignKey(Idea, related_name="ratings")
    positive = models.BooleanField(default=True)