from django.contrib.auth.mixins import UserPassesTestMixin

class AdminLoginRequiredMixin(UserPassesTestMixin):
    """ Restricts access to users in Administrator or IT Staff groups """
    
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.groups.filter(name="Administrator").exists() or
            self.request.user.groups.filter(name="IT Staff").exists()
        )

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('login')  # Redirect to your login page or error page
