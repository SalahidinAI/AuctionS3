from rest_framework import permissions


class SellerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "продавец":
            return True


class BuyerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "покупатель":
            return True

