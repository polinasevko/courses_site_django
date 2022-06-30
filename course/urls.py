from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter

from .views import (AddDeleteStudentView, AddTeacherView, CommentView,
                    CourseView, HometaskView, HomeworkView, LectureView)

course_router = SimpleRouter()
course_router.register(r'', CourseView, basename='course')
lecture_router = NestedSimpleRouter(course_router, r'', lookup='course')
lecture_router.register(r'lecture', LectureView, basename='lecture')
hometask_router = NestedSimpleRouter(lecture_router, r'lecture', lookup='lecture')
hometask_router.register(r'hometask', HometaskView, basename='hometask')
homework_router = NestedSimpleRouter(hometask_router, r'hometask', lookup='hometask')
homework_router.register(r'homework', HomeworkView, basename='homework')
comment_router = NestedSimpleRouter(homework_router, r'homework', lookup='homework')
comment_router.register(r'comment', CommentView, basename='comment')


urlpatterns = [
    path('<int:pk>/teachers/', AddTeacherView.as_view(), name='add-teacher'),
    path('<int:pk>/students/', AddDeleteStudentView.as_view(), name='add-delete-student'),
    path('', include(course_router.urls)),
    path('', include(lecture_router.urls)),
    path('', include(hometask_router.urls)),
    path('', include(homework_router.urls)),
    path('', include(comment_router.urls)),
]
