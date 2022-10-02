from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class Middleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == "/":
            return

        if request.path_info == "/register/":
            return

        info = request.session.get("info")
        if info:
            return
            
        return redirect('/')