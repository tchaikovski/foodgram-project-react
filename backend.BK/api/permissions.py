from rest_framework import permissions


def safe_methods(request):
    if request.method in permissions.SAFE_METHODS:
        return True
    return False


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if safe_methods(request):
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if safe_methods(request):
            return True
        if request.user.is_staff:
            return True
        return False


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            safe_methods(request)
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            safe_methods(request)
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_staff
                )
            )
        )
