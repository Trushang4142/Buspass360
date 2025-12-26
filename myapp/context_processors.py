# myapp/context_processors.py
def user_profile(request):
    if request.user.is_authenticated:
        return {'logged_user': request.user}
    return {}
