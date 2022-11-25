from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from .models import User,Course,Assignment,AssignmentSubmission,GradeAssignmentSubmission
#from .models import Assignment
from django.contrib.auth.forms import PasswordResetForm

class SignupForm(UserCreationForm):
    """The class SignUpForm is form for user(student/instructor) to signup
    :param first_name: CharField for user firstname 
    :param last_name: CharField for user lastname
    :param email: Emailfield for user email 
    """
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','role')

class AssignmentSubmissionForm(forms.ModelForm):
    """The class AssignmentSubmissionForm is form for user(student) to submit assignment 
    The feilds to be present in the form are:
    file:to submit answer file by user
    comment:write if there are any comments
    | It has constructor with 2 parameter 
    | def _init_(self, *args, **kwargs) 
    Just creates form with mentioned labels and placeholders
    | def is_valid(self)
    | checks if form is valid if valid then return that created assignment
    | def save(self, commit=True)
    | saves form i.e saves assignmentsubmission
    """
    class Meta:
        model = AssignmentSubmission
        fields = ['content', 'file']

    def _init_(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self)._init_(*args, **kwargs)
     
        self.fields['file'].label = "Or Upload File"
        self.fields['content'].label = "Comment"

      

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Write Your Comment Here',
            }
        )

        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )
    def is_valid(self):
        valid = super(AssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentSubmissionForm, self).save(commit=False)
        if commit:
            course.save()
        return course
        
class GradeAssignmentSubmissionForm(forms.ModelForm):
    """The class GradeAssignmentSubmissionForm is form for user(instructor) to submit grade for a paticular assignment assignment 
    The feilds to be present in the form are:
    'marks', 'feedback'
    | It has constructor with 2 parameter 
    | def _init_(self, *args, **kwargs) 
    Just creates form with mentioned labels and placeholders
    | def is_valid(self)
    | checks if form is valid if valid then return that created gradeassignment
    | def save(self, commit=True)
    | saves form i.e saves gradeassignmentsubmission
    """
    class Meta:
        model = GradeAssignmentSubmission
        fields = ['marks', 'feedback']

    def _init_(self, *args, **kwargs):
        super(GradeAssignmentSubmissionForm, self)._init_(*args, **kwargs)
        self.fields['marks'].label = "marks"
        self.fields['feedback'].label = "Feedback"
        #self.fields['file'].label = "Or Upload File"

        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks Obtained',
            }
        )

        self.fields['feedback'].widget.attrs.update(
            {
                'placeholder': 'Write Your Feedback Here',
            }
        )
        '''
        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )
        '''
    def is_valid(self):
        valid = super(GradeAssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(GradeAssignmentSubmissionForm, self).save(commit=False)
        if commit:
            course.save()
        return course
        

class ProfileUpdateForm(forms.ModelForm):
    """The class ProfileUpdateForm is form for user(student/instructor) to update its profile 
    The feilds to be present in the form are:
    firstname,lastname,email
    | It has constructor with 2 parameter 
    | def _init_(self, *args, **kwargs) 
    Just creates form with mentioned labels and placeholders
    """

    def _init_(self, *args, **kwargs):
        super(ProfileUpdateForm, self)._init_(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]    

class LoginForm(forms.Form):
    """The class LoginForm is form for user(student/instructor) to login with username and password 
    The feilds to be present in the form are:
    'username', 'password'
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
        
class SetPasswordForm(SetPasswordForm):
    """The class SetPasswordForm is form for user to reset their password
    The feilds to be present in the form are:
    'new_password1', 'new_password2'
    """
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        
'''
class PasswordResetForm(PasswordResetForm):
 
    def _init_(self, *args, **kwargs):
        super(PasswordResetForm, self)._init_(*args, **kwargs)
'''      
class JoinCourseForm(forms.Form):
    """The class JoinCourseForm is form for student to register for any course through course code
    The feilds to be present in the form are:
    'code'
    """
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CODE'}),
        label="CODE")
   
class CourseCreateForm(forms.ModelForm):
    """The class CourseCreateForm is form for instructor to create course.
    The feilds to be present in the form are:
    'course_name', 'course_image','course_code', 'teacher_details', 'course_description'
    | It has constructor with 2 parameter 
    | def _init_(self, *args, **kwargs) 
    Just creates form with mentioned labels and placeholders
    | def is_valid(self)
    | checks if form is valid if valid then return that created course
    | def save(self, commit=True)
    | saves form i.e saves course
    """
    class Meta:
        model = Course
        fields = ['course_name', 'course_image','course_code',  'teacher_details', 'course_description']

    def __init__(self, *args, **kwargs):
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        self.fields['course_image'].label = "Image"
        self.fields['course_code'].label = "Course Code"
        #self.fields['teacher_name'].label = "Instructor Name"
        self.fields['teacher_details'].label = "Instructor Details"
        self.fields['course_description'].label = "Description"
        
        #self.fields['end_date'].label = "End Date"
        
        

        self.fields['course_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Course Name',
            }
        )

        self.fields['course_image'].widget.attrs.update(
            {
                'placeholder': 'Image',
            }
        )
        self.fields['course_code'].widget.attrs.update(
            {
                'placeholder': 'Couse Code',
            }
        )

        self.fields['teacher_details'].widget.attrs.update(
            {
                'placeholder': 'Instructor Details',
            }
        )

        self.fields['course_description'].widget.attrs.update(
            {
                'placeholder': 'Description',
            }
        )

    def is_valid(self):
        valid = super(CourseCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(CourseCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course

class AssignmentCreateForm(forms.ModelForm):
    """The class AssignmentCreateForm is form for instructor to create assignment.
    The feilds to be present in the form are:
    'assignment_name', 'question_content', 'related_file', 'assignment_marks', 'duration'
    | It has constructor with 2 parameter 
    | def _init_(self, *args, **kwargs) 
    Just creates form with mentioned labels and placeholders
    | def is_valid(self)
    | checks if form is valid if valid then return that created assignment
    | def save(self, commit=True)
    | saves form i.e saves assignment
    """
    class Meta:
        model = Assignment
        fields = ['assignment_name', 'question_content','extensions', 'related_file', 'assignment_marks', 'deadline','file_directory_structure_textfile','autograde_script_zipfile']

    def _init_(self, *args, **kwargs):
        super(AssignmentCreateForm, self)._init_(*args, **kwargs)
        

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        assignment = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            assignment.save()
        return assignment
