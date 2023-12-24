from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdminUserOrNotRegistered(BasePermission):
    """仅管理员和未完善身份信息的用户可注册"""
    def has_permission(self, request, view):
        # 仅管理员和未完善身份信息的用户可注册为学生或老师
        if request.method == 'POST':
            return bool(
                request.user.is_superuser or
                (
                    not (request.user.is_student or request.user.is_teacher)
                    and request.user.is_authenticated
                )
            )
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser

class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # 对所有人允许 GET, HEAD, OPTIONS 请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 仅管理员可进行其他操作
        return request.user.is_superuser

class IsAdminUserOrSelf(BasePermission):
    """仅管理员可访问所有信息，登陆用户只访问自己的信息，其余用户只能注册"""
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.user == request.user or request.user.is_superuser)
