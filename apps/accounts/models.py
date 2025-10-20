from django.contrib.auth.models import AbstractUser
from django.db import models
from constants import BANK_CODES, ACCOUNT_TYPE, TRANSACTION_TYPE, TRANSACTION_METHOD


class User(AbstractUser):
    """사용자 모델"""

    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=100, verbose_name="이름")
    nickname = models.CharField(max_length=100, unique=True, verbose_name="닉네임")
    phone = models.CharField(max_length=20, unique=True, verbose_name="전화번호")
    is_staff = models.BooleanField(default=False, verbose_name="스태프 여부")
    is_admin = models.BooleanField(default=False, verbose_name="관리자 여부")
    is_active = models.BooleanField(default=True, verbose_name="계정 활성화 여부")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name", "nickname", "phone"]

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"

    def __str__(self):
        return self.email


class Account(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts", verbose_name="사용자"
    )
    account_number = models.CharField(
        max_length=20, unique=True, verbose_name="계좌번호"
    )
    bank_code = models.CharField(
        max_length=10, choices=BANK_CODES, default="000", verbose_name="은행코드"
    )
    account_type = models.CharField(
        max_length=20, choices=ACCOUNT_TYPE, default="CHECKING", verbose_name="계좌종류"
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, verbose_name="잔액"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        verbose_name = "계좌"
        verbose_name_plural = "계좌들"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_bank_code_display()} - {self.account_number}"


class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="계좌",
    )
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE, verbose_name="거래유형"
    )
    transaction_method = models.CharField(
        max_length=30,
        choices=TRANSACTION_METHOD,
        null=True,
        blank=True,
        verbose_name="거래방법",
    )
    amount = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name="거래금액"
    )
    balance_after = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name="거래후잔액"
    )
    description = models.CharField(max_length=300, verbose_name="거래내용", blank=True)
    transaction_at = models.DateTimeField(auto_now_add=True, verbose_name="거래일시")

    class Meta:
        verbose_name = "거래내역"
        verbose_name_plural = "거래내역들"
        ordering = ["-transaction_at"]

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount}원"
