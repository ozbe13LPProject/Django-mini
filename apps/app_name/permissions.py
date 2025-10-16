from rest_framework import permissions


class IsOwnerAccount(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerTransaction(permissions.BasePermission):



    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user
