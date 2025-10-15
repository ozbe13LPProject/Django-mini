from django.db import models

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    id = models.BigIntegerField()
    account_number = models.CharField(max_length=50, unique=True, null=False)
    bank_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.account_number} ({self.bank_code})"

class Transaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.BigIntegerField()
    action_type = models.CharField(max_length=30)
    action_detail = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_type} {self.amount} on {self.transaction_at}"


