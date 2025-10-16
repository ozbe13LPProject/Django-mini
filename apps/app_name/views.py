from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .services import list_user_accounts, create_new_account, delete_account_if_owner
from .permissions import IsOwnerAccount, IsOwnerTransaction


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank_name', 'account_number', 'bank_code']

    def get_queryset(self):
        return list_user_accounts(self.request.user, filters=self.request.query_params)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerAccount]
    lookup_field = 'account_id'
    queryset = Account.objects.all()


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account']

    def get_queryset(self):
        queryset = Transaction.objects.all()
        account_id = self.request.query_params.get('account')
        if account_id:
            queryset = queryset.filter(account_id=account_id, account__user=self.request.user)
        else:
            queryset = queryset.filter(account__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.user != self.request.user:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerTransaction]
    lookup_field = 'transaction_id'
    queryset = Transaction.objects.all()



