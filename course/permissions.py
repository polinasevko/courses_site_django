from rest_framework.permissions import BasePermission


class TeacherPermissions(BasePermission):
    """
    All permissions - teacher
    """
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        return False


class StudentPermissions(BasePermission):
    """
    All permissions - student
    """
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if request.user.as_student.filter(id=course_id).exists():
            return True
        return False


class CourseMembershipPermission(BasePermission):
    """
    LCRUD - teacher
    LR - student
    """
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        if view.action in ['list', 'retrieve']:
            if request.user.as_student.filter(id=course_id).exists():
                return True
        return False


class HomeworkPermission(BasePermission):
    """
    C - student
    LRUD - student-owner
    LR - teacher
    """
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if request.user.as_student.filter(id=course_id).exists():
            return True
        if view.action in ['list', 'retrieve']:
            if request.user.as_teacher.filter(id=course_id).exists():
                return True
        return False


class CommentPermission(BasePermission):
    """
    C - teacher/student
    LR - teacher/student-owner
    UD - owner
    """
    # LC RUD
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        homework_id = view.kwargs['homework_pk']
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        if request.user.homework_set.filter(id=homework_id).exists():
            return True
        return False

    # R - all teachers, owner student, UD - owner
    def has_object_permission(self, request, view, obj):
        course_id = view.kwargs['course_pk']
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        if obj.owner is request.user:
            return True
        return False
