from django import forms
from .models import *
from django.contrib.auth.models import User

class ClinicReviewForm(forms.ModelForm):
    class Meta:
        model = ClinicReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review...'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if len(review_text) < 10:
            raise forms.ValidationError("Review text must be at least 10 characters long.")
        return review_text

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class PatientForm(forms.ModelForm):
    # User fields for registration and editing
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="New Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=False)

    class Meta:
        model = Patient
        fields = [
            'date_of_birth', 'country', 'region', 'province', 'city_municipality', 'barangay', 'postal_code',
            'house_number_street', 'subdivision', 'contact_number', 'profile_picture'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.get('instance')  # Get the Patient instance
        if patient and patient.user:
            kwargs.setdefault('initial', {})
            kwargs['initial']['username'] = patient.user.username
            kwargs['initial']['first_name'] = patient.user.first_name
            kwargs['initial']['last_name'] = patient.user.last_name
            kwargs['initial']['email'] = patient.user.email

        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:  # Only check if passwords are provided
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_username(self):
        # Only check if the Patient instance has a user object or is a new instance
        username = self.cleaned_data.get('username')

        if self.instance.pk:  # Check if this is an existing patient
            if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():
                raise forms.ValidationError("Username already exists. Please choose another.")
        else:  # If this is a new patient
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.instance.pk:  # If editing an existing patient
            if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by another user.")
        else:  # If new patient
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use by another user.")
        return email

    def save(self, commit=True):
        patient = super().save(commit=False)

        # Check if the Patient already has an associated User, or if it's a new instance
        if not patient.pk:  # If the patient doesn't have a primary key, it's a new patient
            # Create a new User for this patient
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1'] or "default_password"  # If no password, set a default
            )
            patient.user = user  # Associate the new User with the Patient
        else:
            # If editing an existing Patient, update the associated User
            user = patient.user
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if self.cleaned_data['password1']:  # Update password only if provided
                user.set_password(self.cleaned_data['password1'])
            
            user.save()

        if commit:
            patient.save()  # Save the patient with the updated or newly created user

        return patient


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['user', 'date_of_birth', 'contact_number', 'address', 'position', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the position choices with available positions
        self.fields['position'].queryset = StaffPosition.objects.all()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'start_time', 'end_time', 'reason_for_visit', 'service', 'status']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['consultation_date', 'summary', 'prescription_given', 'follow_up_needed', 'patient_records']
        widgets = {
            'consultation_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class StaffScheduleForm(forms.ModelForm):
    class Meta:
        model = StaffSchedule
        fields = ['staff', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'day_of_week': forms.Select(choices=[
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'),
            ]),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['patient', 'diagnosis', 'treatment_plan']

class MedicalConditionForm(forms.ModelForm):
    class Meta:
        model = MedicalCondition
        fields = ['name', 'description']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['patient_record', 'conditions', 'start_date', 'end_date']