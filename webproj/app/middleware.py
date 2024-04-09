from django.contrib.auth.models import AnonymousUser
from app.models import WizardAccount


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.get('authenticated', False):
            nmec = request.session.get('nmec')
            wizard_id = request.session.get('wizard_id')

            # Use the custom user object
            request.user = WizardAccount(nmec=nmec, wizard_id=wizard_id)
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response
