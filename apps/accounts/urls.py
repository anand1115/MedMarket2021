from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
app_name = 'accounts'

urlpatterns = [
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name='token_refresh'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(), name = 'default-logout'),
    # path('user-register/',views.UserRegisterView.as_view(), name = 'default-user-register'),
] + router.urls