from rest_framework.authentication import SessionAuthentication


class BaseSessionAuthenticationApiView(SessionAuthentication):

    def authenticate(self, request):
        return super().authenticate(request)
