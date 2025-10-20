from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime

from .models import User, Account, Transaction
from .serializers import UserSerializer, AccountSerializer
from .forms import UserRegisterForm, UserLoginForm, AccountForm, TransactionForm


# ============================================
# REST API Views
# ============================================


class RegisterView(generics.CreateAPIView):
    """REST API: 회원가입"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    """REST API: 로그아웃 (JWT 블랙리스트)"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST
            )


class AccountListCreateView(generics.ListCreateAPIView):
    """REST API: 계좌 목록 조회 및 생성"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """REST API: 계좌 조회, 수정, 삭제"""

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


# ============================================
# Template Views - 인증
# ============================================


def register_view(request):
    """Template: 회원가입 페이지"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입이 완료되었습니다! 로그인해주세요.")
            return redirect("accounts:login")
        else:
            messages.error(request, "입력 정보를 확인해주세요.")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """Template: 로그인 페이지"""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"{user.name}님, 환영합니다!")
                return redirect("accounts:account_list")
            else:
                messages.error(request, "이메일 또는 비밀번호가 올바르지 않습니다.")
        else:
            messages.error(request, "입력 정보를 확인해주세요.")
    else:
        form = UserLoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """Template: 로그아웃"""
    if request.method == "POST":
        logout(request)
        messages.success(request, "로그아웃되었습니다.")
    return redirect("accounts:login")


# ============================================
# Template Views - 계좌 관리
# ============================================


@login_required(login_url="accounts:login")
def account_list_view(request):
    """Template: 계좌 목록 페이지"""
    accounts = Account.objects.filter(user=request.user)
    total_balance = accounts.aggregate(Sum("balance"))["balance__sum"] or 0

    return render(
        request,
        "accounts/account_list.html",
        {
            "accounts": accounts,
            "total_balance": total_balance,
        },
    )


@login_required(login_url="accounts:login")
def account_create_view(request):
    """Template: 계좌 생성 페이지"""
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "계좌가 추가되었습니다!")
            return redirect("accounts:account_list")
        else:
            messages.error(request, "입력 정보를 확인해주세요.")
    else:
        form = AccountForm()

    return render(request, "accounts/account_form.html", {"form": form})


@login_required(login_url="accounts:login")
def account_update_view(request, pk):
    """Template: 계좌 수정 페이지"""
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "계좌 정보가 수정되었습니다!")
            return redirect("accounts:account_list")
        else:
            messages.error(request, "입력 정보를 확인해주세요.")
    else:
        form = AccountForm(instance=account)

    return render(request, "accounts/account_form.html", {"form": form})


@login_required(login_url="accounts:login")
def account_delete_view(request, pk):
    """Template: 계좌 삭제"""
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == "POST":
        account_number = account.account_number
        account.delete()
        messages.success(request, f"계좌 {account_number}이(가) 삭제되었습니다.")

    return redirect("accounts:account_list")


# ============================================
# Template Views - 거래 내역
# ============================================


