from django.contrib import admin
from .models import StudentProfile, Task, Subject, University, FieldOfStudy, Message

# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(Task)
admin.site.register(Subject)
admin.site.register(University)
admin.site.register(FieldOfStudy)
admin.site.register(Message)