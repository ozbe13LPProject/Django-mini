from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, AccountListCreateView, AccountDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("accounts/", AccountListCreateView.as_view(), name="account-list-create"),
    path("accounts/<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
]
