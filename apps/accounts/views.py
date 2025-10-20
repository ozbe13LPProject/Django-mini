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
from .models import User, Account
from .serializers import UserSerializer, AccountSerializer
from .forms import UserRegisterForm, UserLoginForm, AccountForm


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
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
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 사용자의 계좌만 조회
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 계좌 생성 시 자동으로 사용자를 연결
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인된 사용자의 계좌만 접근 가능
        return Account.objects.filter(user=self.request.user)


def register_view(request):
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
    if request.method == "POST":
        logout(request)
        messages.success(request, "로그아웃되었습니다.")
    return redirect("accounts:login")


@login_required(login_url="accounts:login")
def account_list_view(request):
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
    account = get_object_or_404(Account, pk=pk, user=request.user)

    if request.method == "POST":
        account_number = account.account_number
        account.delete()
        messages.success(request, f"계좌 {account_number}이(가) 삭제되었습니다.")

    return redirect("accounts:account_list")
