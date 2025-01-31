from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .mixins import AdminLoginRequiredMixin  # Import the mixin
from django.urls import reverse_lazy
from .models import *
from .forms import *
from accounts.forms import *

class HomePageView(TemplateView):
    template_name = 'app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch all categories and their related services
        categories = ServiceCategory.objects.all()
        context['categories'] = categories
        
        # Fetch all clinic reviews
        clinic_reviews = ClinicReview.objects.all()
        context['clinic_reviews'] = clinic_reviews

        return context

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ServicesPageView(TemplateView):
    template_name = 'app/services.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact/contact.html'

class FeedbackPageView(TemplateView):
    template_name = 'app/feedback.html'

class FAQsPageView(TemplateView):
    template_name = 'app/faqs.html'

class SupportPageView(TemplateView):
    template_name = 'app/support.html'

class AdminPanelPageView(TemplateView):
    template_name = 'app/admin-panel.html'

def navbar_view(request):
    categories = ServiceCategory.objects.all()  # Fetch all categories
    return {'service_categories': categories}  # Return as context

# ListView: Display all service categories
class ServiceCategoryListView(ListView):
    model = ServiceCategory
    template_name = 'app/service-category/category_list.html'
    context_object_name = 'categories'

# DetailView: Display details of a single service category
class ServiceCategoryDetailView(DetailView):
    model = ServiceCategory
    template_name = 'app/service-category/category_detail.html'
    context_object_name = 'category'

