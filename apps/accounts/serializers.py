from rest_framework import serializers
from .models import User, Account, Transaction


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
    bank_name = serializers.CharField(source="get_bank_code_display", read_only=True)
    account_type_name = serializers.CharField(
        source="get_account_type_display", read_only=True
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "user_email",
            "account_number",
            "bank_code",
            "bank_name",
            "account_type",
            "account_type_name",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    transaction_method_display = serializers.CharField(
        source="get_transaction_method_display", read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "transaction_type",
            "transaction_type_display",
            "transaction_method",
            "transaction_method_display",
            "amount",
            "balance_after",
            "description",
            "transaction_at",
        ]
        read_only_fields = ["balance_after", "transaction_at"]
