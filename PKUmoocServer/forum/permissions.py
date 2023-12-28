from rest_framework.permissions import BasePermission, SAFE_METHODS

'''
教师可以在讨论区内创建多个板块。每个板块下可以包含多个帖子。每个帖子可以包含多个回复。
教师可以设置板块和帖子的权限，删除帖子或回复。
学生仅可以删除自己发布的帖子、回复。

讨论区--> super user only
板块--> super user, 教师 (all)
帖子--> super user, 教师 (create, delete), 学生 (create delete OWN) - super user teacher or owner
回复--> super user, 教师 (create, delete), 学生 (create delete OWN) - super user teacher or owner
'''


class IsReadOnly(BasePermission):
    message = "仅可读，为了讨论区设置的"
    # read only 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsTeacherOrReadOnly(BasePermission):
    message = '老师可创建或删除板块，其他人可阅读板块 '

    # before creation of account, author = self
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_teacher #and request.user.is_authenticated #加上这个老师只可以创建或删除（自己创建的）板块

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_teacher

class IsTeacherOrOwner(BasePermission):
    message = '老师可创建或删除帖子、回复，学生可以创建或删除自己发布的帖子、回复'

    # read only 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["POST", "DELETE"]:
            return ((request.user.is_student and request.user.is_authenticated) 
                    or (request.user.is_teacher) or request.user.is_superuser)

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ["POST", "DELETE"]:
            return ((request.user.is_student and  obj.author == request.user) 
                    or (request.user.is_teacher) or request.user.is_superuser)
        return request.user.is_superuser
    
