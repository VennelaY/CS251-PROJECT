"""testsite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static
from . import views

app_name="users"

urlpatterns = [
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.login_view,name='home'),
    path('course/', CourseView.as_view(), name='course'),
    path('course-create/', CourseCreateView.as_view(), name='course-create'),
    path('avialble_course/', AvailableCourseView.as_view(), name='available_course'),
    path('<int:id>/course-view/', course_single, name='course-view'),
    path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('student/', views.student, name='student'),
    path('instructor/', views.instructor, name='instructor'),
    path('assignment_create/<int:id>',AssignmentCreateView.as_view() , name='assignment_create'),
    path('assignment/<int:id>', AssignmentView.as_view(), name='assignment-list'),
    path("password_change/", views.password_change, name="password_change"),
    path('update/', EditProfileView.as_view(), name='profile-update'),
    path('join/',views.join_course,name='join_course'),
    path('assignment_submission/<int:id>', AssignmentSubmissionView.as_view(), name='assignment_submission'),
    path('assignment-submission-list/<int:id>', AssignmentSubmissionListView.as_view(), name='assignment-submission-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

