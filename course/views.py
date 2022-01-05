from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import TeacherPermissions, CourseMembershipPermission, CoursePermission, HomeworkPermission
from .models import Course, Lecture, Hometask, Homework, Mark
from .serializers import (
    CourseSerializer,
    AddTeacherSerializer,
    AddDeleteStudentSerializer,
    LectureSerializer,
    HometaskSerializer,
    HomeworkSerializer,
    MarkSerializer,
)


class CourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, CoursePermission]

    def get_queryset(self):
        teacher_courses = self.request.user.as_teacher.all()
        student_courses = self.request.user.as_student.all()
        queryset = teacher_courses | student_courses
        return queryset.distinct()


class AddTeacherView(generics.RetrieveUpdateAPIView):
    serializer_class = AddTeacherSerializer
    permission_classes = [TeacherPermissions]

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs['pk'])


class AddDeleteStudentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddDeleteStudentSerializer
    permission_classes = [TeacherPermissions]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            for student in serializer.validated_data['students']:
                instance.students.remove(student.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs['pk'])


class LectureView(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [CourseMembershipPermission]

    def get_queryset(self):
        return Lecture.objects.filter(course=self.kwargs['course_pk'])


class HometaskView(viewsets.ModelViewSet):
    serializer_class = HometaskSerializer
    permission_classes = [CourseMembershipPermission]

    def get_queryset(self):
        return Hometask.objects.filter(lecture=self.kwargs['lecture_pk'])


class HomeworkView(viewsets.ModelViewSet):
    serializer_class = HomeworkSerializer
    permission_classes = [HomeworkPermission]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        user = self.request.user
        if user.as_student.filter(id=course_id).exists():
            return Homework.objects.filter(hometask=self.kwargs['hometask_pk'], student=user)
        return Homework.objects.filter(hometask=self.kwargs['hometask_pk'])


class MarkView(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [CourseMembershipPermission]

    def get_queryset(self):
        # course_id = self.kwargs['course_pk']
        # user = self.request.user
        # if user.as_student.filter(id=course_id).exists():
        #     return Mark.objects.filter(homework=self.kwargs['homework_pk'])
        return Mark.objects.filter(homework=self.kwargs['homework_pk'])