@login_required(login_url="accounts:login")
def transaction_list_view(request, account_pk):
    """
    Template: 거래 내역 조회
    - 특정 계좌의 거래 내역 조회
    - 날짜별, 거래유형별 필터링
    - 시간순 정렬
    """
    account = get_object_or_404(Account, pk=account_pk, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    # 필터링
    transaction_type = request.GET.get("type")  # 입금/출금
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)

    if date_from:
        date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
        transactions = transactions.filter(transaction_at__gte=date_from_obj)

    if date_to:
        date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
        # 해당 날짜의 23:59:59까지 포함
        date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        transactions = transactions.filter(transaction_at__lte=date_to_obj)

    # 통계
    total_deposit = (
        transactions.filter(transaction_type="DEPOSIT").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    total_withdraw = (
        transactions.filter(transaction_type="WITHDRAW").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )

    return render(
        request,
        "accounts/transaction_list.html",
        {
            "account": account,
            "transactions": transactions,
            "total_deposit": total_deposit,
            "total_withdraw": total_withdraw,
            "filter_type": transaction_type,
            "filter_date_from": date_from,
            "filter_date_to": date_to,
        },
    )


@login_required(login_url="accounts:login")
def transaction_create_view(request, account_pk):
    """
    Template: 거래 추가
    - 입금/출금 거래 추가
    - 자동으로 잔액 계산 및 업데이트
    """
    account = get_object_or_404(Account, pk=account_pk, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account

            # 거래 후 잔액 계산
            if transaction.transaction_type == "DEPOSIT":
                # 입금: 잔액 증가
                account.balance += transaction.amount
            elif transaction.transaction_type == "WITHDRAW":
                # 출금: 잔액 감소
                if account.balance >= transaction.amount:
                    account.balance -= transaction.amount
                else:
                    messages.error(request, "잔액이 부족합니다!")
                    return render(
                        request,
                        "accounts/transaction_form.html",
                        {"form": form, "account": account},
                    )

            transaction.balance_after = account.balance
            transaction.save()
            account.save()

            messages.success(request, "거래가 등록되었습니다!")
            return redirect("accounts:transaction_list", account_pk=account.pk)
    else:
        form = TransactionForm()

    return render(
        request, "accounts/transaction_form.html", {"form": form, "account": account}
    )


@login_required(login_url="accounts:login")
def transaction_update_view(request, account_pk, pk):
    """
    Template: 거래 수정
    - 관리자만 수정 가능
    - 잔액 재계산
    """
    account = get_object_or_404(Account, pk=account_pk, user=request.user)
    transaction = get_object_or_404(Transaction, pk=pk, account=account)

    # 관리자만 수정 가능
    if not request.user.is_admin:
        messages.error(request, "관리자만 거래 내역을 수정할 수 있습니다.")
        return redirect("accounts:transaction_list", account_pk=account.pk)

    old_amount = transaction.amount
    old_type = transaction.transaction_type

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            # 이전 거래 취소
            if old_type == "DEPOSIT":
                account.balance -= old_amount
            else:
                account.balance += old_amount

            # 새 거래 적용
            new_transaction = form.save(commit=False)
            if new_transaction.transaction_type == "DEPOSIT":
                account.balance += new_transaction.amount
            else:
                if account.balance >= new_transaction.amount:
                    account.balance -= new_transaction.amount
                else:
                    messages.error(request, "잔액이 부족합니다!")
                    # 원래 거래 복구
                    if old_type == "DEPOSIT":
                        account.balance += old_amount
                    else:
                        account.balance -= old_amount
                    return render(
                        request,
                        "accounts/transaction_form.html",
                        {"form": form, "account": account, "transaction": transaction},
                    )

            new_transaction.balance_after = account.balance
            new_transaction.save()
            account.save()

            messages.success(request, "거래 정보가 수정되었습니다!")
            return redirect("accounts:transaction_list", account_pk=account.pk)
    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        "accounts/transaction_form.html",
        {"form": form, "account": account, "transaction": transaction},
    )


@login_required(login_url="accounts:login")
def transaction_delete_view(request, account_pk, pk):
    """
    Template: 거래 삭제
    - 관리자만 삭제 가능
    - 잔액 복구
    """
    account = get_object_or_404(Account, pk=account_pk, user=request.user)
    transaction = get_object_or_404(Transaction, pk=pk, account=account)

    # 관리자만 삭제 가능
    if not request.user.is_admin:
        messages.error(request, "관리자만 거래 내역을 삭제할 수 있습니다.")
        return redirect("accounts:transaction_list", account_pk=account.pk)

    if request.method == "POST":
        # 거래 취소하고 잔액 복구
        if transaction.transaction_type == "DEPOSIT":
            account.balance -= transaction.amount
        else:
            account.balance += transaction.amount

        account.save()
        transaction.delete()

        messages.success(request, "거래 내역이 삭제되었습니다.")

    return redirect("accounts:transaction_list", account_pk=account.pk)
