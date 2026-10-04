from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.tasks.generic_api_views import LogOut, RegisterView


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token-obtain-pair-view'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),
    path('auth/logout/', LogOut.as_view(), name='logout-view'),
    path('auth/register/', RegisterView.as_view(), name='register-view')
]

