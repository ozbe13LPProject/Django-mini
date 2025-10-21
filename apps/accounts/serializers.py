from rest_framework import serializers
from .models import User, Account, Transaction


class UserSerializer(serializers.ModelSerializer):
    """REST API: 사용자 Serializer"""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "nickname", "phone", "password"]

    def create(self, validated_data):
        """비밀번호 암호화하여 사용자 생성"""
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
    """REST API: 계좌 Serializer"""

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
    """REST API: 거래 내역 Serializer"""

    transaction_type_display = serializers.CharField(
        source="get_transaction_type_display", read_only=True
    )
    transaction_method_display = serializers.CharField(
        source="get_transaction_method_display", read_only=True
    )
    bank_name = serializers.CharField(source="account.bank_name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "bank_name",
            "transaction_type",
            "transaction_type_display",
            "transaction_method",
            "transaction_method_display",
            "amount",
            "balance_after",
            "description",
            "transaction_at",
        ]
        read_only_fields = ["id", "balance_after", "transaction_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    """REST API: 거래 생성용 Serializer (계좌 자동 처리)"""

    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
            "transaction_method",
            "amount",
            "description",
        ]

    def validate_amount(self, value):
        """금액 유효성 검사"""
        if value <= 0:
            raise serializers.ValidationError("거래 금액은 0보다 커야 합니다.")
        return value

    def create(self, validated_data):
        """거래 생성 시 잔액 자동 계산"""
        account = self.context["account"]
        transaction_type = validated_data["transaction_type"]
        amount = validated_data["amount"]

        # 잔액 계산
        if transaction_type == "DEPOSIT":
            account.balance += amount
        elif transaction_type == "WITHDRAW":
            if account.balance < amount:
                raise serializers.ValidationError({"amount": "잔액이 부족합니다."})
            account.balance -= amount

        # 거래 생성
        transaction = Transaction.objects.create(
            account=account, balance_after=account.balance, **validated_data
        )

        account.save()
        return transaction


class AccountDetailSerializer(AccountSerializer):
    """REST API: 계좌 상세 정보 (최근 거래 포함)"""

    recent_transactions = TransactionSerializer(
        source="transactions", many=True, read_only=True
    )

    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ["recent_transactions"]

    def to_representation(self, instance):
        """최근 거래 5개만 반환"""
        representation = super().to_representation(instance)
        representation["recent_transactions"] = TransactionSerializer(
            instance.transactions.all()[:5], many=True
        ).data
        return representation
