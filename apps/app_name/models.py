from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=50, unique=True)
    bank_code = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} ({self.bank_code})"


class Transaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    action_type = models.CharField(max_length=30)
    action_detail = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} {self.amount} on {self.transaction_at}"




