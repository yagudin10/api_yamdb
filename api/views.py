from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from review.models import Comment, Review
from title.models import Category, Genre, Title
from user.models import User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly,
                          IsOwnerOrStaffOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, UserCreateSerializer,
                          UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = TitleFilter


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
            review = Review.objects.filter(
                title=title, author=self.request.user)
            if review.exists():
                raise ParseError
            serializer.save(author=self.request.user, title=title)
        else:
            raise exceptions.NotAuthenticated()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser | IsAdmin]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        self.kwargs['username'] = request.user.username

        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            return self.partial_update(request)


class UserMeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch']
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
            serializer.save(author=self.request.user, review=review)
        else:
            raise exceptions.NotAuthenticated()


class CommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("comment_id"))
        return comment


@api_view(['POST'])
def send_confirmation_code(request):
    user = request.data
    serializer = UserCreateSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(User, email=serializer.data.get('email'))
    confirmation_code = get_random_string(length=32)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Token',
        confirmation_code,
        'from@example.com',
        [serializer.data.get('email')],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_user_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             email=serializer.data.get('email'),
                             confirmation_code=serializer.data.get(
                                 'confirmation_code'),
                             )
    user.email_confirmed = True
    user.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)
