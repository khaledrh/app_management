from django.shortcuts import render
from django.utils.translation import activate
from django.http import HttpResponseRedirect

def homepage(request):
    return render(request, 'home.html')

def set_language(request, lang_code):
    # Activate the selected language
    activate(lang_code)
    
    # Set the language in the session
    request.session['django_language'] = lang_code
    
    # Create a response and set the 'django_language' cookie manually
    response = HttpResponseRedirect(request.GET.get('next', '/'))
    response.set_cookie('django_language', lang_code)
    
    return response