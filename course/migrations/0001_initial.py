# Generated by Django 4.0 on 2022-01-09 09:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('students', models.ManyToManyField(blank=True, related_name='as_student', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(blank=True, related_name='as_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hometask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('max_mark', models.PositiveIntegerField(default=10)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('file', models.FileField(upload_to='')),
                ('created', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('created', models.DateTimeField(auto_now=True)),
                ('mark', models.PositiveIntegerField(blank=True, null=True)),
                ('hometask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.hometask')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='hometask',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.lecture'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.homework')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
