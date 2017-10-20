from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)#, renderer_context={'indent':4})
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
    
class RESTResponse(Response):
    def __init__(self, data, **kwargs):
        #kwargs['content_type'] = 'application/json'
        super(RESTResponse, self).__init__(data=data, **kwargs)
        