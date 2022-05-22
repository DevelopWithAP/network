from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True)

    # Returns all of the user's followers
    def get_followers(self):
        return self.followers.all()

    # Returns the number of followers for a particular user
    def count_followers(self):
        return self.get_followers().count()
    
    # Returns the users the current user is following
    def get_following(self):
        return self.following.all()
    
    # Returns the number of users the current user is following
    def count_following(self):
        return self.get_following().count()

class Post(models.Model):
    """ Stores a Post """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    likes = models.ManyToManyField(User, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    is_visible = models.BooleanField(default=True)

    # String representation of Post model
    def __str__(self):
        return str(self.id)

    # Returns the number of 'likes' for the post
    def get_likes(self):
        return self.likes.all().count()

    # Returns the users who 'like' the particular post
    def get_users_liked(self):
        qs = self.likes.all()
        return ", ".join([user.username for user in qs])

