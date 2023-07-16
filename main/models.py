from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
class faculty_details(models.Model):
    idno = models.IntegerField(null=False, unique=True, blank=False, primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    timetable = ArrayField(ArrayField(models.CharField(max_length=30, null=False, blank=False), size=9))

    def __str__(self):
        return self.name


class faculty_details_even(models.Model):
    idno = models.IntegerField(null=False, unique=True, blank=False, primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    timetable = ArrayField(ArrayField(models.CharField(max_length=30, null=False, blank=False), size=9))

    def __str__(self):
        return self.name

class courseChampions(models.Model):
    courseCode = models.CharField(max_length=8, validators=[MinLengthValidator(8)], primary_key=True)
    courseName = models.CharField(max_length=100)
    champion = models.CharField(max_length=60)
    year = models.IntegerField(null=False, validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return self.courseName

class courseChampions_even(models.Model):
    courseCode = models.CharField(max_length=8, validators=[MinLengthValidator(8)], primary_key=True)
    courseName = models.CharField(max_length=100)
    champion = models.CharField(max_length=60)
    year = models.IntegerField(null=False, validators=[MaxValueValidator(4), MinValueValidator(1)])

    def __str__(self):
        return self.courseName