from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
#from .managers import UserManager
from .decorators import validate_file

# CUSTOM USER MODEL


class Course(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='media')
    teacher_name = models.CharField(max_length=50)
    teacher_details = models.TextField()
    course_description = models.TextField()
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.course_name  
         
class User(AbstractUser):
    student='student'
    instructor='instructor'
    select='SELECT'
    ROLE = [

        (instructor,'instructor') ,
        (student,'student')
    ]
    courses = models.ManyToManyField(Course)
    #arr=ArrayField(base_field=models.CharField(max_length=10,null=True),default=list,blank=True)
    role=models.CharField(choices = ROLE,max_length=32)
    #is_student=models.BooleanField('Is student',default=False)
    #is_instructor=models.BooleanField('Is instrucctor',default=False)

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=100)
    question_content = models.TextField()
    assignment_marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    related_file=models.FileField(upload_to='file1/', null=True, blank=True, validators=[validate_file])
    #created_at = models.DateField(default=timezone.now)
    code = models.CharField(max_length=100,default='00000')
    def __str__(self):
        return self.assignment_name

class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    no = models.IntegerField(default=0)
    file = models.FileField(upload_to='file/', null=True, blank=False, verbose_name="", validators=[validate_file])

    def _str_(self):
        return self.name
        
class GradeAssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    feedback = models.TextField(null=True, blank=True)
    NO = models.IntegerField(default=0)
  #  file = models.FileField(upload_to='file/', null=True, blank=False, verbose_name="", validators=[validate_file])

    def _str_(self):
        return self.name        
	