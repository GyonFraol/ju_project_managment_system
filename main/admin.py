from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Department)
admin.site.register(SchoolYear)
admin.site.register(StudentProfile)
admin.site.register(Stream)
admin.site.register(Comment)
admin.site.register(Project)
