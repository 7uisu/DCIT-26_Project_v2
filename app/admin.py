from django.contrib import admin
from .models import *

# Register models with Django admin
admin.site.register(CountryOfBirth)
admin.site.register(Region)
admin.site.register(Province)
admin.site.register(CityMunicipality)
admin.site.register(Barangay)
admin.site.register(PostalCode)
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(ServiceCategory)

admin.site.register(PatientRecord)
admin.site.register(MedicalCondition)
admin.site.register(MedicalHistory)
admin.site.register(StaffPosition)
admin.site.register(StaffProfile)
admin.site.register(AppointmentStatus)
admin.site.register(Appointment)
admin.site.register(Consultation)
admin.site.register(ClinicReview)
admin.site.register(Prescription)
admin.site.register(MedicalTest)
admin.site.register(PaymentMethod)
admin.site.register(Billing)
admin.site.register(StaffSchedule)

# admin.site.register(ConsultationReview)
# admin.site.register(NotificationType)
# admin.site.register(Notification)
#admin.site.register(SkinConditionAnalysis)
#admin.site.register(SkinConditionPrediction)
