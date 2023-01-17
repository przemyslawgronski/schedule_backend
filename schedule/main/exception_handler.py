from rest_framework.views import exception_handler
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # @param exc - exception object (e.g. ProtectedError)
    # @param context - dict with request, view, args, kwargs
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    if isinstance(exc, ProtectedError):
        response = Response(data={
            'error': 'ProtectedError',
            'message': str(exc.protected_objects)[:100]+'...'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response