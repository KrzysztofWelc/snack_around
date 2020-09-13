from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_client)


class IsRestaurant(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_restaurant)
