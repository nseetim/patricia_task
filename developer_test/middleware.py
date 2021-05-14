import time
from .models import RequestLogs

from rest_framework.decorators import api_view

class LogRequest:
    def __init__(self, get_response):
        self.get_response = get_response

        # List of url's that should be logged, everything else ignored.
        # Use this if there are specific urls to be logged else just leave as-is
        self.prefixs = [
            '/url/prefixes/that/should/be/logged',
            '/*'
            '/api/',
        ]

    def __call__(self, request):
        _t = time.time() # Calculated execution time.
        response = self.get_response(request) # Get response from view function.
        _t = int((time.time() - _t)*1000)    

        # If the url does not start with on of the prefixes above, then return response and dont save log.
        # (Remove these two lines below to log everything)
        # if not list(filter(request.get_full_path().startswith, self.prefixs)): 
        #    return response 

        # Create instance of our model and assign values
        request_log = RequestLogs(
            endpoint=request.get_full_path(),
            response_code=response.status_code,
            method=request.method,
            remote_address=self.get_client_ip(request),
            exec_time=_t,
            body_response=str(response.content),
            body_request=str(response.content)
        )

        # If the user is not annonymous i.e not signed in then attach the user to the Log
        if not request.user.is_anonymous:
            request_log.user = request.user

        # Write the Log to the DB
        request_log.save() 
        return response

    # To get IP of the request origin
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            _ip = x_forwarded_for.split(',')[0]
        else:
            _ip = request.META.get('REMOTE_ADDR')
        return _ip