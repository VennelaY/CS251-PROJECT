from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView,ListView,TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import *
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

    """This view function takes a Web request and returns a Web response.(which is redirect)
    :param request: its a request for redirecting to student home page 
    :type request: HttpRequest object
    :return: redirect to student home page
    :rtype: HttpRequest object
    """
    return render(request,'student.html')

def instructor(request):
    """This view function takes a Web request and returns a Web response.(which is redirect)
    :param request: its a request for redirecting to instructor home page 
    :type request: HttpRequest object
    :return: redirect to instructor home page
    :rtype: HttpRequest object
    """
    return render(request,'instructor.html')

    
class EditProfileView(UpdateView):
    """This class is used for user model to edit their profile by filling form ProfileUpdateForm and 
    after successfully changing it redirects to login page
    :param form_calss:form for updating profile(ProfileUpdateForm)
    :param success_url:redirects to this url after successfullly changing
    :param template_name:corresponding html page
    """
    model = User
    form_class = ProfileUpdateForm 
    success_url = reverse_lazy('users:login')
    template_name = 'edit_profile.html'
    
    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
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
    """This class is used for user model to create course by filling form CourseCreateForm and 
    after successfully creating it redirects to view-courses page
    :param form_calss:form for creating course(CourseCreateForm)
    :param success_url:redirects to this url after successfullly changing
    :param template_name:corresponding html page
    """
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
        form.instance.teacher_name=self.request.user.first_name
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form) 

def join_course(request):
    """This view function takes a Web request and returns a Web response.(which is redirect) along with form
    Also get course corresponding to code ubtained from JoinCourseForm and add that course to corresponding user(student0)
    :param request: its a request for redirecting to joincourse with JoinCourseForm
    :type request: HttpRequest object
    :return: redirect to joincourse
    :rtype: HttpRequest object 
    """
    if request.method == 'POST':
        form = JoinCourseForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data.get('code')
            c1 = Course.objects.all().filter(course_code = join_code).count()
            if c1!=0:
                c = Course.objects.get(course_code = join_code)
                request.user.courses.add(c)
                request.user.save()
                return redirect('users:course')
    form = JoinCourseForm()
    return render(request, 'joincourse.html', {'form': form})

class AvailableCourseView(ListView):
    """This class is used for Course model to show available courses present 
    after successfully creating it redirects to view-courses page
    :param context_object_name:
    :param template_name:corresponding html page
    """
    model = Course
    template_name = 'available_courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

class CourseView(ListView):
    """This class is used for Course model to show users their courses which were already joined through code
    :param context_object_name:
    :param template_name:corresponding html page to show courses
    """
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
    """This function is used to show all courses in view-courses page
    """
    course = get_object_or_404(Course, id=id)
    return render(request, "view_course.html", {'course': course})

def login_view(request):
    """This function is used for user to login by authentication i.e
    If LoginForm is valid then from obtained username and password in LoginForm it searches for user through authentication
    and then according to role of user obtained it logins and redirects to student page/instructor page
    if form is invalid then it again redirects to same page
    """
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
                #messages.error(request, "Error.invalid credentials")
                return redirect('users:login')
                #print("Error.invalid credentials")
    else:
        #print("Error.invalid credentials")
        form = LoginForm(request.POST)      
    return render(request, 'login.html', {'form': form})

def signup(request):
    """This function is used for user to signup by filling form SignupForm i.e 
    First sends a request to form SignupForm and If Form is valid then saves form i.e saves user eith all information provided
    if form is invalid(like if any field is missing/already exists/invalid input in any field) then it again redirects to same page
    """
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

class AssignmentCreateView(SuccessMessageMixin,CreateView):
    """This class is used for user model to create assignment by filling form AssignmentCreateForm and 
    after successfully creating it redirects to view-courses page with a sucess message
    :param form_calss:form for creating assignment(AssignmentCreateForm)
    :param success_url:redirects to this url after successfullly changing
    :param template_name:corresponding html page
    """
    template_name = 'assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    
    success_url = reverse_lazy('users:course')
    success_message="ASSIGNMENT CREATED"

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        """This function checks if user is authenticates and user is instructor 
        else it redirects to login page
        """
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and not self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        #success_url = reverse_lazy('users:assignment-list', kwargs['id'])  
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        """This function fills feilds which are not obtained from form like 
        user model:this present authenticated user and 
        code:first get course with corresponding assignment id and return course_code of corresponding course
        """
        e = Course.objects.get(id=self.kwargs['id'])
        form.instance.user = self.request.user
        form.instance.code = e.course_code       
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()        	
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)       


