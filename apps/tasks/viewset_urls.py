from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewset_views import CategoryViewSet


router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls))
]

