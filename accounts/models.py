from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=100, verbose_name="이름")
    nickname = models.CharField(max_length=100, unique=True, verbose_name="닉네임")
    phone = models.CharField(max_length=20, unique=True, verbose_name="전화번호")
    is_staff = models.BooleanField(default=False, verbose_name="스태프 여부")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 여부")
    is_active = models.BooleanField(default=True, verbose_name="계정 활성화 여부")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name", "nickname", "phone"]

    def __str__(self):
        return self.email


class Account(models.Model):
    """
    계좌 모델 - 사용자의 가계부 계좌
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts", verbose_name="사용자"
    )
    account_number = models.CharField(
        max_length=20, unique=True, verbose_name="계좌번호"
    )
    bank_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="은행코드"
    )
    account_type = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="계좌종류"
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, verbose_name="잔액"
    )

    def __str__(self):
        return f"{self.user.email} - {self.account_number}"
