from .models import Account


def get_accounts_by_user(user, filters=None):
    queryset = Account.objects.filter(user=user)
    if filters:
        if 'bank_name' in  filters:
            queryset = queryset.filter(bank_name__icontains=filters['bank_name'])
        if 'account_number' in filters:
            queryset = queryset.filter(account_number__icontains=filters['account_number'])
        if 'bank_code' in filters:
            queryset = queryset.filter(bank_code__icontains=filters['bank_code'])
    return queryset.order_by('-created_at')


def get_account_by_id(account_id):
    return Account.objects.filter(account_id=account_id).first()


def create_account(user, bank_name, account_number, balance, bank_code):
    return Account.objects.create(
        user=user,
        bank_name=bank_name,
        account_number=account_number,
        balance=balance,
        bank_code=bank_code
    )


def delete_account(account):
    account.delete()


