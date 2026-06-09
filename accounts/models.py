from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # HR Fields
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    profile_picture = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture and self.profile_picture.name != 'default.jpg':
            try:
                img = Image.open(self.profile_picture.path)

                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.profile_picture.path)
            except Exception as e:
                print(f"Error resizing image: {e}")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()