from django.conf.urls import include, url
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoryViewSet, CommentDetailViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UserMeViewSet,
                    UserViewSet, get_user_token, send_confirmation_code)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/',
                TitleViewSet, basename='test_titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename="reviews")
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename="comments")
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
                CommentDetailViewSet, basename="comments_detail")

router.register('users', UserViewSet)
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('auth/email/', send_confirmation_code, name='send_code'),
    path('auth/token/', get_user_token, name='send_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    url('', include(router.urls)),
]
