from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms.models import ModelForm
from courses.models import Course

Student = "Student"
Instructor = "Instructor"

CHOICES =(
	(Student, "Student"),
	(Instructor, "Instructor")
)

class SignupForm(UserCreationForm):	#creating our custom registration form
	first_name = forms.CharField(required = True )
	email = forms.CharField(required=True)
	role = forms.ChoiceField(choices = CHOICES, required = True)

	class Meta:
		model = User
		fields = (
			'username',
		   'password1',
		   'password2',
		   'email',
		   'first_name',
		   'last_name',
		   'role'
		)

	def save(self, commit = True):
		user = super(SignupForm, self ).save(commit = False )
		user.first_name  = self.cleaned_data['first_name']
		user.last_name  = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.role = self.cleaned_data['role']
		if commit:
			user.save()
		return user
	
class ProfileChangeForm(UserChangeForm):
	class Meta:
		model = User
		fields = (
		'email',
		'first_name',
		'last_name',
		)


class Messageform(forms.Form):
    message = forms.CharField(
        widget= forms.Textarea(
            attrs={'style': 'border-color: orange;' 'width: 80%;' 'height: 400px' 'padding: 12px 20px;' 'border: 4px solid #ccc;' 'border-radius: 15px;' 'background-color: #f8f8f8;' 'font-size: 20px;' 'font-family: Verdana, Geneva, Tahoma, sans-serif;' }
        ),
        label='Message',
        required=True,
        max_length=300
    )
