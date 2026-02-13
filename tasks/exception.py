from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

class NoPostFound(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = ('You can not add like to a not found post.')

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        raise NoPostFound()
    
    raise exceptions.NotAuthenticated
