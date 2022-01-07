from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=150, blank=True, null=True)
    created = models.DateTimeField(auto_now=True, editable=False)
    teachers = models.ManyToManyField(User, blank=True, related_name='as_teacher')
    students = models.ManyToManyField(User, blank=True, related_name='as_student')

    def __str__(self):
        return f'Course {self.name}'


class Lecture(models.Model):
    name = models.CharField(max_length=15)
    file = models.FileField()
    created = models.DateTimeField(auto_now=True, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'Lecture {self.name}'


class Hometask(models.Model):
    text = models.TextField()
    max_mark = models.PositiveIntegerField(default=10)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'Hometask {self.id}'


class Homework(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now=True, editable=False)
    mark = models.PositiveIntegerField(blank=True, null=True)
    hometask = models.ForeignKey(Hometask, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Homework {self.id}'


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now=True, editable=False)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id}'
