from django.contrib.auth.models import Group

def is_admin_or_it_staff(request):
    """
    Adds a context variable `is_admin_or_it_staff` that checks
    if the current user belongs to the Administrator or IT Staff group.
    """
    if request.user.is_authenticated:
        return {
            'is_admin_or_it_staff': request.user.groups.filter(name__in=["Administrator", "IT Staff"]).exists()
        }
    return {'is_admin_or_it_staff': False}
