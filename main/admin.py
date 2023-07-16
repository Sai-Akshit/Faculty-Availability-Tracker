from django.contrib import admin
from .models import faculty_details, faculty_details_even, courseChampions, courseChampions_even

# Register your models here.
admin.site.register(faculty_details)
admin.site.register(faculty_details_even)
admin.site.register(courseChampions)
admin.site.register(courseChampions_even)
