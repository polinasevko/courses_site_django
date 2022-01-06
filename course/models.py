from django.db import models
from django.contrib.auth.models import User


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
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return f'Hometask {self.id}'


class Homework(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now=True, editable=False)
    hometask = models.ForeignKey(Hometask, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    mark = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'Homework {self.id}'


# class Mark(models.Model):
#     mark = models.PositiveIntegerField(blank=True, null=True)
#     homework = models.OneToOneField(Homework, primary_key=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'Mark {self.mark}'


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now=True, editable=False)
    # mark = models.ForeignKey(Mark, to_field='homework', on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id}'
