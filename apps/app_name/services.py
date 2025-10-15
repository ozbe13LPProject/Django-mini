from . import repositories

def list_user_accounts(user):
    return repositories.get_accounts_by_user(user)

def create_new_account(user, validated_data):
    return repositories.create_account(
        user=user,
        bank_name=validated_data['bank_name'],
        account_number=validated_data['account_number'],
        balance=validated_data['balance']
    )

def delete_account_if_owner(user, account_id):
    account = repositories.get_account_by_id(account_id)
    if account is None:
        return False, "계좌를 찾을 수 없습니다."
    if account.user != user:
        return False, "삭제 권한이 없습니다."
    repositories.delete_account(account)
    return True, None
