import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.PositiveIntegerField(
        default=current_year(), 
        validators=[MinValueValidator(0), max_value_current_year], 
        blank=True)
    rating = models.FloatField(default=0)
    description = models.CharField(max_length=300, blank=True)
    genre = models.ManyToManyField(
        Genre, blank=True, related_name="titles")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, 
        blank=True, null=True, related_name="titles")
