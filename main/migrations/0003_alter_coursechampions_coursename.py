# Generated by Django 4.1.1 on 2022-11-22 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_coursechampions_remove_faculty_details_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursechampions',
            name='courseName',
            field=models.CharField(max_length=100),
        ),
    ]
