from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Account, Transaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "name", "nickname", "phone", "is_active", "is_staff"]
    list_filter = ["is_active", "is_staff", "is_admin"]
    search_fields = ["email", "name", "nickname", "phone"]
    ordering = ["-id"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인정보", {"fields": ("name", "nickname", "phone")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_admin", "is_superuser")}),
        ("그룹", {"fields": ("groups", "user_permissions")}),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_number",
        "user",
        "get_bank_name",
        "get_account_type_name",
        "balance",
        "created_at",
    ]
    list_filter = ["bank_code", "account_type", "created_at"]
    search_fields = ["account_number", "user__email", "user__name"]
    ordering = ["-created_at"]

    def get_bank_name(self, obj):
        return obj.get_bank_code_display()

    get_bank_name.short_description = "은행"

    def get_account_type_name(self, obj):
        return obj.get_account_type_display()

    get_account_type_name.short_description = "계좌종류"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "account",
        "get_transaction_type_name",
        "get_transaction_method_name",
        "amount",
        "balance_after",
        "transaction_at",
    ]
    list_filter = ["transaction_type", "transaction_method", "transaction_at"]
    search_fields = ["account__account_number", "description"]
    ordering = ["-transaction_at"]

    def get_transaction_type_name(self, obj):
        return obj.get_transaction_type_display()

    get_transaction_type_name.short_description = "거래유형"

    def get_transaction_method_name(self, obj):
        return obj.get_transaction_method_display() if obj.transaction_method else "-"

    get_transaction_method_name.short_description = "거래방법"