# ListView: Display all service categories
class AdminServiceCategoryListView(AdminLoginRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'app/service-category/admin_category_list.html'
    context_object_name = 'categories'

# DetailView: Display details of a single service category
class AdminServiceCategoryDetailView(AdminLoginRequiredMixin, DetailView):
    model = ServiceCategory
    template_name = 'app/service-category/admin_category_detail.html'
    context_object_name = 'category'

# CreateView: Add a new service category
class AdminServiceCategoryCreateView(AdminLoginRequiredMixin, CreateView):
    model = ServiceCategory
    template_name = 'app/service-category/admin_category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('service-category-list')

# UpdateView: Edit an existing service category
class AdminServiceCategoryUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = ServiceCategory
    template_name = 'app/service-category/admin_category_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('service-category-list')

# DeleteView: Delete a service category
class AdminServiceCategoryDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = ServiceCategory
    template_name = 'app/service-category/admin_category_confirm_delete.html'
    success_url = reverse_lazy('service-category-list')

# ListView: Display all services
class ServiceListView(ListView):
    model = Service
    template_name = 'app/services/service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch categories to be able to display them in the template
        categories = ServiceCategory.objects.all()
        context['categories'] = categories
        return context

# DetailView: Display details of a single service
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'app/services/service_detail.html'
    context_object_name = 'service'

# ListView: Display all services
class AdminServiceListView(AdminLoginRequiredMixin, ListView):
    model = Service
    template_name = 'app/services/admin_service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch categories to be able to display them in the template
        categories = ServiceCategory.objects.all()
        context['categories'] = categories
        return context

# DetailView: Display details of a single service
class AdminServiceDetailView(AdminLoginRequiredMixin, DetailView):
    model = Service
    template_name = 'app/services/admin_service_detail.html'
    context_object_name = 'service'

# CreateView: Add a new service
class AdminServiceCreateView(AdminLoginRequiredMixin, CreateView):
    model = Service
    template_name = 'app/services/admin_service_form.html'
    fields = ['category', 'name', 'description', 'price', 'image']  # Include 'image' field
    success_url = reverse_lazy('service-list')

# UpdateView: Edit an existing service
class AdminServiceUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = Service
    template_name = 'app/services/admin_service_form.html'
    fields = ['category', 'name', 'description', 'price', 'image']  # Include 'image' field
    success_url = reverse_lazy('service-list')

# DeleteView: Delete a service
class AdminServiceDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'app/services/admin_service_confirm_delete.html'
    success_url = reverse_lazy('service-list')

def clinic_reviews(request):
    # Fetch only the 5-star reviews
    clinic_reviews = ClinicReview.objects.filter(rating=5)
    
    # Pass reviews to the template
    return render(request, 'clinic_reviews.html', {
        'clinic_reviews': clinic_reviews,
    })





class AdminSettingsPageView(AdminLoginRequiredMixin, ):
    template_name = 'app/admin-pages/admin-panel/admin_settings.html'

class AdminReportsPageView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'app/admin-pages/admin-panel/admin_reports.html'




# CRUD Views for Patient
class AdminDashboardPageView(AdminLoginRequiredMixin ,ListView):
    model = Patient
    template_name = 'app/admin-pages/admin-panel/admin_dashboard.html'
    context_object_name = 'patient_list'
    
class AdminPatientDetailView(AdminLoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'app/admin-pages/crud-patient/admin_patient_detail.html'
    context_object_name = 'patient'

class AdminPatientCreateView(AdminLoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'app/admin-pages/crud-patient/admin_patient_form.html'
    success_url = reverse_lazy('admin-dashboard')  # Redirect to dashboard after successful creation

def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save both User and Patient
            return redirect('success')  # Redirect to a success page after registration
    else:
        form = PatientForm()

    return render(request, 'register_patient.html', {'form': form})

class AdminPatientUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'app/admin-pages/crud-patient/admin_patient_form2.html'
    success_url = reverse_lazy('admin-dashboard')  # Redirect to dashboard after successful update

class AdminPatientDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'app/admin-pages/crud-patient/admin_patient_confirm_delete.html'
    success_url = reverse_lazy('admin-dashboard')  # Redirect to dashboard after successful deletion



# CRUD Views for Staff

class AdminStaffManagementListView(AdminLoginRequiredMixin, ListView):
    model = StaffProfile
    template_name = 'app/admin-pages/admin-panel/admin_staff_management.html'
    context_object_name = 'staff_list'
    

class AdminStaffDetailView(AdminLoginRequiredMixin, DetailView):
    model = StaffProfile
    form_class = StaffProfileForm
    template_name = 'app/admin-pages/crud-staff/admin_staff_detail.html'
    success_url = reverse_lazy('admin-staff-management')

class AdminStaffCreateView(AdminLoginRequiredMixin, CreateView):
    model = StaffProfile
    form_class = StaffProfileForm
    template_name = 'app/admin-pages/crud-staff/admin_staff_form.html'
    success_url = reverse_lazy('admin-staff-management')

class AdminStaffUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = StaffProfile
    form_class = StaffProfileForm
    template_name = 'app/admin-pages/crud-staff/admin_staff_form.html'
    success_url = reverse_lazy('admin-staff-management')

class AdminStaffDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = StaffProfile
    template_name = 'app/admin-pages/crud-staff/admin_staff_confirm_delete.html'
    success_url = reverse_lazy('admin-staff-management')



# CRUD Views for Appointments
class AdminAppointmentsListView(AdminLoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'app/admin-pages/admin-panel/admin_appointments.html'
    context_object_name = 'appointment_list'

class AdminAppointmentDetailView(AdminLoginRequiredMixin, DetailView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/admin-pages/crud-appointment/admin_appointment_detail.html'
    success_url = reverse_lazy('admin-appointments')

class AdminAppointmentCreateView(AdminLoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/admin-pages/crud-appointment/admin_appointment_form.html'
    success_url = reverse_lazy('admin-appointments')

class AdminAppointmentUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/admin-pages/crud-appointment/admin_appointment_form.html'
    success_url = reverse_lazy('admin-appointments')

class AdminAppointmentDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'app/admin-pages/crud-appointment/admin_appointment_confirm_delete.html'
    success_url = reverse_lazy('admin-appointments')

# CRUD Views for Consultations
class AdminConsultationsListView(AdminLoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'app/admin-pages/admin-panel/admin_consultations.html'
    context_object_name = 'consultation_list'

class AdminConsultationDetailView(AdminLoginRequiredMixin, DetailView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'app/admin-pages/crud-consultation/admin_consultation_detail.html'
    success_url = reverse_lazy('admin-consultations')

class AdminConsultationCreateView(AdminLoginRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'app/admin-pages/crud-consultation/admin_consultation_form.html'
    success_url = reverse_lazy('admin-consultations')

class AdminConsultationUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'app/admin-pages/crud-consultation/admin_consultation_form.html'
    success_url = reverse_lazy('admin-consultations')

class AdminConsultationDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'app/admin-pages/crud-consultation/admin_consultation_confirm_delete.html'
    success_url = reverse_lazy('admin-consultations')

# CRUD Views for Schedules
class AdminStaffScheduleListView(AdminLoginRequiredMixin, ListView):
    model = StaffSchedule
    template_name = 'app/admin-pages/admin-panel/admin_schedule.html'
    context_object_name = 'schedules'

class AdminStaffScheduleDetailView(AdminLoginRequiredMixin, DetailView):
    model = StaffSchedule
    template_name = 'app/admin-pages/crud-staff-schedule/admin_schedule_detail.html'
    context_object_name = 'schedule'

class AdminStaffScheduleCreateView(AdminLoginRequiredMixin, CreateView):
    model = StaffSchedule
    template_name = 'app/admin-pages/crud-staff-schedule/admin_schedule_form.html'
    fields = ['staff', 'day', 'start_time', 'end_time']
    success_url = reverse_lazy('admin-schedule-list')

class AdminStaffScheduleUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = StaffSchedule
    template_name = 'app/admin-pages/crud-staff-schedule/admin_schedule_form.html'
    fields = ['staff', 'day', 'start_time', 'end_time']
    success_url = reverse_lazy('admin-schedule-list')

class AdminStaffScheduleDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = StaffSchedule
    template_name = 'app/admin-pages/crud-staff-schedule/admin_schedule_confirm_delete.html'
    success_url = reverse_lazy('admin-schedule-list')

# Patient Record Views
class AdminPatientRecordListView(AdminLoginRequiredMixin, ListView):
    model = PatientRecord
    template_name = 'app/admin-pages/admin-panel/admin_patient_records.html'
    context_object_name = 'patient_record_list'

class AdminPatientRecordDetailView(AdminLoginRequiredMixin, DetailView):
    model = PatientRecord
    template_name = 'app/admin-pages/crud-patient-record/admin_patient_record_detail.html'
    context_object_name = 'patient_record'

class AdminPatientRecordCreateView(AdminLoginRequiredMixin, CreateView):
    model = PatientRecord
    form_class = PatientRecordForm
    template_name = 'app/admin-pages/crud-patient-record/admin_patient_record_form.html'
    success_url = reverse_lazy('admin-patient-records')

class AdminPatientRecordUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = PatientRecord
    form_class = PatientRecordForm
    template_name = 'app/admin-pages/crud-patient-record/admin_patient_record_form.html'
    success_url = reverse_lazy('admin-patient-records')

class AdminPatientRecordDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = PatientRecord
    template_name = 'app/admin-pages/crud-patient-record/admin_patient_record_confirm_delete.html'
    success_url = reverse_lazy('admin-patient-records')


# Medical Condition Views
class AdminMedicalConditionListView(AdminLoginRequiredMixin, ListView):
    model = MedicalCondition
    template_name = 'app/admin-pages/admin-panel/admin_medical_conditions.html'
    context_object_name = 'medical_condition_list'

class AdminMedicalConditionDetailView(AdminLoginRequiredMixin, DetailView):
    model = MedicalCondition
    template_name = 'app/admin-pages/crud-medical-condition/admin_medical_condition_detail.html'
    context_object_name = 'medical_condition'

class AdminMedicalConditionCreateView(AdminLoginRequiredMixin, CreateView):
    model = MedicalCondition
    form_class = MedicalConditionForm
    template_name = 'app/admin-pages/crud-medical-condition/admin_medical_condition_form.html'
    success_url = reverse_lazy('admin-medical-conditions')

class AdminMedicalConditionUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = MedicalCondition
    form_class = MedicalConditionForm
    template_name = 'app/admin-pages/crud-medical-condition/admin_medical_condition_form.html'
    success_url = reverse_lazy('admin-medical-conditions')

class AdminMedicalConditionDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = MedicalCondition
    template_name = 'app/admin-pages/crud-medical-condition/admin_medical_condition_confirm_delete.html'
    success_url = reverse_lazy('admin-medical-conditions')


# Medical History Views
class AdminMedicalHistoryListView(AdminLoginRequiredMixin, ListView):
    model = MedicalHistory
    template_name = 'app/admin-pages/admin-panel/admin_medical_histories.html'
    context_object_name = 'medical_history_list'

class AdminMedicalHistoryDetailView(AdminLoginRequiredMixin, DetailView):
    model = MedicalHistory
    template_name = 'app/admin-pages/crud-medical-history/admin_medical_history_detail.html'
    context_object_name = 'medical_history'

class AdminMedicalHistoryCreateView(AdminLoginRequiredMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'app/admin-pages/crud-medical-history/admin_medical_history_form.html'
    success_url = reverse_lazy('admin-medical-histories')

class AdminMedicalHistoryUpdateView(AdminLoginRequiredMixin, UpdateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'app/admin-pages/crud-medical-history/admin_medical_history_form.html'
    success_url = reverse_lazy('admin-medical-histories')

class AdminMedicalHistoryDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = MedicalHistory
    template_name = 'app/admin-pages/crud-medical-history/admin_medical_history_confirm_delete.html'
    success_url = reverse_lazy('admin-medical-histories')

# Admin Reports Generation View
class AdminGenerateReportsView(AdminLoginRequiredMixin, TemplateView):
    template_name = 'app/admin-pagess/admin_generate_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you want to generate reports for appointments
        appointments = Appointment.objects.all()
        context['appointments'] = appointments
        return context
    
# List View
class AdminClinicReviewListView(AdminLoginRequiredMixin, ListView):
    model = ClinicReview
    template_name = 'app/admin-pages/admin-panel/admin_review.html'  # Create this HTML file
    context_object_name = 'reviews'
    ordering = ['-date']  # Newest reviews first

    # List View
class AdminClinicReviewDetailView(AdminLoginRequiredMixin, DetailView):
    model = ClinicReview
    template_name = 'app/admin-pages/crud-clinic-reviews/admin_review_detail.html'  # Create this HTML file
    context_object_name = 'reviews-details'
    ordering = ['-date']  # Newest reviews first

# Delete View
class AdminClinicReviewDeleteView(AdminLoginRequiredMixin, DeleteView):
    model = ClinicReview
    template_name = 'app/admin-pages/crud-clinic-reviews/admin_review_confirm_delete.html'  # Create this HTML file
    success_url = reverse_lazy('admin-clinic-review')