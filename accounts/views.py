from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .forms import CustomAuthenticationForm, UserCreationForm, PatientProfileFillUpForm
from app.models import *
from app.forms import *

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


import logging

class SignInPageView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

class SignUpPageView(CreateView):
    template_name = 'registration/sign-up.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile-fillup')

class ClinicReviewCreateView(LoginRequiredMixin, CreateView):
    model = ClinicReview
    form_class = ClinicReviewForm
    template_name = 'app/clinic-reviews/review_form.html'
    success_url = reverse_lazy('home')  # Redirect to home page after review is created

    def form_valid(self, form):
        # Check if the user has a corresponding Patient profile
        if not hasattr(self.request.user, 'patient_profile'):
            form.add_error(None, "You need to have a patient profile to submit a review.")
            return self.form_invalid(form)

        form.instance.patient = self.request.user.patient_profile
        # Save the review first
        response = super().form_valid(form)
        return response

    
    # List View for Patients
class ClinicReviewDetailView(DetailView):
    model = ClinicReview
    template_name = 'app/clinic-reviews/review_detail.html'  # Create this HTML file
    context_object_name = 'reviews-details'
    ordering = ['-date']  # Newest reviews first
    
class PatientProfileFillUpPageView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientProfileFillUpForm
    template_name = 'registration/profile-fillup.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        patient, created = Patient.objects.get_or_create(user=self.request.user)
        return patient

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Ensure user is passed to the form if needed
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update the associated User model fields
        user = self.object.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        
        return response
    
class PatientProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch the logged-in user's patient profile
        try:
            patient = Patient.objects.get(user=self.request.user)
            context['patient'] = patient
            context['user'] = patient.user  # Optional: Add the User object explicitly if needed
        except Patient.DoesNotExist:
            context['patient'] = None
        
        return context

# Set up logger
logger = logging.getLogger(__name__)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "app/password-reset/password_reset_email.txt"
                    protocol = 'https' if request.is_secure() else 'http'
                    
                    # Context for the email
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Your site name',
                        "uid": urlsafe_base64_encode(bytes(str(user.pk), 'utf-8')),  # This encodes the user ID
                        "user": user,
                        'token': default_token_generator.make_token(user),  # This creates the reset token
                        'protocol': protocol,
                    }

                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, 'noreply@vstlivestockcorporation.net', [user.email], fail_silently=False)
                    
                    # Log reset request for the patient
                    try:
                        patient = user.patient_profile  # Accessing the Patient instance linked to the User
                        logger.info(f"Password reset request for patient: {patient}")
                    except Patient.DoesNotExist:
                        logger.warning(f"No associated patient profile found for user: {user}")
            return redirect("password-reset-done")
    password_reset_form = PasswordResetForm()
    return render(request, "app/password-reset/password_reset.html", {"password_reset_form": password_reset_form})

def password_reset_confirm(request, uidb64=None, token=None):
    UserModel = get_user_model()
    try:
        uid = str(urlsafe_base64_decode(uidb64))  # Updated here
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                try:
                    patient = user.patient_profile
                    logger.info(f"Password successfully reset for patient: {patient}")
                except Patient.DoesNotExist:
                    logger.warning(f"No associated patient profile found for user: {user}")
                
                messages.success(request, 'Your password has been successfully reset.')
                return redirect('password-reset-complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'app/password-reset/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid, possibly because it has already been used. Please request a new password reset.')
        return redirect('password-reset')