from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer
from .models import CustomUser

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data


        response = Response(
            {"message": "로그인 성공", "access": tokens["access"]},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="refresh",
            value=tokens["refresh"],
            httponly=True,
            samesite="Lax",
            secure=False,
        )
        return response

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({"detail": "쿠키에 refresh 토큰이 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)
        serializer.save()


        response = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        return response

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)