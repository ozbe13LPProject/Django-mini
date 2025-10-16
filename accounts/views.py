from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Account
from .serializers import UserSerializer, AccountSerializer


# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# 로그아웃
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
        # 로그인한 계좌만 조회
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 계좌개통후 자동으로 사용자를 연결
        serializer.save(user=self.request.user)


# 계좌 조회,수정,삭제
class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인된 계좌만 접근 가능
        return Account.objects.filter(user=self.request.user)
