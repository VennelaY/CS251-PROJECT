import zipfile
import shutil
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView,ListView,TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import Course,User,Assignment,AssignmentSubmission,FileModel
from django.contrib import messages
from django.http import Http404,HttpResponseRedirect
#from django.contrib.messages import constants 
from django.utils.decorators import method_decorator
from .decorators import user_is_student,user_is_instructor
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
#from .decorators import validate_file
from subprocess import check_output
from django.utils import timezone
#from zipfile import Zipfile
#from blog.functions.functions import handle_uploaded_files
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
    after successfully changing it redirects to login page \n
    :param form_calss: form for updating profile(ProfileUpdateForm)
    :param success_url: redirects to this url after successfullly changing
    :param template_name: corresponding html page
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
    after successfully creating it redirects to view-courses page\n
    :param form_calss: form for creating course(CourseCreateForm)
    :param success_url: redirects to this url after successfullly changing
    :param template_name: corresponding html page
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
    Also get course corresponding to code ubtained from JoinCourseForm and add that course to corresponding user(student0)\n
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
    after successfully creating it redirects to view-courses page\n
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
    """This class is used for Course model to show users their courses which were already joined through code\n
    :param context_object_name:
    :param template_name: corresponding html page to show courses
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
            #messages.success(request,"Your have successfully signup")
            return redirect('users:login')
        else:
            msg = 'form is not valid'
    else:
        form = SignupForm()
    return render(request,'signup.html', {'form': form, 'msg': msg})

class AssignmentCreateView(SuccessMessageMixin,CreateView):
    """This class is used for user model to create assignment by filling form AssignmentCreateForm and\n 
    after successfully creating it redirects to view-courses page with a sucess message\n
    :param form_calss: form for creating assignment(AssignmentCreateForm)
    :param success_url: redirects to this url after successfullly changing
    :param template_name: corresponding html page
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

    def form_valid(self, form,request):
        """This function fills feilds which are not obtained from form like 
        user model: this present authenticated user and 
        code: first get course with corresponding assignment id and return course_code of corresponding course
        """
        e = Course.objects.get(id=self.kwargs['id'])
        form.instance.user = self.request.user
        form.instance.code = e.course_code
        file_model = FileModel()
        _, file = request.FILES.popitem()  # get first element of the uploaded files
        file = file[0]  # get the file from MultiValueDict
        #print(file.name)
        file_model.file = file
        file_model.save()
        #f1=e.file_directory_structure_textfile.name
        f='users/media/f/'+form.instance.autograde_script_zipfile.name
        y=form.instance.autograde_script_zipfile.name.split(".",1)[0]
        print(y)
        #out = check_output(["",b, f]s)
        with zipfile.ZipFile(f,'r') as zipObj:
            filelist=zipObj.namelist()
            for x in filelist:
                #print(type(x))
                if x.endswith('.py') or x.endswith('.sh'):
                    print(x)
                    form.instance.autograde_script_name=x
                    break
            zipObj.extractall("users/media/f/")

        #raise HttpResponse("fgjhk")           
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()        	
        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form)       


