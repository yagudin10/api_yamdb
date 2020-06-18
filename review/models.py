import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from title.models import Title
from user.models import User


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", null=True)
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews", null=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments", null=True)
