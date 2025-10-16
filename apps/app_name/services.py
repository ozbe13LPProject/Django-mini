from django.shortcuts import get_object_or_404
from . import repositories


def list_user_accounts(user, filters=None):
    return repositories.get_accounts_by_user(user, filters)


def create_new_account(user, validated_data):
    return repositories.create_account(
        user=user,
        bank_name=validated_data['bank_name'],
        account_number=validated_data['account_number'],
        balance=validated_data.get('balance', 0),
        bank_code=validated_data['bank_code'],
    )


def delete_account_if_owner(user, account_id):
    account = get_object_or_404(repositories.Account, account_id=account_id)
    if account.user != user:
        return False, "삭제 권한이 없습니다."
    repositories.delete_account(account)
    return True, None


