from rest_framework.permissions import BasePermission


class TeacherPermissions(BasePermission):
    """
    All permissions to teacher
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')
        if not course_id:
            course_id = view.kwargs['pk']
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        return False


class StudentPermissions(BasePermission):
    """
    All permissions to student
    """
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_pk')
        if not course_id:
            course_id = view.kwargs['pk']
        if request.user.as_student.filter(id=course_id).exists():
            return True
        return False


class IsOwnerOfComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner is request.user:
            return True
        return False
