from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Account, Transaction
from constants import BANK_CODES, ACCOUNT_TYPE, TRANSACTION_TYPE, TRANSACTION_METHOD


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="이메일", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        label="이름",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    nickname = forms.CharField(
        label="닉네임",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="전화번호",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "010-1234-5678"}
        ),
    )
    password1 = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["email", "name", "nickname", "phone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"]
        user.nickname = self.cleaned_data["nickname"]
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Template: 로그인 폼"""

    email = forms.EmailField(
        label="이메일", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["account_number", "bank_code", "account_type", "balance"]
        labels = {
            "account_number": "계좌번호",
            "bank_code": "은행",
            "account_type": "계좌종류",
            "balance": "초기 잔액",
        }
        widgets = {
            "account_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "1234-5678-9012"}
            ),
            "bank_code": forms.Select(
                choices=BANK_CODES, attrs={"class": "form-control"}
            ),
            "account_type": forms.Select(
                choices=ACCOUNT_TYPE, attrs={"class": "form-control"}
            ),
            "balance": forms.NumberInput(
                attrs={"class": "form-control", "step": "10", "min": "10"}
            ),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["transaction_type", "transaction_method", "amount", "description"]
        labels = {
            "transaction_type": "거래 유형",
            "transaction_method": "거래 방법",
            "amount": "거래 금액",
            "description": "거래 내용",
        }
        widgets = {
            "transaction_type": forms.Select(
                choices=TRANSACTION_TYPE, attrs={"class": "form-control"}
            ),
            "transaction_method": forms.Select(
                choices=TRANSACTION_METHOD, attrs={"class": "form-control"}
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "10",
                    "min": "10",
                    "placeholder": "금액 입력",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "거래 내용 입력 (선택사항)",
                }
            ),
        }
