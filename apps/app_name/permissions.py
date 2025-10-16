from rest_framework import permissions


class IsOwnerAccount(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerTransaction(permissions.BasePermission):
    """
    거래 소유자(계좌 소유자)만 접근 가능
    """

    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user
