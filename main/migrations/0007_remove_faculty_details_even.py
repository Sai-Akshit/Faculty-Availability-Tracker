# Generated by Django 3.2.9 on 2023-01-09 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_faculty_details_even'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty_details',
            name='even',
        ),
    ]
