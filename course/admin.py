from django.contrib import admin
from .models import Course, Lecture, Hometask, Homework, Comment


admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Hometask)
admin.site.register(Homework)
admin.site.register(Comment)
