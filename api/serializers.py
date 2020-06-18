from django.db.models import Avg

from rest_framework import serializers

from review.models import Comment, Review
from title.models import Category, Genre, Title
from user.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name,
                'slug': value.slug}


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return {'name': value.name,
                'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        if not Review.objects.exists():
            return None

        return Review.objects.filter(title=obj).aggregate(Avg('score')).get('score__avg')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')
        model = User
        lookup_field = 'username'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User
        lookup_field = 'username'


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'confirmation_code', 'email_confirmed')
        model = User
