from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Static pages
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('feedback/', FeedbackPageView.as_view(), name='feedback'),
    path('faqs/', FAQsPageView.as_view(), name='faqs'),
    path('support/', SupportPageView.as_view(), name='support'),
    path('admin-panel/', AdminPanelPageView.as_view(), name='admin-panel'),



    # Admin views
    path('admin-reviews/', AdminClinicReviewListView.as_view(), name='admin-clinic-review'),
    path('admin-reviews/<int:pk>/', AdminClinicReviewDetailView.as_view(), name='admin-clinic-review-detail'),
    path('admin-reviews/<int:pk>/delete/', AdminClinicReviewDeleteView.as_view(), name='admin-clinic-review-delete'),

    # ServiceCategory Home URLS
    path('service-categories/list/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('service-categories/<int:pk>/', ServiceCategoryDetailView.as_view(), name='service-category-detail'),

    # Service Home URLS
    path('services/list/', ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),

    # Static pages for the admin panel
    path('admin-dashboard/', AdminDashboardPageView.as_view(), name='admin-dashboard'),
    path('admin-patient/create/', AdminPatientCreateView.as_view(), name='admin-patient-create'),
    path('admin-patient/<int:pk>/update/', AdminPatientUpdateView.as_view(), name='admin-patient-update'),
    path('admin-patient/<int:pk>/delete/', AdminPatientDeleteView.as_view(), name='admin-patient-delete'),
    path('admin-patient/<int:pk>/', AdminPatientDetailView.as_view(), name='admin-patient-detail'),  # Add this line

    # path('admin-settings/', AdminSettingsPageView.as_view(), name='admin-settings'),
    path('admin-reports/', AdminReportsPageView.as_view(), name='admin-reports'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # CRUD URLs for Staff
    path('admin-staff-management/', AdminStaffManagementListView.as_view(), name='admin-staff-management'),
    path('admin-staff/<int:pk>/', AdminStaffDetailView.as_view(), name='admin-staff-detail'),
    path('admin-staff/create/', AdminStaffCreateView.as_view(), name='admin-staff-create'),
    path('admin-staff/<int:pk>/update/', AdminStaffUpdateView.as_view(), name='admin-staff-update'),
    path('admin-staff/<int:pk>/delete/', AdminStaffDeleteView.as_view(), name='admin-staff-delete'),

    # Admin URLs for Service Categories
    path('admin-service-categories/', AdminServiceCategoryListView.as_view(), name='admin-service-category'),
    path('admin-service-categories/<int:pk>/', AdminServiceCategoryDetailView.as_view(), name='admin-service-category-detail'),
    path('admin-service-categories/create/', AdminServiceCategoryCreateView.as_view(), name='admin-service-category-create'),
    path('admin-service-categories/<int:pk>/update/', AdminServiceCategoryUpdateView.as_view(), name='admin-service-category-update'),
    path('admin-service-categories/<int:pk>/delete/', AdminServiceCategoryDeleteView.as_view(), name='admin-service-category-delete'),

    # Admin URLs for Services
    path('admin-services/', AdminServiceListView.as_view(), name='admin-services'),
    path('admin-services/<int:pk>/', AdminServiceDetailView.as_view(), name='admin-service-detail'),
    path('admin-services/add/', AdminServiceCreateView.as_view(), name='admin-service-create'),
    path('admin-services/<int:pk>/update/', AdminServiceUpdateView.as_view(), name='admin-service-update'),
    path('admin-services/<int:pk>/delete/', AdminServiceDeleteView.as_view(), name='admin-service-delete'),

    # CRUD URLs for Appointments
    path('admin-appointments/', AdminAppointmentsListView.as_view(), name='admin-appointments'),
    path('admin-appointments/<int:pk>/', AdminAppointmentDetailView.as_view(), name='admin-appointment-detail'),
    path('admin-appointments/create/', AdminAppointmentCreateView.as_view(), name='admin-appointment-create'),
    path('admin-appointments/<int:pk>/update/', AdminAppointmentUpdateView.as_view(), name='admin-appointment-update'),
    path('admin-appointments/<int:pk>/delete/', AdminAppointmentDeleteView.as_view(), name='admin-appointment-delete'),

    # CRUD URLs for Consultations
    path('admin-consultations/', AdminConsultationsListView.as_view(), name='admin-consultations'),
    path('admin-consultations/<int:pk>/', AdminConsultationDetailView.as_view(), name='admin-consultation-detail'),
    path('admin-consultations/create/', AdminConsultationCreateView.as_view(), name='admin-consultation-create'),
    path('admin-consultations/<int:pk>/update/', AdminConsultationUpdateView.as_view(), name='admin-consultation-update'),
    path('admin-consultations/<int:pk>/delete/', AdminConsultationDeleteView.as_view(), name='admin-consultation-delete'),

    # Staff Schedule CRUD URLs
    path('admin-staff-schedule', AdminStaffScheduleListView.as_view(), name='admin-staff-schedule'),
    path('admin-staff-schedule/<int:pk>/', AdminStaffScheduleDetailView.as_view(), name='admin-staff-schedule-detail'),
    path('admin-staff-schedule/create/', AdminStaffScheduleCreateView.as_view(), name='admin-staff-schedule-create'),
    path('admin-staff-schedule/<int:pk>/update/', AdminStaffScheduleUpdateView.as_view(), name='admin-staff-schedule-update'),
    path('admin-staff-schedule/<int:pk>/delete/', AdminStaffScheduleDeleteView.as_view(), name='admin-staff-schedule-delete'),
    
    # Patient Record URLs
    path('admin-patient-records/', AdminPatientRecordListView.as_view(), name='admin-patient-records'),
    path('admin-patient-records/<int:pk>/', AdminPatientRecordDetailView.as_view(), name='admin-patient-record-detail'),
    path('admin-patient-records/add/', AdminPatientRecordCreateView.as_view(), name='admin-patient-record-create'),
    path('admin-patient-records/<int:pk>/edit/', AdminPatientRecordUpdateView.as_view(), name='admin-patient-record-update'),
    path('admin-patient-records/<int:pk>/delete/', AdminPatientRecordDeleteView.as_view(), name='admin-patient-record-delete'),
    
    # Medical Condition URLs
    path('admin-medical-conditions/', AdminMedicalConditionListView.as_view(), name='admin-medical-conditions'),
    path('admin-medical-conditions/<int:pk>/', AdminMedicalConditionDetailView.as_view(), name='admin-medical-condition-detail'),
    path('admin-medical-conditions/add/', AdminMedicalConditionCreateView.as_view(), name='admin-medical-condition-create'),
    path('admin-medical-conditions/<int:pk>/edit/', AdminMedicalConditionUpdateView.as_view(), name='admin-medical-condition-update'),
    path('admin-medical-conditions/<int:pk>/delete/', AdminMedicalConditionDeleteView.as_view(), name='admin-medical-condition-delete'),
    
    # Medical History URLs
    path('admin-medical-histories/', AdminMedicalHistoryListView.as_view(), name='admin-medical-histories'),
    path('admin-medical-histories/<int:pk>/', AdminMedicalHistoryDetailView.as_view(), name='admin-medical-history-detail'),
    path('admin-medical-histories/add/', AdminMedicalHistoryCreateView.as_view(), name='admin-medical-history-create'),
    path('admin-medical-histories/<int:pk>/edit/', AdminMedicalHistoryUpdateView.as_view(), name='admin-medical-history-update'),
    path('admin-medical-histories/<int:pk>/delete/', AdminMedicalHistoryDeleteView.as_view(), name='admin-medical-history-delete'),

    # Settings and Reports
    path('admin-reports/generate/', AdminGenerateReportsView.as_view(), name='admin-reports-generate'),
]
