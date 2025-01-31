from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from app.models import Patient

# Signal to create Patient profile automatically
@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)