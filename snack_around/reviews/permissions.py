from rest_framework.permissions import BasePermission

AUTH_REQUIRED_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']


class ReviewsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in AUTH_REQUIRED_METHODS and request.user.is_authenticated:
            if request.user.is_customer:
                return True

        if request.method == 'GET':
            return True

        return False
