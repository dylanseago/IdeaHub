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

    def __str__(self):
        return self.name

class Idea(DatedModel):
    creator = models.ForeignKey(User, related_name="ideas")
    name = models.TextField(max_length=100)
    category = models.ForeignKey(Category, related_name="ideas")
    tags = models.CharField(max_length=250, default='', blank=True)
    description = models.TextField(max_length=4000)

    @property
    def likes(self):
        return Rating.objects.filter(idea=self.id, positive=True).count()

    @property
    def dislikes(self):
        return Rating.objects.filter(idea=self.id, positive=False).count()

    @property
    def total_ratings(self):
        return Rating.objects.filter(idea=self.id).count()

    @property
    def net_rating(self):
        return self.likes - self.dislikes

    @property
    def percent_liked(self):
        total = self.total_ratings
        if total == 0:
            return 0
        return (float(self.likes) / total) * 100

    @property
    def percent_disliked(self):
        total = self.total_ratings
        if total == 0:
            return 0
        return (float(self.dislikes) / total) * 100

    def as_json(self):
        from jumpstart.apps.home.templatetags.custom_tags import sentences
        return {
            'creator_id': self.creator.id,
            'name': self.name,
            'category': self.category.name,
            'tags': self.tags,
            'summary': sentences(self.description, 1),
            'description': self.description,
            'likes': self.likes,
            'dislikes': self.dislikes,
        }

    def get_absolute_url(self):
        return reverse('idea', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Rating(models.Model):
    rater = models.ForeignKey(User, related_name="ratings_given")
    idea = models.ForeignKey(Idea, related_name="ratings")
    positive = models.BooleanField(default=True)


def sort_ideas(ideas):
    return sorted(ideas, key=lambda x: (x.net_rating, x.likes), reverse=True)