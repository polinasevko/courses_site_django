from django.db.models import F
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Course, Hometask, Homework, Lecture
from .permissions import (IsOwnerOfComment, StudentPermissions,
                          TeacherPermissions)
from .serializers import (AddDeleteStudentSerializer, AddTeacherSerializer,
                          CommentSerializer, CourseSerializer,
                          HometaskSerializer, HomeworkSerializer,
                          LectureSerializer, MarkSerializer)


class CourseView(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        teacher_courses = self.request.user.as_teacher.all()
        student_courses = self.request.user.as_student.all()
        queryset = teacher_courses | student_courses
        return queryset.distinct()

    def get_permissions(self):
        if self.action in ['create', 'list']:
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, TeacherPermissions | StudentPermissions]
        else:
            self.permission_classes = [IsAuthenticated, TeacherPermissions]
        return super().get_permissions()


class AddTeacherView(generics.RetrieveUpdateAPIView):
    serializer_class = AddTeacherSerializer
    permission_classes = [IsAuthenticated, TeacherPermissions]

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs['pk'])


class AddDeleteStudentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddDeleteStudentSerializer
    permission_classes = [IsAuthenticated, TeacherPermissions]

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

    def get_queryset(self):
        return Lecture.objects.filter(course=self.kwargs['course_pk'])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, TeacherPermissions | StudentPermissions]
        else:
            self.permission_classes = [IsAuthenticated, TeacherPermissions]
        return super().get_permissions()


class HometaskView(viewsets.ModelViewSet):
    serializer_class = HometaskSerializer

    def get_queryset(self):
        return Hometask.objects.filter(lecture=self.kwargs['lecture_pk'])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, TeacherPermissions | StudentPermissions]
        else:
            self.permission_classes = [IsAuthenticated, TeacherPermissions]
        return super().get_permissions()


class HomeworkView(viewsets.ModelViewSet):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        user = self.request.user
        if user.as_student.filter(id=course_id).exists():
            return Homework.objects.filter(hometask=self.kwargs['hometask_pk'], student=user)
        return Homework.objects.filter(hometask=self.kwargs['hometask_pk'])\
            .order_by(F('created').desc(nulls_first=True))

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, TeacherPermissions | StudentPermissions]
        elif self.action == 'mark':
            self.permission_classes = [IsAuthenticated, TeacherPermissions]
        else:
            self.permission_classes = [IsAuthenticated, StudentPermissions]
        return super().get_permissions()

    @action(detail=True, methods=['put', 'patch'], serializer_class=MarkSerializer)
    def mark(self, request, pk, **kwargs):
        return super().update(request, pk, **kwargs)


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(homework=self.kwargs['homework_pk'])

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, TeacherPermissions | StudentPermissions]
        else:
            self.permission_classes = [IsAuthenticated, IsOwnerOfComment]
        return super().get_permissions()