class AssignmentView(ListView):
    """This class is used for Assignment model to show users assignments in a particular course  which were created by instructor \n
    :param context_object_name:
    :param template_name: corresponding html page to show assignments
    """
    model = Assignment
    #template_name = 'assignments.html'
    context_object_name = 'assignment'
    #context_object_name2 = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        """This function is used to show assignments under a particular course which are created corre 
        """
        e = Course.objects.get(id=self.kwargs['id'])        
        a = self.model.objects.all().filter(code = e.course_code)
        b = AssignmentSubmission.objects.all()
        return render(request, 'assignments.html', {'assignment':a, 'assignment_submission':b, 'course':e})
        #return a  # filter(user_id=self.request.user.id).order_by('-id')

class ReAssignmentSubmissionView(CreateView):
    """This class is used for user(student) to do resubmission for a particular assignmens in a particular course \n  
    which were created by instructor by filling form AssignmentSubmissionForm i.e uploading answers in that form \n
    :param form_class: form to be filled for resubmitting assigment
    :param template_name: corresponding html page to show assignmentsubmission
    :param success_message: a meassage of success
    :param success_url: after successfully submitting form redirects to previous page(i.e assignments list page)
    """
    template_name = 'assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_meassage="YOU HAVE SUCCESSFULLY UPDATED YOUR ASSIGNMENT"
    success_url = reverse_lazy('users:course')
    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        """
        This function is used to validate form  i.e if user is not authenticated or not a student then asks him to login again 
        i.e allows only student to submit assignment.
        Also If deadline is passed then gives error and again redirects to same page when he tries to submit assignment
        If neither of this is true then allows to fill a form then again validate file extensions and validate file directory structure
        Then for autograde_script is also similar for assignmentsubmission case
        """
        e = Assignment.objects.get(id=self.kwargs['id'])
        e1 = AssignmentSubmission.objects.all().filter(no = e.id)
        for x1 in e1:
            if e.deadline < timezone.now():
                y = Course.objects.get(course_code = e.code)
                messages.error(request,"* FOR ASSIGNMENT "+ e.assignment_name + " DEADLINE IS UP *")
                return redirect('users:assignment-list',y.id)
            if x1.user==self.request.user:
                y1 = Course.objects.get(course_code = e.code)
                form=self.get_form()
                if form.is_valid():
                    e = Assignment.objects.get(id=self.kwargs['id'])
                    form.instance.user = self.request.user
                    form.instance.no = e.id
                    form.instance.name=self.request.user.username
                    x = e.extensions.split(",")
                    ext = form.instance.file.name.split(".",1)[1]
                    ext="."+ext
                    valid_extensions = e.extensions.split(",") #e.extensions
                
                    #valid_extensions=['.py','.zip','.gz','.tgz','.cpp','.pdf']
                    if not ext in valid_extensions:
                        messages.error(request,"ERROR IN File Extension")
                        return redirect('users:reassignment_submission',e.id)
                    file_model = FileModel()
                    _, file = request.FILES.popitem()  # get first element of the uploaded files
                    file = file[0]  # get the file from MultiValueDict

                    file_model.file = file
                    file_model.save()
                    if ext in ['.tgz', '.tar', '.tar.gz']:
                        a='tar'
                        b='-tf'
                    elif ext in ['.zip']:
                        a='zipinfo'
                        b='-1'
                    else:
                        messages.success(request,"FILE SUCCESSFULLY SUBMITTED")
                        return redirect('users:reassignment_submission',e.id)
                    f1=e.file_directory_structure_textfile.name
                    out = check_output([a,b, 'users/media/f/'+form.instance.file.name])  
                    with open('out.txt','w') as f:
                        f.write(out.decode())
                    with open('out.txt','r') as g:
                        for word in g:
                            first_word=word
                            break
                    with open('users/media/'+f1,'r') as e1:
                        for word in e1:
                            second_word=word.replace('\n','')
                            break
                    fin = open("out.txt", "rt")
                    fout = open("out1.txt", "wt")
                    for word in fin:
                        s1=word.split("/",1)
                        if len(s1)<2:
                            messages.error(request,"ERROR IN File Directory Structure")
                            return self.form_invalid(form)
                        s=second_word+s1[1]
                        #print(s)
                        fout.write(word.replace(word,s))
                    #close input and output files
                    fin.close()
                    fout.close()
                    with open('users/media/'+f1,'r') as firstfile:
                        data1=firstfile.read()
                    with open('out1.txt','r') as secondfile:
                        data2=secondfile.read()
                    if (data1==data2):
                        #messages.success(request,"YOU HAVE SUCCESSFULLY SUBMITTED YOUR ASSIGNMENT")    
                        #return super(AssignmentSubmissionView, self).form_valid(form)
                        y=e.autograde_script_zipfile.name.split(".",1)[0]
                        z=e.autograde_script_name
                        z1=z.split(".",1)
                        ext1 = form.instance.file.name.split(".",1)[0]
                        if(z=='00000' or len(z1)<2):
                            form.instance.feedback='Autograding Did not Work, Something is wrong'
                        elif(z1[1]=="sh"):
                            shutil.move("users/media/f/"+form.instance.file.name,form.instance.file.name)   
                            out1=check_output(['bash', 'users/media/f/'+z, self.request.user.username])
                            form.instance.feedback=out1.decode()
                            check_output(['rm',form.instance.file.name]) 
                        x1.content=form.instance.content
                        x1.file=form.instance.file
                        x1.feedback=form.instance.feedback
                        x1.save()
                        messages.success(request,"SUCCESSFULLY YOUR SUBMISSION IS UPDATED")    	              
                        return redirect('users:assignment-list',y1.id)
                    else:
                        #form.instance.format=False
                        messages.error(request,"ERROR IN File Directory Structure")
                        return redirect('users:reassignment_submission',e.id)
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)


class AssignmentSubmissionView(CreateView):
    """This class is used for user(student) to do submission for a particular assignments in a particular course  which were created by instructor
    by filling form AssignmentSubmissionForm i.e uploading answers in that form \n
    :param form_class: form to be filled for submitting assigment
    :param template_name: corresponding html page to show assignments
    :param success_message: a meassage of success
    :param success_url: after successfully submitting form redirects to view course page
    """
    template_name = 'assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_meassge="YOU HAVE SUCCESSFULLY SUBMITTED YOUR ASSIGNMENT "
    success_url = reverse_lazy('users:course')

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        """
        This function is called before form i.e if user is not authenticated or not a student then asks him to login again 
        i.e allows only student to submit assignment.
        Also If deadline is passed then gives error and again redirects to same page when he tries to submit assignment
        """
        e = Assignment.objects.get(id=self.kwargs['id'])
        e1 = AssignmentSubmission.objects.all().filter(no = e.id)
        if e.deadline < timezone.now():
            y = Course.objects.get(course_code = e.code)
            messages.error(request,"* FOR ASSIGNMENT "+ e.assignment_name + " DEADLINE IS UP *")
            return redirect('users:assignment-list',y.id)
        for x in e1:
            if x.user==self.request.user:
                y = Course.objects.get(course_code = e.code) 
                return redirect('users:assignment-list',y.id)    
        if not self.request.user.is_authenticated:
            return reverse_lazy('users:login')
        if self.request.user.is_authenticated and self.request.user.role=='instructor':
            return reverse_lazy('users:login')
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form,request):
        """
        To check if form is valid or not like first check if file extension is one of the extensions given by instructor if not
        form becomes inavalid and asks again to fill form Also verifies file directory structure with the one given by instructor 
        if not match then also form is invalid.This function also includes autograder part like runs command according to that given 
        in autograder_script with file he submitted and test it which will give marks also then stored that feedback.
        Also if form is valid then save that form i.e submission to list of assignment submissions
        """
        e = Assignment.objects.get(id=self.kwargs['id'])
        form.instance.user = self.request.user
        form.instance.no = e.id
        form.instance.name=self.request.user.username
        x = e.extensions.split(",")
        import os
        ext = form.instance.file.name.split(".",1)[1]
        ext="."+ext
        valid_extensions = e.extensions.split(",") #e.extensions
    
        #valid_extensions=['.py','.zip','.gz','.tgz','.cpp','.pdf']
        if not ext in valid_extensions:
            messages.error(request,"ERROR IN File Extension")
            return self.form_invalid(form)
        file_model = FileModel()
        _, file = request.FILES.popitem()  # get first element of the uploaded files
        file = file[0]  # get the file from MultiValueDict

        file_model.file = file
        file_model.save()
        if ext in ['.tgz', '.tar', '.tar.gz']:
            a1='tar'
            b1='-tf'
        elif ext in ['.zip']:
            a1='zipinfo'
            b1='-1'
        else:
            messages.success(request,"FILE SUCCESSFULLY SUBMITTED")
            return super(AssignmentSubmissionView, self).form_valid(form)
        f1=e.file_directory_structure_textfile.name
        out = check_output([a1,b1, 'users/media/f/'+form.instance.file.name]) 
        with open('out.txt','w') as f:
            f.write(out.decode())
        with open('out.txt','r') as g:
            for word in g:
                first_word=word
                break
        with open('users/media/'+f1,'r') as e1:
            for word in e1:
                second_word=word.replace('\n','')
                break
        fin = open("out.txt", "rt")
        fout = open("out1.txt", "wt")
        for word in fin:
            s1=word.split("/",1)
            if len(s1)<2:
                 messages.error(request,"ERROR IN File Directory Structure")
                 return self.form_invalid(form)
            s=second_word+s1[1]
            fout.write(word.replace(word,s))
        #close input and output files
        fin.close()
        fout.close()
        with open('users/media/'+f1,'r') as firstfile:
            data1=firstfile.read()
        with open('out1.txt','r') as secondfile:
            data2=secondfile.read()
        if (data1==data2):
            #messages.success(request,"YOU HAVE SUCCESSFULLY SUBMITTED YOUR ASSIGNMENT")    
            #return super(AssignmentSubmissionView, self).form_valid(form)
            y=e.autograde_script_zipfile.name.split(".",1)[0]
            z=e.autograde_script_name
            z1=z.split(".",1)
            ext1 = form.instance.file.name.split(".",1)[0]
            if(z=='00000' or len(z1)<2):
                form.instance.feedback='Autograding Did not Work, Something is wrong'
                return super(AssignmentSubmissionView, self).form_valid(form)
            if(z1[1]=="sh"):
                shutil.move("users/media/f/"+form.instance.file.name,form.instance.file.name)   
                out1=check_output(['bash', 'users/media/f/'+z, self.request.user.username])
                form.instance.feedback=out1.decode()
                check_output(['rm',form.instance.file.name])                  
            return super(AssignmentSubmissionView, self).form_valid(form)
        else:
            form.instance.format=False
            messages.error(request,"ERROR IN File Directory Structure")
            return self.form_invalid(form)            

    def post(self, request, *args, **kwargs):
        """
        checks if form valid/not if invalid (like not filling up fields/mismatch of filed) then return error
        if it becomes valid for this then checks for further checkings and then also if it is valid then 
        sends to list AssignmentSubmissionView
        """
        self.object = None
        form = self.get_form()
        if form.is_valid():    
            return self.form_valid(form,request)
        else:
            messages.error(request,"FORM INVALID")
            return self.form_invalid(form)




class GradeAssignmentSubmissionView(CreateView):
    """This class is used for user(instructor) to do gradesubmission for a particular assignmentsubmission done 
    by student for a particular assignment in a particular course  which was created by instructor
    by filling form GradeAssignmentSubmissionForm i.e uploading grade in that form\n
    :form_class: form to be filled for submitting grade
    :param template_name: corresponding html page to show grades
    :success_url: after successfully submitting form redirects to previous page
    """
    template_name = 'gradeassignment_submission.html'
    form_class = GradeAssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('users:course')

    @method_decorator(login_required(login_url=reverse_lazy('users:login')))
    def dispatch(self, request, *args, **kwargs):
        """This function checks if grade is already submitted or not if submitted then doesn't allow to fill form of grade assignment
        submission by redirecting to same page also checks if user is authenticated and also an instructor
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

    def form_valid(self, form,request):
        """
        Here checks if marks filled is less than max marks if not don't submit form if satisfied that condition then 
        saves form and sends form to gradeassignmentsubmissionview list
        """
        e = AssignmentSubmission.objects.get(id=self.kwargs['id'])
        y = Assignment.objects.get(id = e.no)
        form.instance.user = self.request.user
        form.instance.NO = e.id 
        print(y.assignment_marks)
        if (form.instance.marks > y.assignment_marks) :
            messages.error(request,"Marks should be less than or equal to max marks: "+str(y.assignment_marks))
            return redirect('users:gradeassignment_submission',e.id)
        return super(GradeAssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        This function allows to fill form by instructor if invalid then redirects to same page
        if valid then sends to anoher function form_valid to validate it further
        """
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form)


class AssignmentSubmissionListView(ListView):
    """
    This class is used for Assignment model to show users(instructors) submitted  assignments 
    by students for a particular assignment created in a particular course  which were created by instructor\n
    :param context_object_name:
    :param template_name: corresponding html page to show assignments
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
 
def GradeView(request,id):
    #assignment = get_object_or_404(Assignment, id=id)
    #return render(request, "view_course.html", {'course': course})
    """
    This function is used to show student their grade which is evaluated by autograder 
    """
    b = AssignmentSubmission.objects.get(id=id) 
    #model=AssignmentSubmission
    return render(request, 'autograde.html', {'assignment_submission':b})
    
class AssignmentSubmissionGradeListView(ListView):
    """This class is used for GradeAssignmentSubmission model to show users(students) recieved grades given by
    instructor for a particular assignment submission done by student for a particular assignment in a course  which were created by instructor\n
    :param context_object_name:
    :param template_name: corresponding html page to show grades
    """
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
