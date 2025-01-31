from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminLoginRequiredMixin(UserPassesTestMixin):
    """ Restricts access to users in Administrator or IT Staff groups """
    
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Administrator").exists() or
            self.request.user.groups.filter(name="IT Staff").exists()
        )

    def handle_no_permission(self):
        return redirect('login')  # Adjust the redirect as needed
