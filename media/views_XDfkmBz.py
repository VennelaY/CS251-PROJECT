from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView,ListView,TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm,LoginForm,CourseCreateForm,AssignmentCreateForm,AssignmentSubmissionForm
from .forms import SetPasswordForm,ProfileUpdateForm
from .forms import PasswordResetForm
from .models import Course,User,Assignment,AssignmentSubmission
from django.contrib import messages
from django.http import Http404,HttpResponseRedirect
#from django.contrib.messages import constants 
from django.utils.decorators import method_decorator
from .decorators import user_is_student,user_is_instructor
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
'''
MESSAGE_TAGS = {
    messages.INFO: '',
    50: 'critical',
}
'''
#messages.add_message(request, messages.INFO, 'Hello world.')

def student(request):
    return render(request,'student.html')

def instructor(request):
    return render(request,'instructor.html')

class EditProfileView(UpdateView):
    model = User
    form_class = ProfileUpdateForm 
    success_url = reverse_lazy('users:login')
    '''
    if(user_is_instructor):
        context_object_name = 'instructor'
        success_url = reverse_lazy('users:login')
    if(user_is_student):
        context_object_name = 'student'
        success_url = reverse_lazy('users:student')
    '''
    template_name = 'edit_profile.html'
    
    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    @method_decorator(user_is_instructor or user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj

class CourseCreateView(SuccessMessageMixin,CreateView):
    template_name = 'course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('users:course')
    success_message="COURSE CREATED"

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and not self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 
'''
class join_course(request):
    model = User
    form_class = JoinCourseForm 
    success_url = reverse_lazy('users:login')
    if request.method == 'POST':
        form = JoinCourseForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            #return render(request, 'users/login.html', {'form': form})
            return redirect('users:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = JoinCourseForm(user)
    return render(request, 'joincourse.html', {'form': form})
'''
class CourseView(ListView):
    model = Course
    template_name = 'courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "view_course.html", {'course': course})

def login_view(request):
    if request.method == 'POST': 
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'student':
                login(request, user)
                #success_message="You have successfully login"
                #messages.success(request,"You have successfully login")
                return redirect('users:student')
            elif user is not None and user.role == 'instructor':
                login(request, user)
                #success_message="You have successfully login"
                #messages.success(request,"Your have successfully login")
                return redirect('users:instructor')
            else:
                #msg= 'invalid credentials'
                messages.error(request, "Error.invalid credentials")
                return redirect('users:login')
        else:
            print("Error.invalid credentials")
    else:
        print("Error.invalid credentials")
        form = LoginForm(request.POST)      
    return render(request, 'login.html', {'form': form})

def signup(request):
    msg = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            messages.success(request,"Your have successfully signup")
            return redirect('users:login')
        else:
            msg = 'form is not valid'
    else:
        form = SignupForm()
    return render(request,'signup.html', {'form': form, 'msg': msg})
'''    
def assignment_create(request):
       return render(request,'assignment_create.html')
'''
class AssignmentCreateView(SuccessMessageMixin,CreateView):
    template_name = 'assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('users:assignment-list')
    success_message="ASSIGNMENT CREATED"

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and not self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)   

class AssignmentView(ListView):
    model = Assignment
    template_name = 'assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')

class AssignmentSubmissionView(CreateView):
    template_name = 'assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('users:home')

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            #return render(request, 'users/login.html', {'form': form})
            return redirect('users:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})
'''
def password_reset_request(request):
    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )
'''

def passwordResetConfirm(request, uidb64, token):
    return redirect("home")
