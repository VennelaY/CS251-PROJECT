from django.core.exceptions import PermissionDenied


def user_is_student(function):
    """This function decides whether user is student 
    :param function: 
    :type function: HttpRequest object
    :return: User Permission With Student role
    :rtype: 
    """
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role=='student':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_instructor(function):
    """This function decides whether user is instructor 
    :param function: 
    :type function: HttpRequest object
    :return: User permission with Instructor Role
    :rtype: 
    """
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role=='instructor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
            
    return wrap
    
from django.core.exceptions import ValidationError

def validate_file(value):
    """This function decides whether fie extension is valid/not 
    :param value: file for which extension need to be checked
    :type value: file name
    :return: Validdation error if extension is not valid(i.e not our required)
    """
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = []
    if not ext in valid_extensions:
        raise ValidationError('File not supported!')

def valid(value):
    """This function decides whether fie extension is valid/not 
    :param value: checks if file extension is .txt
    :type value: file name
    :return: Validation error if extension is not valid(i.e not .txt)
    """
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt']
    if not ext in valid_extensions:
        raise ValidationError('File not supported!Only txt file is valid')        

def valid1(value):
    """This function decides whether fie extension is valid/not 
    :param value: checks if fi;e extension is .zip
    :type value: file name
    :return: Validation error if extension is not valid(i.e not .pdf)
    """
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.zip']
    if not ext in valid_extensions:
        raise ValidationError('File not supported! Only zip file is valid') 