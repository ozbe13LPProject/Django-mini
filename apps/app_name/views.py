from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Transaction.objects.filter(account_id=account_id)
        return super().get_queryset()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'transaction_id'