class AssignmentView(ListView):
    """This class is used for Assignment model to show users assignments in a particular course  which were created by instructor
    :param context_object_name:
    :param template_name:corresponding html page to show assignments
    """
    model = Assignment
    template_name = 'assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        """This function is used to show assignments under a particular course which are created corre 
        """
        e = Course.objects.get(id=self.kwargs['id'])        
        a = self.model.objects.all().filter(code = e.course_code)
        return a  # filter(user_id=self.request.user.id).order_by('-id')

class AssignmentSubmissionView(CreateView):
    """This class is used for user(student) to do submission for a particular assignments in a particular course  which were created by instructor
    by filling form AssignmentSubmissionForm i.e uploading answers in that form
    :form_class=form to be filled for submitting assigment
    :param template_name:corresponding html page to show assignments
    :success_url=after successfully submitting form redirects to view course page
    """
    template_name = 'assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('users:course')

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        e = Assignment.objects.get(id=self.kwargs['id'])
        e1 = AssignmentSubmission.objects.all().filter(no = e.id)
        for x in e1:
            if x.user==self.request.user:
                y = Course.objects.get(course_code = e.code)   
                return redirect('users:assignment-list',y.id)    
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        e = Assignment.objects.get(id=self.kwargs['id'])
        form.instance.user = self.request.user
        form.instance.no = e.id 
        form.instance.name=self.request.user.username        
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GradeAssignmentSubmissionView(CreateView):
    """This class is used for user(instructor) to do gradesubmission for a particular assignmentsubmission by student for a particular assignment in a particular course  which were created by instructor
    by filling form GradeAssignmentSubmissionForm i.e uploading grade in that form
    :form_class=form to be filled for submitting grade
    :param template_name:corresponding html page to show grades
    :success_url=after successfully submitting form redirects to view course page
    """
    template_name = 'gradeassignment_submission.html'
    form_class = GradeAssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('users:course')

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        """This function searches for assignmentsubmission object with id and 
        then submitted grades under that assignment
        """
        e = AssignmentSubmission.objects.get(id = self.kwargs['id'])
        e1 = GradeAssignmentSubmission.objects.all().filter(NO = e.id)
        for x in e1:
            if x.user==self.request.user:
                y = Assignment.objects.get(id = e.no)
                return redirect('users:assignment-submission-list',y.id)         
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and self.request.user.role=='student':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        e = AssignmentSubmission.objects.get(id=self.kwargs['id'])
        form.instance.user = self.request.user
        form.instance.NO = e.id     
        return super(GradeAssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AssignmentSubmissionListView(ListView):
    """This class is used for Assignment model to show users(instructors) submitted  assignments by students for a particular assignment created in a particular course  which were created by instructor
    :param context_object_name:
    :param template_name:corresponding html page to show assignments
    """
    model = AssignmentSubmission
    template_name = 'assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        """This function first searches for assignment with assignment id(which is unique) and 
        Then searches for submissions which are made under this assignment(by searching with assignment id)
        """
        e = Assignment.objects.get(id=self.kwargs['id'])        
        a = self.model.objects.all().filter(no = e.id) 
        return a  
        
class AssignmentSubmissionGradeListView(ListView):
    model = GradeAssignmentSubmission
    template_name = 'gradeassignment_submission_list.html'
    context_object_name = 'gradeassignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        e = AssignmentSubmission.objects.all().filter(no=self.kwargs['id']) 
        e2= e.all().filter(user=self.request.user).count()
        if e2==0:
              return redirect('users:course')
        e1 = e.get(user=self.request.user)
        a = self.model.objects.all().filter(NO = e1.id) 
        a1= self.model.objects.all().filter(NO = e1.id).count()
        if a1==0:
            return redirect('users:course')
        else:
            return a 
        

@login_required
def password_change(request):
    """This function is used for user to change their password by filling form SetPasswordForm
    If form is valid then it saves form i.e updates profile and after successfully changing 
    redirects to login page
    """
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, "Your password has been changed")
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

def passwordResetConfirm(request, uidb64, token):
    return redirect("home")
'''