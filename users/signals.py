from django.db.models.signals import post_save 
from django.contrib.auth.models import User 
from django.dispatch import receiver, Signal 
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail



# Custom signal for password reset
password_reset_completed = Signal()

def send_password_reset_email(sender, user, request, **kwargs):
    subject = 'Your Password Has Been Reset'
    message = 'This is a confirmation that the password for your account has just been changed.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

password_reset_completed.connect(send_password_reset_email)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
