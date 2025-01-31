from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView


urlpatterns = [
    path('login/', SignInPageView.as_view(), name='login'),
    path('sign-up/', SignUpPageView.as_view(), name='sign-up'),
    path('profile-fillup/', PatientProfileFillUpPageView.as_view(), name='profile-fillup'),
    path('profile/', PatientProfilePageView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Create View for patients
    path('reviews/create/', ClinicReviewCreateView.as_view(), name='clinic-review-create'),

    # Detail View for a specific review
    path('reviews/<int:pk>/', ClinicReviewDetailView.as_view(), name='clinic-review-detail'),

     # Password reset views
    path('password-reset/', password_reset_request, name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='app/password-reset/password_reset_done.html'), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password-reset-confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='app/password-reset/password_reset_complete.html'), name='password-reset-complete'),
]
