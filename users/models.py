from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
#from .managers import UserManager
from .decorators import valid,valid1,validate_file

# CUSTOM USER MODEL
class FileModel(models.Model):
    file = models.FileField(upload_to='f', default='')
    created = models.DateTimeField(auto_now=True)

class Course(models.Model):
    """The class Course is model for every course with following contents.\n 
    | def _str_(self) 
    | It has no member functions\n
    :param course_name: any string
    :param course_code: used for registering course by student
    :param course_image: to upload image 
    :param teacher_name: CharField
    :param teacher_details: Some text about teacher visible on course page
    :param course_description: Some text about teacher visible on course page
    """
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
    """The class User is model for specific user \n
    :param student: for student
    :param instructor: for instructor
    :param ROLE: dictionary for 2 roles(student,instructor)
    :courses: here user model needs to reference multiple instances of another model course 
    :role: for selecting role either as student/instructor
    """
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
    """The class Assignment is model for specific assignment.\n
    | def _str_(self) 
    | It has no member functions\n
    :param user: It is Forein Key
    :param assignment_name: CharField for title of Assignment
    :param question_content: Just TextField 
    :param extensions: Just textField for extensions
    :param assignment_marks: max marks
    :param deadline: for deadline
    :param related_file: upload file for question
    :param autograde_script_name: name of script
    :param autograde_script_zipfile: upload file for autograde
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_name = models.CharField(max_length=100)
    question_content = models.TextField()
    extensions = models.TextField(default='00000')
    assignment_marks = models.IntegerField(default=0)
    deadline = models.DateTimeField(blank=False)
    related_file=models.FileField(upload_to='file1/', null=True, blank=True)
    file_directory_structure_textfile=models.FileField(upload_to='file1/', null=True, blank=True, validators=[valid])
    autograde_script_name=models.CharField(max_length=100,default='00000')
    autograde_script_zipfile = models.FileField(upload_to='file1/', null=True, blank=True, validators=[valid1])
    #created_at = models.DateField(default=timezone.now)
    code = models.CharField(max_length=100,default='00000')
    def __str__(self):
        return self.assignment_name

class AssignmentSubmission(models.Model):
    """The class AssignmentSubmission is model for specific assignment submission.\n
    :param user: It is Forein Key
    :param name: CharField for title of Assignment which is usernname
    :param content: Just TextField 
    :param no: IntegerId for assignment ID
    :param grade: To store grade
    :param feedback: To store feedback
    :param file: user upload answer file for assignment
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    no = models.IntegerField(default=0)
    grade=models.FloatField(default=-1)
    feedback=models.TextField(null=True, blank=True,default="THIS IS MANUALLY GRADED")
    format=models.BooleanField(default=True)
    file = models.FileField(upload_to='file/', null=True, blank=False)
    def _str_(self):
        return self.name
        
class GradeAssignmentSubmission(models.Model):
    """The class GradeAssignmentSubmission is model for providing grade for a specific assignment submission.\n
    :param marks: IntegerField for providing marks for assignment submitted
    :param feedback: Just TextField to give any comments about submission
    :param NO: IntegerId for assignment ID
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    feedback = models.TextField(null=True, blank=True)
    NO = models.IntegerField(default=0)
    
    def _str_(self):
        return self.name        
	
