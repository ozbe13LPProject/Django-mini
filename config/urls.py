from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.accounts.views import (
    RegisterView,
    LogoutView,
    AccountListCreateView,
    AccountDetailView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API 문서
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # ============================================
    # REST API 엔드포인트
    # ============================================
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="api-register"),
    path("api/logout/", LogoutView.as_view(), name="api-logout"),
    path("api/accounts/", AccountListCreateView.as_view(), name="api-account-list"),
    path(
        "api/accounts/<int:pk>/", AccountDetailView.as_view(), name="api-account-detail"
    ),
    # ============================================
    # Template 웹 페이지 (include 사용)
    # ============================================
    path("accounts/", include("apps.accounts.urls")),  # accounts 앱의 URL 포함
]
