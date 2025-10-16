from rest_framework import serializers
from .models import User, Account


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "nickname", "phone", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            phone=validated_data["phone"],
            password=validated_data["password"],
        )
        return user


class AccountSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "user_email",
            "account_number",
            "bank_code",
            "account_type",
            "balance",
        ]
        read_only_fields = ["user"]
