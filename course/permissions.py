from rest_framework.permissions import BasePermission


class TeacherPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        course_id = view.kwargs['pk']
        if request.method == 'GET':
            if request.user.as_teacher.filter(id=course_id).exists() or \
                    request.user.as_student.filter(id=course_id).exists():
                return True
        if request.user in obj.teachers.all():
            return True
        return False


class CoursePermission(BasePermission):
    # create - any user
    def has_object_permission(self, request, view, obj):
        course_id = view.kwargs['pk']
        if view.action == 'retrieve':
            if request.user.as_teacher.filter(id=course_id).exists() or \
                    request.user.as_student.filter(id=course_id).exists():
                return True
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        return False


# LCRUD teacher LR student
class CourseMembershipPermission(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if view.action in ['list', 'retrieve']:
            if request.user.as_teacher.filter(id=course_id).exists() or \
                    request.user.as_student.filter(id=course_id).exists():
                return True
        if request.user.as_teacher.filter(id=course_id).exists():
            return True
        return False


# C student, LRUD student(owner), LR teacher
class HomeworkPermission(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs['course_pk']
        if view.action in ['list', 'retrieve']:
            if request.user.as_teacher.filter(id=course_id).exists() or \
                    request.user.as_student.filter(id=course_id).exists():
                return True
        if request.user.as_student.filter(id=course_id).exists():
            return True
        return False
