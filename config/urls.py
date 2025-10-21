"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

from apps.accounts.views import (
    RegisterView,
    LogoutView,
    AccountListCreateView,
    AccountDetailView,
)


from apps.accounts.views import login_view

urlpatterns = [
    path("", login_view, name="root_login"),
    # Admin
    path("admin/", admin.site.urls),
    # ============================================
    # API 문서
    # ============================================
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # ============================================
    # REST API 및 JWT 엔드포인트
    # ============================================
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # HEAD의 accounts 관련 API 엔드포인트
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
