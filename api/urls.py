from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import AchievementViewSet, BackgroundViewSet, BookViewSet, OpenLibrarySearch, UserListView, ShelfViewSet


router = SimpleRouter()
router.register('books', BookViewSet, basename='book')
router.register('shelves', ShelfViewSet, basename='shelf')
router.register(r'backgrounds', BackgroundViewSet, basename='background')
router.register(r'achievements', AchievementViewSet, basename='achievement')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/search/', OpenLibrarySearch.as_view()),
    path('v1/users/', UserListView.as_view(), name='user-list'),
]
