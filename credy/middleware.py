from django.utils.deprecation import MiddlewareMixin

class SetCounterMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        hit = request.session.get('hit')
        if not hit:
            request.session['hit'] = 1
        else:
            request.session['hit'] += 1
        return response
