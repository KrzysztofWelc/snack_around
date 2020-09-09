from rest_framework.permissions import BasePermission
import pprint

AUTH_REQUIRED_METHODS = ['POST', 'PUT', 'DELETE']
pp = pprint.PrettyPrinter(indent=4)


class ReviewsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in AUTH_REQUIRED_METHODS and request.user.is_authenticated:
            if request.user.is_customer:
                return True

        if request.method == 'GET':
            return True

        return False
