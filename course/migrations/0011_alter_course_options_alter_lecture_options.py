# Generated by Django 4.0 on 2021-12-29 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_lecture_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': (('teacher', 'As teacher'),)},
        ),
        migrations.AlterModelOptions(
            name='lecture',
            options={'permissions': (('teacher', 'As teacher'),)},
        ),
    ]