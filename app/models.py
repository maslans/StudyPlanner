from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=200, verbose_name="University Name")

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=200, verbose_name="Field Of Study")
    university = models.ForeignKey(
        University, 
        on_delete=models.CASCADE, 
        related_name="fieldOfStudy"
    )

    def __str__(self):
        return f"{self.name}"
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="School")
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Field Of Study")
    birthdate = models.DateField(null=False, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.field_of_study}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
    
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name subject", unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=False,
        verbose_name="Subject"
    )

    TASK_TYPE_CHOICES = [
        ('TASK', 'TASK'),
        ('EXAM', 'EXAM'),
        ('TEST', 'TEST'),
        ]
    
    type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        null=False
    )

    title = models.CharField(max_length=200, null=False, verbose_name="Title")
    description = models.TextField(verbose_name="Description", blank=True)
    due_date = models.DateField(null=True, blank=False, verbose_name="Term")

    is_done = models.BooleanField(default=False, verbose_name="Is Done")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"
        
    @property
    def days_left(self):
        if self.due_date:
            delta = (self.due_date - date.today()).days
            return max(delta, 0)  # Zwraca 0, jeśli data już minęła
        return None  # Brak terminu