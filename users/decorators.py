from django.core.exceptions import PermissionDenied


def user_is_student(function):

    #returns USER PERMISSION WITH STUDENT ROLE
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role=='student':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_instructor(function):
    
    #return: USER PERMISSION WITH INSTRUCTOR ROLE

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role=='instructor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
            
    return wrap
    
from django.core.exceptions import ValidationError


def validate_file(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.py','.zip','.gz','.tgz','.cpp','.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')
