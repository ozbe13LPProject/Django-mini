from django.urls import path
from . import views

app_name = "accounts"  # 네임스페이스 설정

urlpatterns = [
    # Template Views (웹 페이지)
    path("signup/", views.register_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.account_list_view, name="account_list"),
    path("create/", views.account_create_view, name="account_create"),
    path("<int:pk>/update/", views.account_update_view, name="account_update"),
    path("<int:pk>/delete/", views.account_delete_view, name="account_delete"),
    # 계좌관리
    path(
        "<int:account_pk>/transactions/",
        views.transaction_list_view,
        name="transaction_list",
    ),
    path(
        "<int:account_pk>/transactions/create/",
        views.transaction_create_view,
        name="transaction_create",
    ),
    path(
        "<int:account_pk>/transactions/<int:pk>/update/",
        views.transaction_update_view,
        name="transaction_update",
    ),
    path(
        "<int:account_pk>/transactions/<int:pk>/delete/",
        views.transaction_delete_view,
        name="transaction_delete",
    ),
]
