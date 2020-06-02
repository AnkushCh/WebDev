from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
# Create your models here.

MALE ='M'
FEMALE  = 'F'

Gender =(
	(MALE,'Male',),
	(FEMALE,'Female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=False)
    checkin = models.BooleanField(blank=False,default=0)
    time_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class TravelReimbursement(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    travel_date=models.DateField(blank=True)
    from_place=models.CharField(max_length=255)
    to_place=models.CharField(max_length=255)
    total_fare=models.PositiveIntegerField()
    upload_bill=models.ImageField(upload_to='bill_images',blank=True)
    time_generated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_generated']

    def get_absolute_url(self):
        return reverse('home') 
    
    def __str__(self):
        return self.user.username

class ProjectCategory(models.Model):
    name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class RegModel(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    company=models.CharField(max_length=255)
    gender=models.CharField(choices = Gender,max_length=1,default=MALE)
    signup_as=models.CharField(max_length=255)
    student_id=models.BooleanField(default=False)
    emp_opportunity=models.BooleanField()
    learn_ab_hackathon=models.CharField(max_length=255)
    github_url=models.URLField(blank=True)
    how_contribute=models.TextField()
    votes_total = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username

class Vote(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    voteregs = models.ForeignKey(RegModel,on_delete=models.CASCADE)
    class Meta:
        unique_together=('organizer','voteregs')    