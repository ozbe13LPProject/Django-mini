from .models import Account

def get_accounts_by_user(user):
    return Account.objects.filter(user=user).order_by('-created_at')

def get_account_by_id(account_id):
    return Account.objects.filter(id=account_id).first()

def create_account(user, bank_name, account_number, balance):
    return Account.objects.create(
        user=user,
        bank_name=bank_name,
        account_number=account_number,
        balance=balance
    )

def delete_account(account):
    account.delete()
