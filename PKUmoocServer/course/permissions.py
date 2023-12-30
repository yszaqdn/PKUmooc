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


class IsTeacherOrOwner(permissions.BasePermission):
    message = '老师可创建或删除帖子、回复，学生可以创建或删除自己发布的帖子、回复'

    # read only 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif request.method in ["POST", "DELETE"]:
            return ((request.user.is_student and request.user.is_authenticated) 
                    or (request.user.is_teacher) or request.user.is_superuser)

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ["POST", "DELETE"]:
            return ((request.user.is_student and  obj.author == request.user) 
                    or (request.user.is_teacher) or request.user.is_superuser)
        return request.user.is_superuser

