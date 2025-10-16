from django.urls import path
from .views import (
    AccountListCreateView, AccountDetailView,
    TransactionListCreateView, TransactionDetailView
)

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:account_id>/', AccountDetailView.as_view(), name='account-detail'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:transaction_id>/', TransactionDetailView.as_view(), name='transaction-detail'),
]





