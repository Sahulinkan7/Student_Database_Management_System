# Generated by Django 4.2.5 on 2023-12-07 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_alter_attendance_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstaff',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='leavereportstudent',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
