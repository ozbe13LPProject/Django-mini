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
]
