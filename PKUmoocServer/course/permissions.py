from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    """仅老师可以修改, 其他用户仅可查看"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_teacher:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser
