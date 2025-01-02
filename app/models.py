from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

# CountryofBirth model (kept separate, not connected to Region)
class CountryOfBirth(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Region model (not connected to Country)
class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Province model (connected to Region)
class Province(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='provinces')

    def __str__(self):
        return f"{self.name}, {self.region}"

# City/Municipality model (connected to Province)
class CityMunicipality(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name}, {self.province}"

# Barangay model (connected to City/Municipality)
class Barangay(models.Model):
    name = models.CharField(max_length=100)
    city_municipality = models.ForeignKey(CityMunicipality, on_delete=models.CASCADE, related_name='barangays')

    def __str__(self):
        return f"{self.name}, {self.city_municipality}"

# Postal Code model (connected to City/Municipality)
class PostalCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    city_municipality = models.ForeignKey(CityMunicipality, on_delete=models.CASCADE, related_name='postal_codes')

    def __str__(self):
        return f"{self.code} ({self.city_municipality})"

# Patient model (extended User model)
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')  # One-to-one with User
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(db_index=True)
        
    # Connects location models
    country = models.ForeignKey(CountryOfBirth, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    city_municipality = models.ForeignKey(CityMunicipality, on_delete=models.SET_NULL, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True, blank=True)
    postal_code = models.ForeignKey(PostalCode, on_delete=models.SET_NULL, null=True, blank=True)

    # Unique address fields for each patient
    house_number_street = models.CharField(max_length=255, blank=True, null=True)
    subdivision = models.CharField(max_length=255, blank=True, null=True)
    
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    profile_picture = models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# PatientRecord model, stores medical records for a patient: Connected to: Patient (ForeignKey).
class PatientRecord(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='record')  # One-to-One link to Patient
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    date_recorded = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.date_recorded}"

# MedicalCondition model, Represents a predefined medical condition: Connected to: MedicalHistory (ForeignKey).
class MedicalCondition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optional detailed description
    
    def __str__(self):
        return self.name

# MedicalHistory model, Tracks medical conditions for a patient: Connected to: Connected to: Patient (ForeignKey), MedicalCondition (ForeignKey).
class MedicalHistory(models.Model):
    patient_record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='medical_histories')  # ForeignKey to PatientRecord
    conditions = models.ManyToManyField(MedicalCondition, related_name='medical_histories')  # Many-to-Many relationship with MedicalCondition
    start_date = models.DateTimeField()  # When the condition was diagnosed or started
    end_date = models.DateTimeField(null=True, blank=True)  # When the condition resolved or ended, blank if ongoing
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ongoing_status = 'Ongoing' if not self.end_date else f"to {self.end_date}"
        return f"History for {self.patient_record.patient} ({self.start_date} {ongoing_status})"
    
# Predefined roles of staff: Connected to StaffProfile
class StaffPosition(models.Model):
    title = models.CharField(max_length=100, unique=True)  # Unique role names like "Doctor", "Nurse", etc.
    description = models.TextField(blank=True, null=True)  # Optionally store role description
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='staff_position', null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically create or associate a Group
        with the StaffPosition based on its title.
        """
        # Create or associate a Group with the title of this position
        if not self.group:
            self.group, _ = Group.objects.get_or_create(name=self.title)
        else:
            # Ensure the Group's name matches the position's title
            if self.group.name != self.title:
                self.group.name = self.title
                self.group.save()
        super().save(*args, **kwargs)

    def assign_permissions(self, permissions):
        """
        Assign a list of permissions to the Group associated with this StaffPosition.
        
        Args:
            permissions (list): A list of Permission objects or codenames.
        
        Raises:
            ValidationError: If any provided permission codename does not exist.
        """
        if not self.group:
            raise ValidationError(f"StaffPosition '{self.title}' does not have an associated Group.")

        for permission in permissions:
            if isinstance(permission, str):  # If a codename is provided
                try:
                    permission = Permission.objects.get(codename=permission)
                except Permission.DoesNotExist:
                    raise ValidationError(f"Permission with codename '{permission}' does not exist.")
            self.group.permissions.add(permission)

    def clear_permissions(self):
        """
        Clears all permissions assigned to the Group associated with this StaffPosition.
        """
        if self.group:
            self.group.permissions.clear()

    def get_assigned_permissions(self):
        """
        Retrieves all permissions assigned to the Group associated with this StaffPosition.

        Returns:
            QuerySet: A QuerySet of Permission objects.
        """
        return self.group.permissions.all() if self.group else Permission.objects.none()

    def __str__(self):
        return self.title

# StaffProfile model, extends Django's User model to represent clinic staff members: User (One-to-One), StaffPosition (ForeignKey), StaffSchedule, Appointment, Consultation, DoctorReview (ForeignKey).
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    position = models.ForeignKey(StaffPosition, on_delete=models.SET_NULL, null=True, related_name='staff_members')
    profile_picture = models.ImageField(upload_to='staff/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.position and self.position.group:
            self.user.groups.add(self.position.group)
        else:
            self.user.groups.clear()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.username

# StaffSchedule model, tracks working schedules of staff members: Tracks the working schedule of staff members: Connected to: StaffProfile (ForeignKey).
class StaffSchedule(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def working_hours(self):
        return f"{self.day_of_week}: {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

    def __str__(self):
        return f"{self.staff} schedule for {self.day_of_week}"

# Service Category Model
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Service Model
class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Optional field for service pricing
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)  # New field for picture upload

    def __str__(self):
        return f"{self.name} ({self.category.name})"

#AppointmentStatus model, Predefined statuses for an appointment, e.g., "scheduled" or "completed": Connected to: Appointment (ForeignKey).
class AppointmentStatus(models.Model):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (SCHEDULED, 'Scheduled'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    name = models.CharField(max_length=9, choices=STATUS_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, related_name="appointments")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason_for_visit = models.CharField(max_length=255, blank=True, null=True)  # Optional if service explains the visit
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")  # Direct connection to Service
    status = models.ForeignKey(AppointmentStatus, on_delete=models.PROTECT, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_appointments')

    def clean(self):
        # Ensure end time is after start time
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')

        # Check for overlapping appointments
        overlapping_appointments = Appointment.objects.filter(
            Q(doctor=self.doctor) | Q(patient=self.patient),
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)  # Exclude the current appointment

        if overlapping_appointments.exists():
            raise ValidationError('There is already an appointment during this time.')


    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def delete(self, *args, **kwargs):
        # Override delete to implement soft delete
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.start_time}"


# Consultation model, representing a medical consultation between a patient and a doctor: Connected to: Patient (ForeignKey), StaffProfile (ForeignKey, doctor).
class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation')
    consultation_date = models.DateTimeField()
    summary = models.TextField(blank=True, null=True)
    prescription_given = models.BooleanField(default=False)
    follow_up_needed = models.BooleanField(default=False)
    patient_records = models.ManyToManyField('PatientRecord', related_name="consultations", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation for {self.appointment.patient} with {self.appointment.doctor} on {self.consultation_date}"
    

# Prescription model, tracks medications prescribed to patients during appointments: Connected to: Patient (ForeignKey), Appointment (ForeignKey, optional).
class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)  # Optional appointment linkage
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()  # Instructions for taking the medication
    refills = models.PositiveIntegerField(default=0)  # Track number of refills allowed

    def __str__(self):
        return f"Prescription for {self.consultation.appointment.patient}: {self.medication_name}"


# Medical Test model, tracks tests performed during appointments, including optional test result images: Connected to: Appointment (ForeignKey).
class MedicalTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='tests')  # Linked to Appointment
    test_name = models.CharField(max_length=100)
    results = models.TextField(blank=True, null=True)  # Results of the test
    date_taken = models.DateField()  # When the test was performed
    test_image = models.ImageField(upload_to='medical_tests/', blank=True, null=True)  # Optional test result image

    def __str__(self):
        return f"Test: {self.test_name} for {self.appointment}"

#PaymentMethod model, Stores different payment methods used for billing, e.g., "credit card", "cash", etc: Connected to: Billing (ForeignKey).
class PaymentMethod(models.Model):
    method = models.CharField(max_length=50)
    details = models.TextField(blank=True, null=True)  # Any additional info for this payment method
    
    def __str__(self):
        return self.method
    
# Billing model, represents the billing of an appointment: Connected to: Appointment (ForeignKey), PaymentMethod (ForeignKey).
class Billing(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='billing')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="billings", help_text="The primary service being billed.")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total amount billed, adjusted based on doctor's recommendation.")
    date_issued = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Billing for {self.consultation.appointment} - Amount: {self.total_amount}"

    def save(self, *args, **kwargs):
        # Log a warning if the total amount is left as 0.00
        if self.total_amount <= 0.0:
            raise ValidationError("Total amount cannot be zero. Please update the amount based on doctor's recommendation.")
        super().save(*args, **kwargs)


# DoctorReview model, stores patient reviews and ratings for doctors: Connected to: StaffProfile (ForeignKey, doctor), Patient (ForeignKey).
# ***Consultation Review Dapat***
class ConsultationReview(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='review', help_text="The consultation being reviewed.")  # Link to Consultation
    doctor = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='consultation_reviews', help_text="The doctor involved in the consultation.")  # Link to the doctor from the consultation
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultation_reviews', help_text="The patient who is reviewing the consultation.")  # Link to the patient
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], help_text="Rating from 1 (lowest) to 5 (highest).")  # Rating scale
    review = models.TextField(help_text="The written review of the consultation.")
    date = models.DateTimeField(auto_now_add=True, help_text="The date the review was created.")

    def clean(self):
        # Ensure the doctor in the review matches the doctor in the consultation
        if self.consultation.appointment.doctor != self.doctor:
            raise ValidationError("The doctor in the review must match the doctor from the consultation.")

        # Ensure the patient in the review matches the patient in the consultation
        if self.consultation.appointment.patient != self.patient:
            raise ValidationError("The patient in the review must match the patient from the consultation.")

    def __str__(self):
        return f"Review by {self.patient} for Dr. {self.doctor} on {self.consultation.consultation_date}"

# NotificationType model: Represents a predefined notification type.
class NotificationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    default_message = models.TextField(blank=True, null=True)  # Optional default message

    def __str__(self):
        return self.name

# Notification model: Represents notifications for users, connected to a NotificationType.
class Notification(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='notifications')  # Directly linked to Patient
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, null=True, blank=True)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, null=True, blank=True)
    related_url = models.URLField(max_length=255, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.message and self.notification_type:
            self.message = self.notification_type.default_message
        super().save(*args, **kwargs)

    @classmethod
    def mark_all_as_read(cls, patient):
        cls.objects.filter(patient=patient, read=False, is_deleted=False).update(read=True)

    def mark_as_read(self):
        self.read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.patient.user.username} - {self.message[:20]}..."



# Supplier model, tracks the suppliers of inventory items: Connected to: Inventory (ForeignKey).
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()  # Supplier contact information
    supply_type = models.CharField(max_length=100)  # Type of supplies provided

    def __str__(self):
        return self.name

# Inventory model, tracks items (e.g., medical supplies) used in the clinic: Connected to: Supplier (ForeignKey), InventoryTransaction (ForeignKey).
class Inventory(models.Model):
    item_name = models.CharField(max_length=100)  # Name of the item
    description = models.TextField(blank=True, null=True)  # Optional description of the item
    quantity = models.PositiveIntegerField()  # Current stock quantity
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='supplies')  # Linked supplier
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    reorder_level = models.PositiveIntegerField(default=0)  # Stock level at which to reorder
    item_image = models.ImageField(upload_to='inventory/', blank=True, null=True)  # Item image (optional)

    def __str__(self):
        return f"{self.item_name} (Qty: {self.quantity})"

    def is_below_reorder_level(self):
        return self.quantity <= self.reorder_level

# TransactionType model, Represents predefined types of inventory transactions, e.g., "inflow" or "outflow":Connected to: InventoryTransaction (ForeignKey).
class TransactionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Inventory Transaction model, logs usage or movement of inventory items: Connected to: Inventory (ForeignKey), TransactionType (ForeignKey).
class InventoryTransaction(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='transactions')  # Linked to Inventory
    quantity_used = models.PositiveIntegerField()  # Amount used
    date = models.DateTimeField(auto_now_add=True)  # When the transaction occurred
    reason = models.TextField()  # Why the item was used
    notes = models.TextField(blank=True, null=True)  # Optional notes about the transaction
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.quantity_used} of {self.item} on {self.date}"



# Skin Condition Analysis Model, allows patients to upload images for AI-based skin condition analysis: Connected to: Patient (ForeignKey),
# SkinConditionPrediction (ForeignKey).
#class SkinConditionAnalysis(models.Model):
    #patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='skin_analyses')
    #uploaded_image = models.ImageField(upload_to='skin_conditions/')
    #results = models.JSONField()  # Replace the old JSONField here
    #analysis_date = models.DateTimeField(auto_now_add=True)
    #confirmed_by_doctor = models.BooleanField(default=False)


    #def __str__(self):
        #return f"Analysis for {self.patient} on {self.analysis_date}"
    
#SkinConditionPrediction model, Tracks predictions made by the AI for a skin condition analysis: Connected to: SkinConditionAnalysis (ForeignKey).
#class SkinConditionPrediction(models.Model):
    #analysis = models.ForeignKey(SkinConditionAnalysis, on_delete=models.CASCADE, related_name='predictions')
    #condition = models.CharField(max_length=100)
    #probability = models.DecimalField(max_digits=5, decimal_places=4)