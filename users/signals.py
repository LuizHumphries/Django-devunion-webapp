from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile

#@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username = user.username,
            email=user.email
        )


#@receiver(post_delete, sender=Profile)
def user_delete(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_save.connect(create_profile, sender=User)
post_delete.connect(user_delete, sender=Profile)