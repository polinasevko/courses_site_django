# Generated by Django 4.0 on 2021-12-29 10:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0008_alter_course_students_alter_course_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='as_student', to=settings.AUTH_USER_MODEL),
        ),
    ]
