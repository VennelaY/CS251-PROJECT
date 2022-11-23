from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from .models import User,Course,Assignment,AssignmentSubmission
#from .models import Assignment
from django.contrib.auth.forms import PasswordResetForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','role')
    ''' 
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
    '''
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['name', 'content', 'file']

    def _init_(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self)._init_(*args, **kwargs)
        self.fields['name'].label = " Name"
        self.fields['content'].label = "Answer"
        self.fields['file'].label = "Or Upload File"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Write Your Answer Here',
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

class ProfileUpdateForm(forms.ModelForm):

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
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
        
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
        

class PasswordResetForm(PasswordResetForm):
    def _init_(self, *args, **kwargs):
        super(PasswordResetForm, self)._init_(*args, **kwargs)
      
class JoinCourseForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CODE'}),
        label="CODE")
   
class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_image','course_code', 'teacher_name', 'teacher_details', 'course_description']

    def __init__(self, *args, **kwargs):
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        self.fields['course_image'].label = "Image"
        self.fields['course_code'].label = "Course Code"
        self.fields['teacher_name'].label = "Instructor Name"
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

        self.fields['teacher_name'].widget.attrs.update(
            {
                'placeholder': 'Instructor Name',
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
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'marks', 'duration']

    def _init_(self, *args, **kwargs):
        super(AssignmentCreateForm, self)._init_(*args, **kwargs)
        self.fields['title'].label = "Assignment Name"
        self.fields['content'].label = "Content"
        self.fields['marks'].label = "Marks"
        self.fields['duration'].label = "Duration"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter A Name',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Content',
            }
        )

        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks',
            }
        )

        self.fields['duration'].widget.attrs.update(
            {
                'placeholder': '3 hour, 2 hour etc ...',
            }
        )

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course
