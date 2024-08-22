import logging
from django.middleware.locale import LocaleMiddleware

logger = logging.getLogger(__name__)

class DebugLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        super().process_request(request)
        # Log the language code being set for this request
        logger.debug(f"LANGUAGE_CODE being used: {request.LANGUAGE_CODE}")

        # If you want to log more information about the request, you can add more here:
        if request.COOKIES.get('django_language'):
            logger.debug(f"Language cookie: {request.COOKIES.get('django_language')}")
        if request.session.get('django_language'):
            logger.debug(f"Language in session: {request.session.get('django_language')}")